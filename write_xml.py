# encoding: utf-8
#

from xml.etree.ElementTree import Element, SubElement, tostring, XML
from xml.etree import ElementTree
from xml.dom import minidom

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

top = Element('top')

parent_a = SubElement(top, 'parent', id='')
parent_b = SubElement(top, 'parent', id='B')

# 子を作成する
children = XML('''<root><child num="0" /><child num="1" /><child num="2" /></root> ''')

# 重複を分かり易くするためにノードの Python オブジェクト id に id をセットする
for c in children:
    c.set('id', str(id(c)))

# 最初の親に追加する
parent_a.extend(children)

print ('A:')
print (prettify(top))
print

# 2番目の親にノードをコピーする
parent_b.extend(children)

print ('B:')
print (prettify(top))
print