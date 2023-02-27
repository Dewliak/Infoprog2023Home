from datetime import datetime
import collections

from modules.setup_logger import logger
from modules.event import Event
from modules.datacontainer import DataContainer
from modules.file_operator import FileOperator
from modules.data_operator import DataOperator


import modules.gui as gui
import tkinter as tk
from tkinter import ttk

from generator import generate_random

import configparser


def main():
	config = configparser.ConfigParser()
	config.read("config/config.ini")

	container = DataContainer()

	input_data = FileOperator.read_file(config["DATA"]["path"])
	input_data = DataOperator.parse_items(input_data)

	for data in input_data:
		container.insert(data)

	container.sort_all()

	print(container.date_data[datetime(2019, 5, 10, 0, 0)])
	x = container.get_data_sorted_by_date()

	for i in x:
		for j in i[1]:
			print(j)
	random_event = Event(datetime(2023,2,28,0,0),datetime(1900,1,1,13,00),datetime(1900,1,1,15,00),"test input")
	print(random_event.date)
	print(container.search_if_start_time_is_free(random_event))
	container.insert_new_add_file(random_event)


	used_format = []
	for date in container.date_data.items():
		if type(date[0]) not in used_format:
			used_format.append(type(date[0]))

	print(used_format)
	root = tk.Tk()

	ttk.Style().theme_use('clam')
	manager = gui.Manager(root, container)
	root.resizable(width=False, height=False)
	root.geometry('{}x{}'.format(900,560))
	main_app = gui.MainApplication(root,manager,container)
	manager.gui = main_app

	main_app.pack(side="top", fill="both", expand=True)
	#manager.delete_old_dates()

	used_format = []
	for date in container.date_data.items():
		if type(date[0]) not in used_format:
			used_format.append(type(date[0]))

	print("FORMATS: ", used_format)

	root.mainloop()

	#FileOperator.delete_old_events("naplo.txt")


if __name__ == "__main__":
	#logging.basicConfig(level=logging.DEBUG)
	main()
