import yaml
import sys
from os import listdir
from os.path import isfile, join, split

from changeset import XMLWriter as ChangeSetWriter
from executor import Executor as LiquibaseExecutor

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
    self.liquibaseExecutor = LiquibaseExecutor(host, database, username, password)
    self.tempDir = tempDir
    self.outputXmlChangeLogFilePath = self.tempDir + "/liquipy_changelog.xml"



  def initialize(self, yamlPath):
    changes = self.inputYamlToChangeSets(yamlPath)
    changeSetWriter = ChangeSetWriter(self.outputXmlChangeLogFilePath)
    changeSetWriter.write(changes)


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
      targetDir = join(currentDir,relativeTargetDir)
      migrationFiles = [ 
        join(targetDir, f) 
        for f in listdir(targetDir) 
        if f.endswith('.yml')
      ]
      for includedMigration in migrationFiles:
        includeChanges = self.inputYamlToChangeSets(includedMigration)
        changes.update(includeChanges)
      del changes['include']
    return changes


  def update(self):
    self.liquibaseExecutor.run(self.outputXmlChangeLogFilePath, 'update')

