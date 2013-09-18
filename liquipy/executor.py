from subprocess import call
from pkg_resources import Requirement, resource_filename

RUN_TEMPLATE = """java -jar %s \
    --driver=com.mysql.jdbc.Driver \
    --classpath=%s \
    --changeLogFile=%s \
    --url="jdbc:mysql://%s/%s" \
    --username=%s \
    --password=%s \
    --logLevel=info \
"""


class Executor(object):
  """
  Executes Liquibase.
  """

  def __init__(self, host, database, username, password):
    self.host = host
    self.database = database
    self.username = username
    self.password = password
    self.liquibaseJar = resource_filename(Requirement.parse('liquipy'), 'externals/liquibase.jar')
    self.mysqlJar = resource_filename(Requirement.parse('liquipy'), 'externals/mysql-connector-java-5.1.17-bin.jar')


  def run(self, changeLogFilePath, *args):
    cmd = RUN_TEMPLATE % (
      self.liquibaseJar, self.mysqlJar, changeLogFilePath, self.host, self.database, self.username, self.password)
    cmd = cmd + ' '.join(args)
    # print('\n' + cmd + '\n')
    call(cmd, shell=True)
