import liquipy

db = liquipy.Database(
  host="localhost",
  port="3306",
  database="test_liquipy",
  username="root",
  tempDir=".")

db.initialize('changelog.yml')

db.update()
