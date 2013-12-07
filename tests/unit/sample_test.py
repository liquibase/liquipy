#!/usr/bin/env python
import os
import unittest2 as unittest

from mock import patch, ANY

import liquipy
from liquipy.executor import Executor as LiquibaseExecutor

class LiquipySampleTest(unittest.TestCase):
  def setUp(self):
    self.pathToChangelog = os.path.realpath(os.path.join(
      os.path.dirname(__file__), 
      "../../sample/changelog.yml"))
  
  @patch("liquipy.db.LiquibaseExecutor", autospec=LiquibaseExecutor)
  def testSample(self, LiquibaseExecutorMock):
    """ Simple unit test demonstrating common use, mirroring the bundled sample 
    """
    
    db = liquipy.Database(
      host="localhost", 
      database="test_liquipy", 
      username="root",
      tempDir=".")

    db.initialize(self.pathToChangelog)
    
    db.update()

    # Basic assertions on use of liquipy.executor.Executor 
    
    self.assertTrue(LiquibaseExecutorMock.called)
    LiquibaseExecutorMock.assert_called_once_with(
        "localhost", "test_liquipy", "root", ANY)
    self.assertTrue(LiquibaseExecutorMock.return_value.run.called)
    LiquibaseExecutorMock.return_value.run.assert_called_once_with(
        ANY, "update")



if __name__ == '__main__':
  unittest.main()
