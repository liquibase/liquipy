#!/usr/bin/env python
import os
import unittest2 as unittest

from mock import patch, mock_open, MagicMock

import liquipy
from liquipy.changeset import XMLWriter


class XMLWriterTest(unittest.TestCase):
  
  def testOneSimpleChangeSetSuccess(self):
    changes = {'1': {
      'author': 'Author',
      'comment': 'Comment',
      'sql': 'SQL',
      'rollback': 'Rollback'
    }}

    expected = """<?xml version="1.0" encoding="UTF-8"?>
<databaseChangeLog
        xmlns="http://www.liquibase.org/xml/ns/dbchangelog"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:ext="http://www.liquibase.org/xml/ns/dbchangelog-ext"
        xsi:schemaLocation="http://www.liquibase.org/xml/ns/dbchangelog http://www.liquibase.org/xml/ns/dbchangelog/dbchangelog-3.0.xsd
        http://www.liquibase.org/xml/ns/dbchangelog-ext http://www.liquibase.org/xml/ns/dbchangelog/dbchangelog-ext.xsd">
  <changeSet id="1" author="Author">
    <comment>Comment</comment>
    <sql><![CDATA[
SQL
    ]]></sql>
    <rollback><![CDATA[
Rollback
    ]]></rollback>
  </changeSet>
</databaseChangeLog>
"""

    writer = XMLWriter('outputFilePath')
    mockOpen = mock_open()
    mockOutputFile = MagicMock()
    mockOpen.return_value = mockOutputFile

    with patch('liquipy.changeset.open', mockOpen, create=True):
      writer.write(changes)

    _, fileWriteArgs, _ = mockOutputFile.mock_calls[1]

    mockOpen.assert_called_once_with('outputFilePath', 'w')
    self.assertEqual(expected, fileWriteArgs[0])


  def testOneSimpleChangeSetWithTagSuccess(self):
    changes = {'1': {
      'author': 'Author',
      'comment': 'Comment',
      'sql': 'SQL',
      'rollback': 'Rollback',
      'tag': 1.0
    }}

    expected = """<?xml version="1.0" encoding="UTF-8"?>
<databaseChangeLog
        xmlns="http://www.liquibase.org/xml/ns/dbchangelog"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:ext="http://www.liquibase.org/xml/ns/dbchangelog-ext"
        xsi:schemaLocation="http://www.liquibase.org/xml/ns/dbchangelog http://www.liquibase.org/xml/ns/dbchangelog/dbchangelog-3.0.xsd
        http://www.liquibase.org/xml/ns/dbchangelog-ext http://www.liquibase.org/xml/ns/dbchangelog/dbchangelog-ext.xsd">
  <changeSet id="1" author="Author">
    <comment>Comment</comment>
    <sql><![CDATA[
SQL
    ]]></sql>
    <rollback><![CDATA[
Rollback
    ]]></rollback>
  </changeSet>
  <changeSet id="1-tag" author="liquipy">
      <tagDatabase tag="1.0"/>
  </changeSet>
</databaseChangeLog>
"""

    writer = XMLWriter('outputFilePath')
    mockOpen = mock_open()
    mockOutputFile = MagicMock()
    mockOpen.return_value = mockOutputFile

    with patch('liquipy.changeset.open', mockOpen, create=True):
      writer.write(changes)

    _, fileWriteArgs, _ = mockOutputFile.mock_calls[1]

    mockOpen.assert_called_once_with('outputFilePath', 'w')
    self.assertEqual(expected, fileWriteArgs[0])


  def testManyChangeSetsSuccess(self):
    changes = {'1': {
      'author': 'Author 1',
      'comment': 'Comment 1',
      'sql': 'SQL 1',
      'rollback': 'Rollback 1',
      'tag': 1.0
    }, '2': {
      'author': 'Author 2',
      'comment': 'Comment 2',
      'sql': 'SQL 2',
      'rollback': 'Rollback 2',
    }, '3': {
      'author': 'Author 1',
      'comment': 'Comment 3',
      'sql': 'SQL 3',
      'rollback': 'Rollback 3',
      'tag': 2.0
    }, '4': {
      'author': 'Author 2',
      'comment': 'Comment 4',
      'sql': 'SQL 4',
      'rollback': 'Rollback 4',
    }}

    expected = """<?xml version="1.0" encoding="UTF-8"?>
<databaseChangeLog
        xmlns="http://www.liquibase.org/xml/ns/dbchangelog"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:ext="http://www.liquibase.org/xml/ns/dbchangelog-ext"
        xsi:schemaLocation="http://www.liquibase.org/xml/ns/dbchangelog http://www.liquibase.org/xml/ns/dbchangelog/dbchangelog-3.0.xsd
        http://www.liquibase.org/xml/ns/dbchangelog-ext http://www.liquibase.org/xml/ns/dbchangelog/dbchangelog-ext.xsd">
  <changeSet id="1" author="Author 1">
    <comment>Comment 1</comment>
    <sql><![CDATA[
SQL 1
    ]]></sql>
    <rollback><![CDATA[
Rollback 1
    ]]></rollback>
  </changeSet>
  <changeSet id="1-tag" author="liquipy">
      <tagDatabase tag="1.0"/>
  </changeSet>
  <changeSet id="2" author="Author 2">
    <comment>Comment 2</comment>
    <sql><![CDATA[
SQL 2
    ]]></sql>
    <rollback><![CDATA[
Rollback 2
    ]]></rollback>
  </changeSet>
  <changeSet id="3" author="Author 1">
    <comment>Comment 3</comment>
    <sql><![CDATA[
SQL 3
    ]]></sql>
    <rollback><![CDATA[
Rollback 3
    ]]></rollback>
  </changeSet>
  <changeSet id="3-tag" author="liquipy">
      <tagDatabase tag="2.0"/>
  </changeSet>
  <changeSet id="4" author="Author 2">
    <comment>Comment 4</comment>
    <sql><![CDATA[
SQL 4
    ]]></sql>
    <rollback><![CDATA[
Rollback 4
    ]]></rollback>
  </changeSet>
</databaseChangeLog>
"""

    writer = XMLWriter('outputFilePath')
    mockOpen = mock_open()
    mockOutputFile = MagicMock()
    mockOpen.return_value = mockOutputFile

    with patch('liquipy.changeset.open', mockOpen, create=True):
      writer.write(changes)

    _, fileWriteArgs, _ = mockOutputFile.mock_calls[1]

    mockOpen.assert_called_once_with('outputFilePath', 'w')
    self.assertEqual(expected, fileWriteArgs[0])


  def testWriterRaisesExceptionWhenAuthorMissing(self):
    changes = {'1': {
      'comment': 'Comment',
      'sql': 'SQL',
      'rollback': 'Rollback',
      'tag': 1.0
    }}

    writer = XMLWriter('')

    with self.assertRaisesRegexp(Exception, 'ChangeSet "1" missing required attribute "author"'):
      writer.write(changes)


  def testWriterRaisesExceptionWhenCommentMissing(self):
    changes = {'1': {
      'author': 'Author',
      'sql': 'SQL',
      'rollback': 'Rollback',
      'tag': 1.0
    }}

    writer = XMLWriter('')

    with self.assertRaisesRegexp(Exception, 'ChangeSet "1" missing required attribute "comment"'):
      writer.write(changes)


  def testWriterRaisesExceptionWhenSqlMissing(self):
    changes = {'1': {
      'author': 'Author',
      'comment': 'Comment',
      'rollback': 'Rollback',
      'tag': 1.0
    }}

    writer = XMLWriter('')

    with self.assertRaisesRegexp(Exception, 'ChangeSet "1" missing required attribute "sql"'):
      writer.write(changes)


  def testWriterRaisesExceptionWhenRollbackMissing(self):
    changes = {'1': {
      'author': 'Author',
      'comment': 'Comment',
      'sql': 'SQL',
      'tag': 1.0
    }}

    writer = XMLWriter('')

    with self.assertRaisesRegexp(Exception, 'ChangeSet "1" missing required attribute "rollback"'):
      writer.write(changes)



if __name__ == '__main__':
  unittest.main()
