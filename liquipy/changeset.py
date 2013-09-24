# Copyright 2013 Numenta

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

ROOT_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<databaseChangeLog
        xmlns="http://www.liquibase.org/xml/ns/dbchangelog"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:ext="http://www.liquibase.org/xml/ns/dbchangelog-ext"
        xsi:schemaLocation="http://www.liquibase.org/xml/ns/dbchangelog http://www.liquibase.org/xml/ns/dbchangelog/dbchangelog-3.0.xsd
        http://www.liquibase.org/xml/ns/dbchangelog-ext http://www.liquibase.org/xml/ns/dbchangelog/dbchangelog-ext.xsd">%s
</databaseChangeLog>
"""
CHANGESET_TEMPLATE = """
  <changeSet id="%s" author="%s">
    <comment>%s</comment>
    <sql><![CDATA[
%s
    ]]></sql>
    <rollback><![CDATA[
%s
    ]]></rollback>
  </changeSet>"""
CHANGESET_TAG_TEMPLATE = """
  <changeSet id="%s" author="%s">
      <tagDatabase tag="%s"/>
  </changeSet>"""

class XMLWriter(object):
  """
  Writes a changeset to XML in the proper format for Liquibase.
  """

  REQUIRED = ['author', 'comment', 'sql', 'rollback']

  def __init__(self, outputFile):
    self.outputFile = outputFile


  def write(self, changes):
    # data structure to xml
    xmlOut = ""
    for changeSetId in sorted(changes.keys()):
      changeSet = changes[changeSetId]
      self._validateChangeSet(changeSetId, changeSet, self.REQUIRED)
      xmlOut += CHANGESET_TEMPLATE % (
        changeSetId, changeSet['author'], changeSet['comment'],
        changeSet['sql'], changeSet['rollback'])
      if 'tag' in changeSet:
        xmlOut += CHANGESET_TAG_TEMPLATE % (
          str(changeSetId) + "-tag", 
          'liquipy', 
          changeSet['tag'])
    xmlOut = ROOT_TEMPLATE % (xmlOut,)

    with open(self.outputFile, "w") as f:
      f.write(xmlOut)

  def _validateChangeSet(self, id, changeSet, requiredAttributes):
    for attribute in requiredAttributes:
      if attribute not in changeSet:
        raise Exception(('ChangeSet "%s" missing required attribute "%s"') % (str(id), attribute))

