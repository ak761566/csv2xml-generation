import csv
import pprint
import xml.etree.ElementTree as ET
import os



''''
This is the script which is being used for the conversion of CSV to XML files.
'''''
# Constants declaration

CSV_FILE_LOCATION = "/Portico-Project/Amdigital/AMER_COMM_AFRICA_I/SETUP-23875/PQ-4838/Copy of Master Audio Import FULL.csv"

CSV_FILE_DATA = open(CSV_FILE_LOCATION,'r', encoding='utf-8')

display_name = 'American Committee on Africa I: Liberation Movements, Solidarity and Activism'

local_output_location = "/Portico-Project/Amdigital/AMER_COMM_AFRICA_I/SETUP-23875/PQ-4838/DataExport-PorticoOffsystemCreated/"

input_spreadsheet_metadata = "Copy_of_Master_Audio_Import_FULL-csv-PTC-"

Generate_PTC_Group_ID = True
folder_name_column_index = 0
ptc_group_id_name = []


# if not Generate_PTC_Group_ID:
#     response = input("Do you want to generate group ID column (Y/N): ")
#     if response == 'Y' or response == 'y':
#         Generate_PTC_Group_ID = True
#         ptc_group_id_name = input("Please enter group id name: ")
#     else:
#         pass

while Generate_PTC_Group_ID:
        response = input("Do you want to generate group ID column (Y/N): ")
        if response == 'Y' or response == 'y':
            #Generate_PTC_Group_ID = True
            response_grp_id = input("Please enter group id name: ")
            ptc_group_id_name.append(response_grp_id)
        else:
            Generate_PTC_Group_ID = False




column_dict ={}

# Functions declarations

def generate_csv_list(csv_file_data):
    csv_file_data_list = []
    for record in csv.reader(csv_file_data, dialect='excel'):
        # csv_file_data_list.extend([record.split(sep=',')])
        csv_file_data_list.extend([record])
   # print(csv_file_data_list[1])
    return csv_file_data_list


#TODO-2 Update and replace junk chars from the header

def generate_column_name(csv_data_list):
    csv_file_header_list = []
    org_csv_file_header_list = []

    header_column_count = 0
    global column_dict

    for header in csv_data_list[0]:
        header_column_count += 1
        org_csv_file_header_list.append(header.replace('ï»¿','').replace('\n','').replace('\ufeff',''))

        if header not in column_dict:
            header = header.replace('ï»¿', '').replace('\n', '').replace('\ufeff', '')
            column_dict[header] = [0, ]
        else:
            dup_col_index = column_dict[header]
            # print(dup_col_index[-1])
            column_dict[header].append(dup_col_index[-1] + 1)


    print(f"Total number of columns are {len(org_csv_file_header_list)}")
    #pprint.pprint(column_dict)
    #pprint.pprint(csv_file_header_list)

    for item in org_csv_file_header_list:
        if column_dict[item][0] == 0:
            csv_file_header_list.append(item)
            if len(column_dict[item]) != 1:
                column_dict[item] = column_dict[item][1:]
        else:
            csv_file_header_list.append(item + "." + str(column_dict[item][0]))
            if len(column_dict[item]) != 1:
                column_dict[item] = column_dict[item][1:]

    #pprint.pprint(csv_file_header_list)

    return csv_file_header_list


def generate_csv_data_dict(data_list, folder_column_index):
    csv_data_dict = {}
    for counter in range(1, len(data_list)):
        # print(csv_data_list[counter][3])
        if data_list[counter][folder_column_index] not in csv_data_dict:
            csv_data_dict[data_list[counter][folder_column_index]] = data_list[counter]
        else:
            csv_data_dict[data_list[counter][folder_column_index] + '-duplicateRow-index-' + str(counter)] = data_list[counter]

    #pprint.pprint(csv_data_dict)
    return csv_data_dict

def generate_labeled_csv_data_dict(unlabeled_data_dict, csv_data_header_list):
    labeled_csv_data_dict = {}
    for csv_data_key in unlabeled_data_dict:
        labeled_csv_data_dict[csv_data_key] = dict(zip(csv_data_header_list, csv_data_dict[csv_data_key]))
        #print(dict(zip(csv_data_header_list, csv_data_dict[csv_data_key])))

    return labeled_csv_data_dict

def generate_amd_data_xml(csv_labeled_data_dict, collection_name, output_location, source_spreadsheet_name):
    records_counter = 0
    output_folder_location = output_location

    if not os.path.exists(output_folder_location):
        os.mkdir(output_folder_location)

    source_csv_file_name = source_spreadsheet_name


    for data_key in csv_labeled_data_dict:
        # print(data_key)
        records_counter += 1
        global ptc_group_id_name

        amd_xml_path_fileName = output_folder_location + source_csv_file_name + data_key + '.xml'
        file_to_write = open(amd_xml_path_fileName, 'wb')

        root = ET.Element('root')
        tree = ET.ElementTree(root)
        row = ET.SubElement(root, 'row')
        collection_name_col = ET.SubElement(row, 'column', attrib=dict((('name', 'ptc-added-collection-name'),)))
        collection_name_col.text = collection_name
        # print(csv_labeled_data_dict[data_key])


        # if Generate_PTC_Group_ID:
        #     global ptc_group_id_name
        #     column_ptc_group_id_1 = ET.SubElement(row, 'column', attrib=dict((('name', 'ptc-group-id-1'),)))
        #     column_ptc_group_id_1.text = ptc_group_id_name

        if len(ptc_group_id_name) > 0:
            grp_index = 1
            for grpName in ptc_group_id_name:
                column_ptc_group_id = ET.SubElement(row, 'column', attrib=dict((('name', f'ptc-group-id-{grp_index}'),)))
                column_ptc_group_id.text = grpName
                grp_index += 1


        for data_label in csv_labeled_data_dict[data_key]:
            if data_label == 'Start Image':
                pass
            elif  data_label == 'End Image':
                pass
            else:
                column = ET.SubElement(row, 'column', attrib=dict((('name', data_label),)))
                column.text = csv_labeled_data_dict[data_key][data_label]

        #ET.dump(root)
        ET.indent(tree, space='', level=0)
        tree.write(file_to_write, encoding='utf-8', xml_declaration=True)

        file_to_write.close()

    print(f"Total number of XML files created : {records_counter} files")




# Functions Calling

csv_data_list = generate_csv_list(CSV_FILE_DATA)

csv_data_header_list = generate_column_name(csv_data_list)
#print(csv_data_header_list)

csv_data_dict = generate_csv_data_dict(csv_data_list, folder_name_column_index)
# print(csv_data_dict['TNA_MH_113_4'])

labeled_data_dict = generate_labeled_csv_data_dict(csv_data_dict, csv_data_header_list)

generate_amd_data_xml(csv_labeled_data_dict=labeled_data_dict, collection_name=display_name , output_location=local_output_location,source_spreadsheet_name=input_spreadsheet_metadata)
