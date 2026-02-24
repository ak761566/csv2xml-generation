import pprint
import re
import xml.etree.cElementTree as xml
from collections import defaultdict

# BL_IOR_E_1_205.xml:	<ref>BL_IOR_E_1_205_0002.jpg</ref>
# BL_IOR_E_1_205.xml:	<ref>BL_IOR_E_1_205_0003.jpg</ref>
# BL_IOR_E_1_205.xmcrl:	<ref>BL_IOR_E_1_205_0004.jpg</ref>
# BL_IOR_E_1_205.xml:	<ref>BL_IOR_E_1_tup205_0005.jpg</ref>

f = open('C:\\portico-project\\work\\amdigital\\EastIndiaCompany\\updated_refs.txt','r')
of = open('C:\\portico-project\\work\\amdigital\\EastIndiaCompany\\east_india_company5_fileref_mapping.xml', 'wb')

# text = """BL_IOR_E_1_205.xml:	<ref>BL_IOR_E_1_205_0001.jpg</ref>
# BL_IOR_E_1_205.xml:	<ref>BL_IOR_E_1_205_0002.jpg</ref>"""
# lst = []
# for line in re.split('\n', text):
#     l = re.split(':\s', line)
#     lst.append(l)
# ordDict = defaultdict(list)
# for k, v in lst:
#     ordDict[k].append(v)
# for i in ordDict:
#     print(ordDict[i])
lst = []
for l in f.readlines():
    l1 = re.split(':\s', l)
    if len(l1) > 1:
        lst.append(l1)

ordDict = defaultdict(list)

try:
    for k, v in lst:
        ordDict[k].append(v)

    root = xml.Element("fileref_mapping", collection="East India Company")
    for k in ordDict:
        attrib = k
        ref = xml.SubElement(root, "references", imagedirectory=attrib)
        for i in ordDict[k]:
            fileName = re.search(r'\w+\.jpg',i)
            xml.SubElement(ref,'ref').text=fileName.group()

    tree = xml.ElementTree(root)
    xml.indent(tree, space=' ', level=0)
    tree.write(of, encoding="utf-8", xml_declaration=True, )
    # print(ordDict["BL_IOR_E_1_205.xml"])

except Exception as e:
    print(e)


of.close()
f.close()