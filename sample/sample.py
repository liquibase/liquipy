import liquipy

db = liquipy.Database(
  host="localhost", 
  database="test_liquipy", 
  username="root",
  tempDir=".")

db.initialize('changelog.yml')

db.update()