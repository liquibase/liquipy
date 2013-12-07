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

from subprocess import Popen, PIPE, STDOUT
from pkg_resources import resource_filename

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
    self.liquibaseJar = resource_filename(
      __package__, "externals/liquibase.jar")
    self.mysqlJar = resource_filename(
      __package__,
      "externals/mysql-connector-java-5.1.17-bin.jar")


  def run(self, changeLogFilePath, *args):
    cmd = RUN_TEMPLATE % (
      self.liquibaseJar, self.mysqlJar, changeLogFilePath, self.host,
      self.database, self.username, self.password)
    cmd = cmd + " ".join(args)
    # print("\n" + cmd + "\n")

    p = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT, close_fds=True)
    # TODO Need to use p.communicate() BEFORE p.wait() to avoid deadlock in case
    #   the process spits out more STDERR/STDOUT data than there is room for in
    #   the pipe's buffer (which is not that large)
    p.wait()
    output = p.stdout.read()

    if p.returncode != 0:
      raise Exception("""

Error running liquibase! See output below:

%s
The Liquibase XML changelog file used to perform this operation is here: %s
""" % (output, changeLogFilePath)
      )
    print output
