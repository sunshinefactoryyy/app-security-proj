from lib2to3.pgen2.parse import ParseError
import xml.etree.ElementTree as ET
from lxml import etree
from xml.dom import minidom

try:
    parser = etree.XMLParser(load_dtd=True,no_network=False)
    mytree = ET.parse('sample.xml')
except ET.ParseError:
    print("hi")

#ET.dump(mytree.getroot())

"""
parser = etree.XMLParser(load_dtd=True,no_network=False)
mytree = ET.parse("sample.xml",parser=parser)
#print(etree.dump(mytree.getroot()))
"""
root = mytree.getroot()
#print(root[0][0].text)

for i in range(len(root)):
    username = root[i][0].text
    email = root[i][1].text
    password = root[i][2].text
    print(username)
    print(email)
    print(password)

"""
tree = ET.parse('sample.xml')
root = tree.getroot()
print(root[1][0].text)
"""