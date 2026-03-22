import csv
import os.path

import pandas as pd
import pprint
import xml.etree.ElementTree as ET
import tkinter

#TO DO: Convert CSV file each row into separate XML file
#

class Csv2xml:
    def __init__(self, collection_name : str, csv_file_location : str, folder_nam_col_index: int, group_id : str,
                 window : tkinter, canvas : tkinter, run_btn: tkinter, quit_btn: tkinter):
        self.collection_name = collection_name
        self.csv_file_location = csv_file_location
        self.window = window
        self.canvas = canvas
        self.run_btn = run_btn
        self.quit_btn = quit_btn

        self.metadata_file_name = (os.path.basename(csv_file_location).replace(' ', '_')
                                   .replace('.','-')) + "-PTC-"
        self.input_folder_name = os.path.dirname(csv_file_location)
        self.out_file_directory = (self.input_folder_name.replace('C:', '').replace('\\','/')
                                   + "/" + "DataExport-PorticoOffsystemCreated")

        self.folder_nam_col_index =  folder_nam_col_index
        self.group_id = group_id

        self.file_path_token_list = self.csv_file_location.split('\\')

        if not os.path.exists(self.out_file_directory):
            os.mkdir(self.out_file_directory)


    def read_supplied_csv(self):
        # Iterate over every row
        # generate XML file for each row.
        # name of the xml file correspond to the image folder name

        self.canvas.insert(tkinter.END, "Processing initiated..\n")
        self.run_btn.config(state=tkinter.DISABLED)
        self.quit_btn.config(state=tkinter.DISABLED)
        self.window.update()

        dataFrame = pd.read_csv(self.csv_file_location)

        self.canvas.insert(tkinter.END, f"Input CSV: {os.path.basename(self.csv_file_location)}\n"
                                                      f"Number of Rows: {dataFrame.shape[0]}\n"
                                                    f"Number of Columns:{dataFrame.shape[1]}\n\n")
        #print(dataFrame.dtypes)
        #print(dataFrame.shape)
        counter = 0
        for row in dataFrame.iterrows():
            counter += 1
            root_elem = ET.Element("root")
            tree = ET.ElementTree(root_elem)
            row_elem = ET.SubElement(root_elem, "row")
            collection_name_column = ET.SubElement(row_elem, "column", attrib=dict((("name", "ptc-added-collection-name"),)))
            collection_name_column.text = self.collection_name

            if self.group_id:
                group_id_list = [item for item in self.group_id.split(',')]

                for item in group_id_list:
                    group_id_elem = ET.SubElement(row_elem, "column", attrib=dict((("name","ptc-group-id"),)))
                    group_id_elem.text = item.rstrip().lstrip()


            for col in row:
                if isinstance(col, int):
                    pass
                else:
                    file_name = col.iloc[self.folder_nam_col_index]
                    #print(file_name)
                    payload = self.out_file_directory + '/' + self.metadata_file_name + file_name + ".xml"
                    result_file = open(payload, 'wb')
                   #print(out_file_name_loc)
                    for index, value in (col.items()):
                        #print(f"{index}-{value}")
                        column = ET.SubElement(row_elem, "column", attrib=dict((("name", index.__str__()),)))
                        if str(value) == 'nan':
                            pass
                        else:
                            column.text = str(value)

            ET.indent(tree, space="  ", level=0)
            tree.write(result_file, encoding="utf-8", xml_declaration=True, method="xml")
            #ET.dump(root_elem)
            result_file.close()

        self.run_btn.config(state=tkinter.ACTIVE)
        self.quit_btn.config(state=tkinter.ACTIVE)

        self.canvas.insert(tkinter.END, "Processing is completed..\n")
        self.canvas.insert(tkinter.END, f"XML files: {counter}.\n"
                                        f"Output folder: {os.path.dirname(self.csv_file_location) 
                                                          + "\\DataExport-PorticoOffsystem"}.")

