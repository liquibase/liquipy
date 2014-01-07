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
from pkg_resources import resource_filename
import subprocess


RUN_TEMPLATE = """java -jar %s \
    --driver=com.mysql.jdbc.Driver \
    --classpath=%s \
    --changeLogFile=%s \
    --url="jdbc:mysql://%s:%s/%s" \
    --username=%s \
    --password=%s \
    --logLevel=info \
"""



g_logger = logging.getLogger("liquipy.executor")



class Executor(object):
  """
  Executes Liquibase.
  """

  def __init__(self, host, port, database, username, password):
    self.host = host
    self.port = port
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
      self.liquibaseJar, self.mysqlJar, changeLogFilePath, self.host, self.port,
      self.database, self.username, self.password)
    cmd = cmd + " ".join(args)

    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT, close_fds=True)
    # Use p.communicate() BEFORE p.wait() to avoid deadlock in case the process
    # spits out more STDERR/STDOUT data than there is room for in the pipe's
    # buffer (which is not that large)
    (output, _stderr) = p.communicate()
    p.wait()

    if p.returncode != 0:
      raise Exception("""

Error running liquibase (returncode=%s)! See output below:

%s
The Liquibase XML changelog file used to perform this operation is here: %s
""" % (p.returncode, output, changeLogFilePath)
      )
    g_logger.info("%s", output)
