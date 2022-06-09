import xml.etree.ElementTree as ET
from lxml import etree
from xml.dom import minidom
"""
parser = etree.XMLParser(load_dtd=True,no_network=False)
mytree = ET.parse('sample.xml')

ET.dump(mytree.getroot())

"""
parser = etree.XMLParser(load_dtd=True,no_network=False)
mytree = ET.parse("sample.xml",parser=parser)
print(etree.dump(mytree.getroot()))

root = mytree.getroot()
print(root[0][0].text)

"""
tree = ET.parse('sample.xml')
root = tree.getroot()
print(root[1][0].text)
"""