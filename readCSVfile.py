import csv
import pprint
import xml.etree.ElementTree as ET


# file = open('C:\\portico-project\\work\\amdigital\\COLCARIBBEAN\\Colonial Caribbean Image Metadata Import.csv', 'r')
file = open('C:\\portico-project\\work\\amdigital\\COLCARIBBEAN\\Colonial Caribbean Section Metadata Import.csv', 'r')
file_out = open('C:\\portico-project\\work\\amdigital\\COLCARIBBEAN\\ColCaribbean_fileref_mapping.xml','wb')

csv_reader = csv.reader(file)

img_grp = {}
next(csv_reader)
for row in csv_reader:
    # if row[1] not in img_grp:

    if row[0] not in img_grp:
        # img_grp[row[1]] = [row[0]]
        # img_grp[row[0]] = [item.strip() for item in row[2].split(sep=';') if item.isspace() == False]
        img_grp[row[0]] = [row[2]]
    else:
        #img_grp[row[1]].append(row[0])
        img_grp[row[0]].append(row[2])
        #img_grp[row[0]].add(item.strip() for item in row[2].split(sep=';'))


for k in img_grp:
    img_grp[k] = [img.split('; ') for img in img_grp[k]]

file.close()
# print(img_grp)
# for k in img_grp.keys():
#     print(k, end=': ')
#     for v in img_grp[k]:
#         print(v, end=' ')
#     print()

# pprint.pprint(img_grp)

root = ET.Element("fileref_mapping", attrib=dict((('collection','Colonial Caribbean'),)))
tree = ET.ElementTree(root)

# refs_elem = ET.SubElement(root, "references", attrib=dict((('imagedirectory',""),)))
for key in img_grp:
    refs_elem = ET.SubElement(root, "references", attrib=dict((('imagedirectory', key),)))
    for val_list in img_grp[key]:
        for val in val_list:
            ref_elem = ET.SubElement(refs_elem, "ref")
            ref_elem.text = val

ET.indent(root,space=' ',level=0)
ET.dump(root)


tree.write(file_out , xml_declaration=True, encoding="utf-8")

file_out.close()
