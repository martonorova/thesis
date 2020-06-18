import dicttoxml
import xmltodict
import json
from xml.dom.minidom import parseString
from lxml import etree
from xml.etree import ElementTree as ET
import pprint

# prezentacioban csak 2 attributumu jsonnal

pp = pprint.PrettyPrinter(indent=4)

# old_json = [
#     {'New York': 288.22, 'timestamp': 1592063501770},
#     {'New York': 288.24767617, 'timestamp': 1592067101770},
#     {'New York': 288.326939663, 'timestamp': 1592070701770},
#     {'New York': 288.406203155, 'timestamp': 1592074301770},
#     {'New York': 288.485466648, 'timestamp': 1592077901770}
# ]

old_json = [
    {'New York': 288.22, 'timestamp': 1592063501770},
    {'New York': 288.24767617, 'timestamp': 1592067101770}
]

new_json = {
    "target": "weather_retrieve_process?city=New York",
    "datapoints": [
        [288.22, 1592063501770],
        [288.24767617, 1592067101770],
        [288.326939663, 1592070701770],
        [288.406203155, 1592074301770],
        [288.485466648, 1592077901770]
    ]
}

data = json.dumps(old_json)
pp.pprint(data)

data = json.loads(data)
print("DICT\n")
pp.pprint(data)
print("\n\n")

xml = dicttoxml.dicttoxml(data, attr_type=False)
dom = parseString(xml)
print("XML\n")
print(dom.toprettyxml())

#
# XSLT magic here
#

xslt_root = etree.XML(
    '''<?xml version="1.0" encoding="UTF-8"?>

        <xsl:stylesheet version="1.0"
        xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

        <xsl:template match="/">

            <root>

            <target>weather_retrieve_process</target>

            <xsl:for-each select="root/item">
                <datapoints>
                    <value><xsl:value-of select="New_York"/></value>
                    <value><xsl:value-of select="timestamp"/></value>
                </datapoints>
            </xsl:for-each>

            </root>

        </xsl:template>

        </xsl:stylesheet>'''
)

transform = etree.XSLT(xslt_root)

doc = etree.fromstring(str(xml))
result_xml = transform(doc)

dom = parseString(etree.tostring(result_xml))
print("RESULT XML\n")
print(dom.toprettyxml())

# TODO XPATH-tal a vegso formatum

root = ET.fromstring(etree.tostring(result_xml))
print(root.tag)

print("FOR LOOP")
for i in root:
    print(i.tag)

print("FIND ALL\n")
elements = root.findall("./datapoints/value")

for element in elements:
    print(element.text)

print("\n DATAPOINTS \n")
datapoints = [elements[i:i+2] for i in range(0, len(elements) - 1, 2)]
datapoints = map(lambda datapoint: [float(datapoint[0].text), int(datapoint[1].text)], datapoints)
# for datapoint in datapoints:
#     print([float(datapoint[0].text), int(datapoint[1].text)])
print(datapoints)

target_element = root.findall("./target")[0]
print(target_element.text)

result = {
    "target": target_element.text,
    "datapoints": datapoints
}

# result = json.dumps((xmltodict.parse(etree.tostring(result_xml))), indent=4, separators=(',', ': '))
# result = json.loads(result)
print("\n\nRESULT\n")
print(result)
# pp.pprint(result)
print(type(result))

# print(result['root']['item'][0]['New_York']['item'][0])