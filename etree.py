import xml.etree.ElementTree as ET

xmlfile = "countries.xml"

tree = ET.parse(xmlfile)
root = tree.getroot()

# ET.dump(tree)

for elm in root.findall('./country[@name="Panama"]/neighbor[@direction="W"]'):
    print(elm.attrib)            # use text , attributes, tag, etc. to access the element's data


