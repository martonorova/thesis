import dicttoxml
import xmltodict
import json
from xml.dom.minidom import parseString
import pprint

# prezentacioban csak 2 attributumu jsonnal

pp = pprint.PrettyPrinter(indent=4)

old_json = [
    {'New York': 288.22, 'timestamp': 1592063501770},
    {'New York': 288.24767617, 'timestamp': 1592067101770},
    {'New York': 288.326939663, 'timestamp': 1592070701770},
    {'New York': 288.406203155, 'timestamp': 1592074301770},
    {'New York': 288.485466648, 'timestamp': 1592077901770}
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
data = json.loads(data)
print("DICT\n")
pp.pprint(data)
print("\n\n")

xml = dicttoxml.dicttoxml(data, attr_type=False, custom_root='datapoints')
dom = parseString(xml)
print("XML\n")
print(dom.toprettyxml())

result = json.dumps((xmltodict.parse(xml)))
result = json.loads(result)
print("RESULT\n")
pp.pprint(result)