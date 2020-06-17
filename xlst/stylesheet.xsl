<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="/">

<root>

<target>
    weather_retrieve_process
</target>

<xsl:for-each select="root/item">
<datapoints>
    <value><xsl:value-of select="New_York"/></value>
    <value><xsl:value-of select="timestamp"/></value>
</datapoints>
</xsl:for-each>

</root>

</xsl:template>

</xsl:stylesheet>