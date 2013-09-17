import yaml
import pprint

DEFAULT = {
  'url': "jdbc:mysql://localhost",
  'database': "liquipy_test",
  'username': "root",
  'password': ""
}

class LiquipyDatabase(object):
  """
  Main interface for Liquipy
  """

  def __init__(self, url=DEFAULT['url'],
                     database=DEFAULT['database'],
                     username=DEFAULT['username'],
                     password=DEFAULT['password']):
    self.url = url
    self.database = database
    self.username = username
    self.password = password


  def initialize(self, yamlPath):
    rawYaml = open(yamlPath, 'r').read()
    try:
      changes = yaml.load(rawYaml)
    except yaml.scanner.ScannerError as e:
      msg = "Error parsing input YAML file '%s':\n%s" % (yamlPath, e)
      raise Exception(msg)

    # pprint.pprint(yaml.load(rawYaml))

    changeLog = []

    for changeId in changes.keys():
      change = changes[changeId]
      changeSet = {
        'id': changeId,
        'author': change['author'],
        'sql': change['sql'],
        'rollback': change['rollback'],
        'comment': change['comment']
      }
      changeLog.append({'changeSet': changeSet})

    yamlOut = {'databaseChangelog': changeLog}

    rawYamlOut = yaml.dump(yamlOut)
    print rawYamlOut
    yamlFile = open('/tmp/liquipy.yaml', 'w')
    yamlFile.write(rawYamlOut)
