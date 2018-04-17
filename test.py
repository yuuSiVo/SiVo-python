from xml.etree.ElementTree import Element, SubElement, tostring, XML
from xml.etree import ElementTree
from xml.dom import minidom
import xml.etree.ElementTree as ET

root = ET.Element("root")
tree = ET.ElementTree(root)
tree.write("test.xml")