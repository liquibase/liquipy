ROOT_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<databaseChangeLog
        xmlns="http://www.liquibase.org/xml/ns/dbchangelog"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:ext="http://www.liquibase.org/xml/ns/dbchangelog-ext"
        xsi:schemaLocation="http://www.liquibase.org/xml/ns/dbchangelog http://www.liquibase.org/xml/ns/dbchangelog/dbchangelog-3.0.xsd
        http://www.liquibase.org/xml/ns/dbchangelog-ext http://www.liquibase.org/xml/ns/dbchangelog/dbchangelog-ext.xsd">
          %s
</databaseChangeLog>
"""
CHANGESET_TEMPLATE = """
  <changeSet id="%s" author="%s">
    <comment>%s</comment>
    <sql><![CDATA[
%s
    ]]></sql>
    <rollback><![CDATA[
%s
    ]]></rollback>
  </changeSet>
"""
CHANGESET_TAG_TEMPLATE = """
  <changeSet id="%s" author="%s">
      <tagDatabase tag="%s"/>
  </changeSet>
"""

class XMLWriter(object):
  """
  Writes a changeset to XML in the proper format for Liquibase.
  """

  def __init__(self, outputFile):
    self.outputFile = outputFile


  def write(self, changes):
    # data structure to xml
    xmlOut = ""
    for changeSetId in changes.keys():
      changeSet = changes[changeSetId]
      xmlOut += CHANGESET_TEMPLATE % (
        changeSetId, changeSet['author'], changeSet['comment'],
        changeSet['sql'], changeSet['rollback'])
      xmlOut += CHANGESET_TAG_TEMPLATE % (
        "tag_" + str(changeSetId), 
        changeSet['author'], 
        "version_" + str(changeSetId))
    xmlOut = ROOT_TEMPLATE % (xmlOut,)

    outputXmlFile = open(self.outputFile, "w")
    outputXmlFile.write(xmlOut)