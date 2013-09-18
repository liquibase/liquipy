import unittest2 as unittest

from mock import patch, mock_open, Mock, MagicMock

import liquipy
from liquipy import Database

class LiquipyDatabaseTest(unittest.TestCase):

  def testYamlInlineChanges(self):
    mockYaml = """1: 
  author: a1
  comment: c1
  tag: t1
  sql: sql
  rollback: rollback
2: 
  author: a2
  comment: c2
  sql: sql 2
  rollback: rollback 2
"""

    db = Database()

    with patch('liquipy.db.open', mock_open(read_data=mockYaml), create=True):
      changes = db.inputYamlToChangeSets('yamlPath')

    changeKeys = changes.keys()
    self.assertNotIn(0, changeKeys)
    self.assertIn(1, changeKeys)
    self.assertIn(2, changeKeys)
    self.assertNotIn(3, changeKeys)
    # Just test the structure of one. Other tests around how change sets are 
    # created from YAML input are in xmlwriter_test.py.
    changeOne = changes[1]
    self.assertIn('author', changeOne)
    self.assertIn('comment', changeOne)
    self.assertIn('tag', changeOne)
    self.assertIn('sql', changeOne)
    self.assertIn('rollback', changeOne)


  def testYamlRelativeLocalFileInclude(self):
    mockMasterYaml = """include:
  directory: migrations
"""
    mockIncludedYaml = """1: 
  author: a1
  comment: c1
  sql: sql
  rollback: rollback
"""

    masterChangeSetFilePath = 'master_changeset.yml'

    db = Database()

    def side_effect(filePath, mode):
      mockFile = Mock()
      if filePath == masterChangeSetFilePath:
        mockFile.read = Mock(return_value=mockMasterYaml)
      else:
        self.assertEqual('migrations/include1.yml', filePath)
        mockFile.read = Mock(return_value=mockIncludedYaml)
      return mockFile

    mockOpen = mock_open()
    mockOpen.side_effect = side_effect
    mockListdir = Mock(return_value=['include1.yml', 'other.thing'])

    with patch('liquipy.db.open', mockOpen, create=True):
      with patch('liquipy.db.listdir', mockListdir, create=True):
        changes = db.inputYamlToChangeSets(masterChangeSetFilePath)

    mockListdir.assert_called_once_with('migrations')

    changeKeys = changes.keys()
    self.assertNotIn('include', changeKeys)
    self.assertNotIn(0, changeKeys)
    self.assertIn(1, changeKeys)
    self.assertNotIn(2, changeKeys)
    # Just test the structure of one. Other tests around how change sets are 
    # created from YAML input are in xmlwriter_test.py.
    changeOne = changes[1]
    self.assertIn('author', changeOne)
    self.assertIn('comment', changeOne)
    self.assertIn('sql', changeOne)
    self.assertIn('rollback', changeOne)



  def testYamlAbsoluteFileInclude(self):
    mockMasterYaml = """include:
  directory: migrations
"""
    mockIncludedYaml = """1: 
  author: a1
  comment: c1
  sql: sql
  rollback: rollback
"""

    masterChangeSetFilePath = '/foo/bar/baz/master_changeset.yml'

    db = Database()

    def side_effect(filePath, mode):
      mockFile = Mock()
      if filePath == masterChangeSetFilePath:
        mockFile.read = Mock(return_value=mockMasterYaml)
      else:
        self.assertEqual('/foo/bar/baz/migrations/include1.yml', filePath)
        mockFile.read = Mock(return_value=mockIncludedYaml)
      return mockFile

    mockOpen = mock_open()
    mockOpen.side_effect = side_effect
    mockListdir = Mock(return_value=['include1.yml', 'other.thing'])

    with patch('liquipy.db.open', mockOpen, create=True):
      with patch('liquipy.db.listdir', mockListdir, create=True):
        changes = db.inputYamlToChangeSets(masterChangeSetFilePath)

    mockListdir.assert_called_once_with('/foo/bar/baz/migrations')

    changeKeys = changes.keys()
    self.assertNotIn(0, changeKeys)
    self.assertIn(1, changeKeys)
    self.assertNotIn(2, changeKeys)
    # Just test the structure of one. Other tests around how change sets are 
    # created from YAML input are in xmlwriter_test.py.
    changeOne = changes[1]
    self.assertIn('author', changeOne)
    self.assertIn('comment', changeOne)
    self.assertIn('sql', changeOne)
    self.assertIn('rollback', changeOne)



  def testIncludeWithMissingDirectoryRaisesException(self):
    self.fail()

