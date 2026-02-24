import csv
import pprint
import xml.etree.ElementTree as ET
import os.path as path
import os as os


# CSV_FILE_PATH = 'C:\\portico-project\\work\\amdigital\\Transform_Shopping\\Shopping import.csv'
# CSV_FILE_PATH = 'C:\\portico-project\\work\\amdigital\\EastIndiaCompany\\PQ-4338\\AMD East India V Missing Metadata.csv'
CSV_FILE_PATH = 'C:\\portico-project\\work\\amdigital\\MEXICO_IN_HISTORY\\Mexico in History_asset metadata_October 2024.csv'




source_csv_file = open(CSV_FILE_PATH, 'r', encoding='utf-8')

# dict_reader = csv.DictReader(source_csv_file,  dialect='excel')
dict_reader = csv.reader(source_csv_file,  dialect='excel')
# pprint.pprint(next(dict_reader))

header_row = next(dict_reader)
# pprint.pprint(header_row)

ddup_head_row = []
counter = 0

header_row = [item.replace('(','').replace(')','') for item in header_row]

# print(header_row)

for head in header_row:
    # print(head)
    if head == '﻿Quartex Name':
        ddup_head_row.append('Image Directory(Quartex Name)')
    elif head in ddup_head_row:
        counter += 1
        ddup_head_row.append(head + "." + str(counter))
    else:
        ddup_head_row.append(head)
    counter = 0

# pprint.pprint(ddup_head_row)

# print(next(dict_reader))

dict_metadata ={}

for item in dict_reader:
    # print(type(item))
    dict_metadata[item[0]] = dict(zip(ddup_head_row, item))

    # pprint.pprint(dict_all_metadata['\ufeffQuartex Name'])

# for key in dict_metadata:
#     print(key,':', dict_metadata[key])

# out_path = "C:\\portico-project\\work\\amdigital\\Transform_Shopping\\DataExport-PorticoOffsystemCreated"
# out_path = "C:\\portico-project\\work\\amdigital\\EastIndiaCompany\\PQ-4338\\DataExport-PorticoOffsystemCreated"
out_path = "C:\\portico-project\\work\\amdigital\\MEXICO_IN_HISTORY\\DataExport-PorticoOffsystemCreated\\"

if os.path.exists(out_path):
    pass
else:
    os.mkdir(out_path)

input_data_dir = out_path + '\\'

for key in dict_metadata:
    # Coll_name = 'Transform-shopping-Document-Shopping-import-csv-PTC-'
    # Coll_name = 'amd-eastindiacompany-missingmetadata-csv-PTC-'
    Coll_name = 'Transform-Mexico-In-History-import-csv-PTC-'
    collection_name = 'Mexico-In-History'

    file_name = Coll_name + key + '.xml'
    xml_out = open(path.join(input_data_dir, file_name), 'wb')
    # pprint.pprint(path.join(input_data_dir, file_name))
    root = ET.Element("root")
    Tree = ET.ElementTree(root)
    row = ET.SubElement(root, "row")
    ET.indent(root,space=' ', level=0)
    column = ET.SubElement(row, "column", attrib=dict((("name", "ptc-added-collection-name"),)))
    # column.text = "Transform_Shopping"
    # column.text = "East India Company V"
    column.text = collection_name

    for key_val in dict_metadata[key]:
        # out = key_val + ':' + dict_metadata[key][key_val]
        # pprint.pprint(out)
        sub_col = ET.SubElement(row, "column", attrib=dict((("name", key_val),)))
        sub_col.text = dict_metadata[key][key_val]
    ET.dump(root)
    ET.indent(Tree,space=' ', level=0)
    Tree.write(xml_out, xml_declaration=True, encoding='utf-8')
    xml_out.close()

source_csv_file.close()