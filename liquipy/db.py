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

import yaml
from os import listdir
from os.path import join, split

from liquipy.changeset import XMLWriter as ChangeSetWriter
from liquipy.executor import Executor as LiquibaseExecutor

DEFAULT = {
  'host': "localhost",
  'database': "liquipy_test",
  'username': "root",
  'password': "",
  'tempDir': "/tmp"
}

class LiquipyDatabase(object):
  """
  Main interface for Liquipy
  """

  def __init__(self, host=DEFAULT['host'],
                     database=DEFAULT['database'],
                     username=DEFAULT['username'],
                     password=DEFAULT['password'],
                     tempDir=DEFAULT['tempDir']):
    self.liquibaseExecutor = LiquibaseExecutor(host, database, username,
                                               password)
    self.tempDir = tempDir
    self.outputXmlChangeLogFilePath = self.tempDir + "/liquipy_changelog.xml"
    self.changes = None



  def initialize(self, yamlPath):
    self.changes = self.inputYamlToChangeSets(yamlPath)
    changeSetWriter = ChangeSetWriter(self.outputXmlChangeLogFilePath)
    changeSetWriter.write(self.changes)


  def inputYamlToChangeSets(self, yamlPath):
    rawYaml = open(yamlPath, 'r').read()
    try:
      changes = yaml.load(rawYaml)
    except yaml.scanner.ScannerError as e:
      msg = "Error parsing input YAML file '%s':\n%s" % (yamlPath, e)
      raise Exception(msg)
    if 'include' in changes.keys():
      relativeTargetDir = changes['include']['directory']
      currentDir = join(split(yamlPath)[:-1])[0]
      targetDir = join(currentDir, relativeTargetDir)
      try:
        dirFiles = listdir(targetDir)
      except Exception:
        raise Exception('Included directory "' + targetDir + '" does not exist')
      migrationFiles = [
        join(targetDir, f)
        for f in dirFiles
        if f.endswith('.yml')
      ]
      for includedMigration in migrationFiles:
        includeChanges = self.inputYamlToChangeSets(includedMigration)
        changes.update(includeChanges)
      del changes['include']
    return changes


  def update(self):
    print "Running all migrations..."
    self.liquibaseExecutor.run(self.outputXmlChangeLogFilePath, 'update')


  def rollback(self, tagName):
    print "Rolling back to %s..." % (tagName,)
    self.liquibaseExecutor.run(self.outputXmlChangeLogFilePath, 'rollback',
                               tagName)


  def getTags(self):
    return [
      {'tag':self.changes[c]['tag'], 'changeSet': c}
      for c in self.changes.keys()
      if 'tag' in self.changes[c]
    ]

