from json import JSONDecodeError
from tkinter import *
from csv2xml import Csv2xml
import json


class Ui:
    def __init__(self):
        self.window = Tk()
        self.window.title("Ithaka Amdigital Project")
        self.window.minsize(width=600, height=300)
        self.window.resizable(width=False, height=False)
        self.window.config(padx=100, pady=50)
        self.error_log_list = []

        self.frm_1 = Frame(self.window)
        self.frm_1.grid(row=0, column=0, pady=10)

        self.lbl_collection_name = Label(self.frm_1 , text="Collection Name: ")
        self.lbl_collection_name.grid(row=0, column=0, padx=5, pady=5)
        self.entry_collection_name = Entry(self.frm_1, width=100)
        self.entry_collection_name.grid(row=0, column=1, pady=5)

        self.lbl_input_file_path = Label(self.frm_1, text="CSV File Path: ")
        self.lbl_input_file_path.grid(row=1, column=0, padx=5, pady=5)
        self.entry_file_path = Entry(self.frm_1 , width=100)
        self.entry_file_path.grid(row=1, column=1, pady=5)

        self.lbl_group_id = Label(self.frm_1, text="Group Id (use comma to separate multiple value): ")
        self.lbl_group_id.grid(row=2, column=0, padx=5, pady=5)
        self.entry_group_id = Entry(self.frm_1, width=100)
        self.entry_group_id.grid(row=2, column=1, pady=5)

        self.frm_2 = Frame(self.window)
        self.frm_2.grid(row=1, column=0, padx=40)

        self.lbl_file_name_col_index = Label(self.frm_2 , text="CSV column Index (for File Name): ")
        self.lbl_file_name_col_index.grid(row=0, column=0, sticky=W)
        self.entry_file_name_col_index = Entry(self.frm_2 , width=10)
        self.entry_file_name_col_index.grid(row=0, column=1, padx=0, pady=10) # use sticky attribute to align
                                                # widget "w" (west/left), "e" (east/right), "n" (north/top),
                                    # "s" (south/bottom), or combinations like "ew" to stretch horizontally.

        self.btn_run = Button(self.frm_2, text="Run", width=10, command=self.execute_split)
        self.btn_run.grid(row=0, column=2, padx=10, pady=10)


        self.btn_quit = Button(self.frm_2, text="Quit", width=10, command=self.exit_application)
        self.btn_quit.grid(row=0, column=3, padx=10, pady=10)

        self.log_text = Text(self.frm_2, height=10)
        self.log_text.grid(row=1, column=0, rowspan=3, columnspan=4)




        self.on_load()
        self.window.mainloop()

    def on_load(self):
        try:
            with open("input_fields.json", "r") as param_file:
                jsom_data = json.load(param_file)
                #print(jsom_data)
                self.entry_collection_name.insert(0, jsom_data["collection_name"])
                self.entry_file_path.insert(0, jsom_data["csv_file_location"])
                self.entry_group_id.insert(0, jsom_data["group_id"])
                self.entry_file_name_col_index.insert(0, jsom_data["folder_name_column_index"])
        except JSONDecodeError as error:
            pass

    def validate_coll_name(self):
        collection_name = self.entry_collection_name.get()
        if collection_name:
            return True
        else:
            self.error_log_list.append("Collection name is required...")
            return False


    def validate_file_path(self):
        file_path = self.entry_file_path.get()
        if file_path:
            return True
        else:
            self.error_log_list.append("Source metadata file path is required....")
            return False

    def validate_file_name_col_index(self):
        col_index = self.entry_file_name_col_index.get()
        if col_index.isnumeric():
            return True
        else:
            return False

    def validate_grp_id(self):
        group_id  = self.entry_group_id.get()
        if group_id:
            return True
        else:
            return False


    def execute_split(self):
        self.error_log_list.clear()

        collection_name_validation = self.validate_coll_name()
        file_path_validation = self.validate_file_path()
        file_name_col_index_validation = self.validate_file_name_col_index()

        collection_name = self.entry_collection_name.get().rstrip().lstrip()

        csv_file_location = self.entry_file_path.get().rstrip().lstrip()
        group_id = self.entry_group_id.get().rstrip().lstrip()

        folder_name_col_index = self.entry_file_name_col_index.get().rstrip().lstrip()

        #print(self.error_log_list)

        if collection_name_validation and file_path_validation and file_name_col_index_validation:

            #create json file to write user entries data to avoid retyping

            with open("input_fields.json", "w") as param_file:
                data = {
                    "collection_name" : collection_name,
                    "csv_file_location" : csv_file_location,
                    "group_id" : group_id,
                    "folder_name_column_index": folder_name_col_index
                }
                json.dump(data, param_file, indent=4)



            csv2xml = Csv2xml(collection_name=collection_name, csv_file_location=csv_file_location,
                           folder_nam_col_index=int(folder_name_col_index), group_id=group_id, window=self.window,
                              canvas=self.log_text, run_btn=self.btn_run, quit_btn=self.btn_quit)

            #self.window.update()
            # self.btn_run.config(state=DISABLED)
            # self.btn_quit.config(state=DISABLED)
            csv2xml.read_supplied_csv()
        else:
            self.log_text.insert(END, f"{self.error_log_list[0]}\n{self.error_log_list[1]}")




    def exit_application(self):
        self.window.quit()

new_ui = Ui()








# default_font = ("Sarif", 15, "bold")
# script_dir = os.path.dirname(os.path.abspath(__file__))
# image_file_path = os.path.join(script_dir,"tomato.png")
#
# #print(image_file_path)
# window = Tk()
# window.title("My first GUI programme.")
# #window.minsize(width=600, height=300)
# window.config(padx=100, pady=50, bg="yellow")
#
# my_label = Label(text="My label", font=default_font)
# my_label.pack()
#
# def change_lbl():
#     my_label.config(text=input.get())
#     input.delete(0, END)
#
# my_button = Button(text="Click Me", command=change_lbl, font=default_font)
# my_button.pack()
#
# input = Entry(width=40)
# input.pack()
#
# text = Text(height=5, width=30)
# text.pack()
#
# canvas = Canvas(height=400, width=400, bg="yellow")
#
# tomato_image =  PhotoImage(file=image_file_path)
# canvas.create_image(200, 200, image=tomato_image)
# canvas.create_text(200,250, text="00:00", fill="white", font=("serif", 20, "bold"))
# canvas.pack()
#
#
#
# window.mainloop()