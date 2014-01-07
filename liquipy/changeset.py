# Copyright 2014 Numenta

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# NOTE/WARNING: The generated ChangeLog content and its order MUST not change
#  from one invocation of liquipy to the next! Any changes to the
#  ChangeLog/ChangeSet *_TEMPLATE values below, and ultimately any changes in
#  the ChangeLog/ChangeSet content may have the DISASTROUS side-effect of
#  causing previously-executed changeSets to be re-executed, likely CORRUPTING
#  the database tables or their content. This is because liquibase uses the MD5
#  checksum of the ChangeSets as well as some attributes from the ChangeLog
#  (among others) to generate a unique key when determining which ChangeSets
#  have already been executed and which still need to be executed. So, changing
#  the content makes it appear as if it had not been executed, resulting in
#  re-execution of previously-executed ChangeSets.

ROOT_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<databaseChangeLog
        logicalFilePath="%(logicalFilePath)s"
        xmlns="http://www.liquibase.org/xml/ns/dbchangelog"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:ext="http://www.liquibase.org/xml/ns/dbchangelog-ext"
        xsi:schemaLocation="http://www.liquibase.org/xml/ns/dbchangelog http://www.liquibase.org/xml/ns/dbchangelog/dbchangelog-3.0.xsd
        http://www.liquibase.org/xml/ns/dbchangelog-ext http://www.liquibase.org/xml/ns/dbchangelog/dbchangelog-ext.xsd">%(content)s
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

  _LOGICAL_CHANGELOG_FILE_PATH = "liquipy_logical_changelog_path.xml"
  """ Logical file path to associate with the generated liquibase changelog.
  NOTE: this value MUST NEVER CHANGE! Changing it will cause all previously-
  executed changesets to be re-executed.

  EXPLANATION: The never-changing logical file path is needed because liquibase
  uses the changelog filepath, along with the changeset's md5 checksum and other
  attributes, to uniquely identify executed changesets when determining whether
  a changeset needs to be executed. Since we generate the changelog XML file
  dynamically and at an absolute path (typically in a temp directory), using the
  ever-chaning physical path would lead to re-execution of all changesets that
  were previously executed.
  """

  REQUIRED = ["author", "comment", "sql", "rollback"]

  def __init__(self, outputFile):
    self.outputFile = outputFile


  def write(self, changes):
    # data structure to xml
    xmlOut = ""
    for changeSetId in sorted(changes.keys()):
      changeSet = changes[changeSetId]
      self._validateChangeSet(changeSetId, changeSet, self.REQUIRED)
      xmlOut += CHANGESET_TEMPLATE % (
        changeSetId, changeSet["author"], changeSet["comment"],
        changeSet["sql"], changeSet["rollback"])
      if "tag" in changeSet:
        xmlOut += CHANGESET_TAG_TEMPLATE % (
          str(changeSetId) + "-tag",
          "liquipy",
          changeSet["tag"])
    xmlOut = ROOT_TEMPLATE % {
      "logicalFilePath": self._LOGICAL_CHANGELOG_FILE_PATH,
      "content": xmlOut}

    with open(self.outputFile, "w") as f:
      f.write(xmlOut)

  @classmethod
  def _validateChangeSet(cls, changeSetId, changeSet, requiredAttributes):
    for attribute in requiredAttributes:
      if attribute not in changeSet:
        raise Exception(("ChangeSet %r missing required attribute %r") % (
          str(changeSetId), attribute))

