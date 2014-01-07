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

import logging
import os
import tempfile
import yaml

from liquipy.changeset import XMLWriter as ChangeSetWriter
from liquipy.executor import Executor as LiquibaseExecutor



DEFAULT = {
  "host": "localhost",
  "port": "3306",
  # TODO: we shouldn't have test settings in production code.
  "database": "liquipy_test",
  "username": "root",
  "password": ""
}



g_logger = logging.getLogger("liquipy.db")



class LiquipyDatabase(object):
  """
  Main interface for Liquipy
  """

  _GENERATED_CHANGELOG_FILE_NAME = "liquipy_changelog.xml"
  """ This is the name of the generated changlog xml file """

  def __init__(self, host=DEFAULT["host"],
                     port=DEFAULT["port"],
                     database=DEFAULT["database"],
                     username=DEFAULT["username"],
                     password=DEFAULT["password"],
                     tempDir=None):
    self.liquibaseExecutor = LiquibaseExecutor(host, port, database, username,
                                               password)
    self.tempDir = tempDir
    self.changes = None


  def initialize(self, yamlPath):
    self.changes = self.inputYamlToChangeSets(yamlPath)


  def inputYamlToChangeSets(self, yamlPath):
    rawYaml = open(yamlPath, "r").read()
    try:
      changes = yaml.load(rawYaml)
    except yaml.scanner.ScannerError as e:
      msg = "Error parsing input YAML file %r:\n%r" % (yamlPath, e)
      raise Exception(msg)
    if "include" in changes.keys():
      relativeTargetDir = changes["include"]["directory"]
      currentDir = os.path.join(os.path.split(yamlPath)[:-1])[0]
      targetDir = os.path.join(currentDir, relativeTargetDir)
      try:
        dirFiles = os.listdir(targetDir)
      except Exception as e:
        raise Exception("Included directory %r does not exist (%r)" % (
          targetDir, e))
      migrationFiles = [
        os.path.join(targetDir, f)
        for f in dirFiles
        if f.endswith(".yml")
      ]
      for includedMigration in migrationFiles:
        includeChanges = self.inputYamlToChangeSets(includedMigration)
        # TODO Need validation to make sure that the same ID is not reused!
        #   Issue https://github.com/GrokSolutions/liquipy/issues/15
        changes.update(includeChanges)
      del changes["include"]
    return changes


  def _getTempXMLChangeLogFilePath(self):
    """
    retval: filepath to be used for the generated ChangeLog XML file; MOTE: if
      tempDir was not specified by the user via constructor (self.tempDir is
      None), then an empty file will be created via tempfile.mkstemp as a
      place-holder for avoiding tempfile race conditions, and the caller is
      responsible for deleting that file
    """
    if self.tempDir is not None:
      # Generate the path inside user-supplied tempDir
      tempXMLChangeLogFilePath = os.path.join(
        self.tempDir,
        self._GENERATED_CHANGELOG_FILE_NAME)
    else:
      # Safely create a temp file and return its path
      (tempFD, tempXMLChangeLogFilePath) = tempfile.mkstemp(
        suffix=self._GENERATED_CHANGELOG_FILE_NAME)
      # Don't need the fd, so close it
      os.close(tempFD)

    return tempXMLChangeLogFilePath


  def update(self):
    g_logger.info("Running all migrations on db=%s",
                  self.liquibaseExecutor.database)

    tempXMLChangeLogFilePath = self._getTempXMLChangeLogFilePath()
    try:
      ChangeSetWriter(tempXMLChangeLogFilePath).write(self.changes)

      self.liquibaseExecutor.run(tempXMLChangeLogFilePath, "update")
    except:
      # On error, leave the genearted changelog file in place for debugging
      raise
    else:
      # Delete the generated changelog file if the user didn't provide tempDir
      if self.tempDir is None:
        os.unlink(tempXMLChangeLogFilePath)


  def rollback(self, tagName):
    g_logger.info("Rolling back db=%s to tag=%s",
                  self.liquibaseExecutor.database, tagName)

    tempXMLChangeLogFilePath = self._getTempXMLChangeLogFilePath()
    try:
      ChangeSetWriter(tempXMLChangeLogFilePath).write(self.changes)

      self.liquibaseExecutor.run(tempXMLChangeLogFilePath, "rollback",
                                 tagName)
    except:
      # On error, leave the genearted changelog file in place for debugging
      raise
    else:
      # Delete the generated changelog file if the user didn't provide tempDir
      if self.tempDir is None:
        os.unlink(tempXMLChangeLogFilePath)


  def getTags(self):
    return [
      {"tag": self.changes[c]["tag"], "changeSet": c}
      for c in self.changes.keys()
      if "tag" in self.changes[c]
    ]

