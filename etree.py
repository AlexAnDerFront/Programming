import xml.etree.ElementTree as ET

xmlfile = "sample.xml"

tree = ET.parse(xmlfile)
root = tree.getroot()

ET.dump(tree)

for elm in root.findall('.'):
    print(elm.tag)