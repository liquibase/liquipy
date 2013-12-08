#!/usr/bin/env python
import os
import unittest2 as unittest

from mock import patch, ANY, Mock

import liquipy
from liquipy.executor import Executor as LiquibaseExecutor

class LiquipySampleTest(unittest.TestCase):
  def setUp(self):
    self.pathToChangelog = os.path.realpath(os.path.join(
      os.path.dirname(__file__),
      "../../sample/changelog.yml"))
  
  @patch("liquipy.db.LiquibaseExecutor", autospec=LiquibaseExecutor)
  def testSample(self, liquibaseExecutorClassMock):
    """ Simple unit test demonstrating common use, mirroring the bundled sample
    """
    
    liquibaseExecutorMock = liquibaseExecutorClassMock.return_value
    liquibaseExecutorMock.database = Mock()
    
    db = liquipy.Database(
      host="localhost",
      database="test_liquipy",
      username="root")

    db.initialize(self.pathToChangelog)
    
    db.update()

    # Basic assertions on use of liquipy.executor.Executor
    
    self.assertTrue(liquibaseExecutorClassMock.called)
    liquibaseExecutorClassMock.assert_called_once_with(
        "localhost", "test_liquipy", "root", ANY)
    self.assertTrue(liquibaseExecutorClassMock.return_value.run.called)
    liquibaseExecutorClassMock.return_value.run.assert_called_once_with(
        ANY, "update")



if __name__ == '__main__':
  unittest.main()
