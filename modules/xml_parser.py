"""
XML parsing helpers using the standard library's ElementTree.

Adjust `parse_xml` to match the actual structure of the XML you're
working with — this is a generic example assuming XML shaped like:

    <items>
        <item>
            <name>Widget</name>
            <price>9.99</price>
            <quantity>10</quantity>
        </item>
        ...
    </items>
"""
import xml.etree.ElementTree as ET


def parse_xml(xml_bytes_or_str):
    """
    Parse raw XML content into a list of flat dicts, one per <item>.

    Args:
        xml_bytes_or_str: raw XML content (bytes or str)

    Returns:
        list[dict]: one dict per <item> element, keyed by child tag name
    """
    root = ET.fromstring(xml_bytes_or_str)

    records = []
    for item in root.findall("item"):
        record = {}
        for child in item:
            record[child.tag] = child.text
        records.append(record)

    return records


def parse_xml_file(path):
    """Convenience wrapper for parsing directly from a file path."""
    with open(path, "rb") as f:
        return parse_xml(f.read())