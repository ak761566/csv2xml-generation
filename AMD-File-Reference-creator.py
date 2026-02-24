import pprint
import re
import xml.etree.ElementTree as ET

from soupsieve.util import lower

# Open CSV File and store data in a variable
CSV_FILE = "/Portico-Project/Amdigital/LAT_AM_HIST_US/reference/Latin_American_Histories_in_the_United_States_section_export_2025_10_23_08_44_27.csv"
CSV_Rows = open(CSV_FILE, 'r')

# Output file
XML_FILE = "/Portico-Project/Amdigital/LAT_AM_HIST_US/reference/Latin_American_Histories_in_the_United_States-mapping.xml"
output_file_location = open(XML_FILE,'wb')

# Collection Name
Collection_Name = 'Latin American Histories in the United States'

def update_folder_name_column(csv_file):
    '''This function will add folder name in the first column, if it is not provided. It will get the folder name from
    previous records and use it in those records where it is missing. Records should be continuous otherwise this function
    will not work.'''
    next(csv_file)
    csv_records_list = []
    folder_name = ''
    for row in CSV_Rows:
        temp_list = []
        temp_list.extend(row.replace('\n','').replace('\t',',').replace('|', ',').split(sep=','))
        if temp_list[0] != '':
            folder_name = temp_list[0]
        elif temp_list[0] == '':
            temp_list[0] = folder_name

        csv_records_list.append(temp_list)
        #print(temp_list)
    return csv_records_list


#Expand File references
def expand_start_end_ref(records_list):
    '''This function will expand the start and end references.'''
    expanded_ref_csv_records = []
    #print(records_list)

    for records in records_list:
        #print(records)
        temp_list = []
        if len(records) == 2:
            expanded_ref_csv_records.append(records)
            # print(expanded_ref_csv_records)
        else:
            if records[1] == '':
                pass
            elif records[1].endswith('_R'):
                folder_name = records[0] + '_'
                start_index = int(records[1].replace('_R', '').replace(folder_name, ''))
                # print(start_index)
                if records[2] == '':
                    end_index = int(records[1].replace('_R', '').replace(folder_name, ''))
                    # print(end_index)
                else:
                    end_index = int(records[2].replace('_L', '').replace(folder_name, ''))
                    # print(end_index)
                    # example 0/P [BL_IOR_F_4_1326, [BL_IOR_F_4_1326_0001_R, BL_IOR_F_4_1326_0001_L]]

                temp_list.extend([records[0], [f"{folder_name}{'{:0>4}'.format(str(item))}{'_R'}"
                                               for item in range(start_index, end_index)]
                                  + [f"{folder_name}{'{:0>4}'.format(str(item))}{'_L'}"
                                     for item in range(start_index, end_index)]
                                  ])

                #print(temp_list)
                expanded_ref_csv_records.append(temp_list)
            elif len(records) > 3:
                temp_list.extend([records[0], [records[index] for index in range(1, len(records)) ]])
                #print(temp_list)
                expanded_ref_csv_records.append(temp_list)
            else:
                folder_name = records[0] + '_'
                try:
                    start_index = int(records[1].replace(folder_name, '', -1))
                    # print(records[0] + ' ', records[2].replace(folder_name,'',-1))
                    end_index = ''
                    if records[2] == '':
                        end_index = int(records[1].replace(folder_name, '', -1)) + 1
                    else:
                        end_index = int(records[2].replace(folder_name, '', -1)) + 1

                    temp_list.extend([records[0], [str(f"{folder_name}{'{:0>4}'.format(str(item))}") for item in
                                                   range(start_index, end_index)]])

                except ValueError:
                    lower_alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
                                   'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

                    rec1_num_value = re.sub('[a-z]', '', records[1].replace(folder_name, '', -1))

                    start_alphabet = lower_alpha.index(re.sub('[0-9]', '', records[1].replace(folder_name, '', -1)))
                    # print(lower_alpha[start_alphabet])
                    if records[2] == '':
                        end_alphabet = lower_alpha.index(re.sub('[0-9]', '', records[1].replace(folder_name, '', -1)))
                    else:
                        end_alphabet = lower_alpha.index(re.sub('[0-9]', '', records[2].replace(folder_name, '', -1)))

                    # print(lower_alpha[end_alphabet])

                    temp_list.extend([records[0], [f"{folder_name}{rec1_num_value}{lower_alpha[item]}" for item in
                                                   range(start_alphabet, end_alphabet + 1)]])

                expanded_ref_csv_records.append(temp_list)
                # print(temp_list)

    return expanded_ref_csv_records


# print(new_expandedRef_list[0])


def generate_ref_dict(expandedref_list):
    '''This will generate dictionary of references provided in the list data structure.'''
    ref_list_dict = {}
    print("***************************")
    print(expandedref_list)

    for ref_list in expandedref_list:
        # print(ref_list[1])
        if ref_list[0] not in ref_list_dict:
            if isinstance(ref_list[1], list):
                ref_list_dict[ref_list[0]] = ref_list[1]
            else:
                ref_list_dict[ref_list[0]] = [ref_list[1]]
            #print(ref_list_dict)
        else:
            if isinstance(ref_list[1], list):
                ref_list_dict[ref_list[0]].extend(ref_list[1])
            else:
                ref_list_dict[ref_list[0]].append(ref_list[1])


    return ref_list_dict


#pprint.pprint(ref_dict['BL_IOR_F_4_1011'])
def create_fileref_mapping_xml(references_dictionary, collection_name, file_output_location):
    '''This function will generate file ref mapping xml file'''
    folder_count = 0
    ref_count = 0
    root = ET.Element('fileref_mapping',attrib=dict((('collection',collection_name),)))
    tree = ET.ElementTree(root)

    for folder_name in references_dictionary:
        folder_count += 1
        references = ET.SubElement(root,'references',attrib=dict((('imagedirectory',folder_name),)))
        for image_name in  ref_dict[folder_name]:
            ref_count += 1
            ref = ET.SubElement(references,'ref')
            ref.text = image_name
    #ET.dump(root)
    ET.indent(tree,space='',level=0)
    tree.write(file_output_location,encoding="utf-8",xml_declaration=True)
    print(f"Mapping file generated...output location {file_output_location.name} and Total number of Articles {folder_count} and total number of references {ref_count}.")
    CSV_Rows.close()
    output_file_location.close()


new_csv_records_list = update_folder_name_column(CSV_Rows)
#print(new_csv_records_list)

new_expandedRef_list = expand_start_end_ref(new_csv_records_list)
#print(new_expandedRef_list)

ref_dict = generate_ref_dict(new_expandedRef_list)
#pprint.pprint(ref_dict)

create_fileref_mapping_xml(ref_dict,Collection_Name, output_file_location)