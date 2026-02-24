import csv
import pprint
import shutil
from imaplib import IMAP4
import os

# TODO: read CSV File

SRC_File_Path = 'C:\\Portico-Project\\SAE Standards\\SETUP-21241\\PQ-3844_SAE E-Standards_MissingMetadataFileReport_1521-Batches.csv'

src_file = open(SRC_File_Path,'r')

csv_file = csv.reader(src_file,skipinitialspace=True)

next(csv_file)

batch_name = []
file_name = []

for row in csv_file:
    batch_name.append(row[0])
    file_name.append(row[1])

#print(batch_name)
#print(file_name)
ingest_path = '/pcontent/ongoing/journal_content/INGEST_MASTER/_eStandards/SAE/Fetched/Standards/NEW/'

folder_list = [item.replace(ingest_path,'').split(sep='/') for item in file_name]

#print(folder_list[0])

folder_dict ={}

for lst in folder_list:
    if len(lst) > 1:
        if lst[0] not in folder_dict:
            folder_dict[lst[0]] = [lst[2]] ## Folder Name
            # folder_dict[lst[0]] = [lst[-1].split('.')[0]] ## File name without extension
        else:
            folder_dict[lst[0]].append(lst[2]) ## Folder Name
            #folder_dict[lst[0]].append(lst[-1].split('.')[0]) ## File name without extension

#pprint.pprint(folder_dict)

folder_location = 'C:\\Portico-Project\\SAE Standards\\SETUP-21241\\PQ-3844-Python-Generated-Folder-Structure\\'

if os.path.exists(folder_location):
    pass
else:
    os.mkdir(folder_location)

#supplied_files_folder_location = 'C:\\Portico-Project\\SAE Standards\\SETUP-21241\\SAE_Standards_-_Missing_Metadata\\'
# supplied_files_folder_location = 'C:\\Portico-Project\\SAE Standards\\SETUP-21241\\PQ-3844-Python-Generated-XML\\'
supplied_files_folder_location = 'C:\\Portico-Project\\SAE Standards\\SETUP-21241\\ALL-XML-For_Python_Process\\'
supplied_files_prefix = "PQ-3844_Standards_NO_XML-XLSX-PTC-"

file_copied_counter = 0
file_not_copied_counter = 0

for key in folder_dict:
    dest_folder = folder_location + key + '\\'
    print(dest_folder)
    if not os.path.exists(dest_folder):
        os.mkdir(dest_folder)
    for v in folder_dict[key]:
        key_sub_folder = dest_folder + '\\' + v
        if not os.path.exists(key_sub_folder):
            #os.mkdir(key_sub_folder)
            #print(key_sub_folder)
            pass
        if os.path.exists(supplied_files_folder_location + v + '.xml'):
            src_file = supplied_files_folder_location + v + '.xml'
            #shutil.copy(src_file,key_sub_folder)
            shutil.copy(src_file,dest_folder)
            file_copied_counter +=1
        elif os.path.exists(supplied_files_folder_location + supplied_files_prefix + v + '.xml'):
            src_file = supplied_files_folder_location + supplied_files_prefix + v + '.xml'
            #shutil.copy(src_file, key_sub_folder)
            shutil.copy(src_file, dest_folder)
            file_copied_counter += 1
        else:
            print(f"File not present : {v + '.xml'} check supplied files or supplied excel metadata")

            file_not_copied_counter += 1

    key_folder=''

print(f"Number of files copied from {supplied_files_folder_location} are {file_copied_counter}")
print(f"Number of files not copied {file_not_copied_counter}")