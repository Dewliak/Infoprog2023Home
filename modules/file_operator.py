from modules.output_operator import OutputOperator
from datetime import datetime

import configparser

config = configparser.ConfigParser()
config.read("config/config.ini")

class FileOperator:

	@staticmethod
	def read_file(path):
		
		data = []

		with open(path,'r',encoding = 'utf-8') as file:
			data = file.readlines()

		return data

	@staticmethod
	def write_file(path,data):
		with open(path,'w',encoding = 'utf-8') as file:
			file.writelines(line + "\n" for line in data)


	@staticmethod
	def append_file(path,data):
		with open(path,'a',encoding = 'utf-8') as file:
			file.write(data)
			file.write("\n")


	@staticmethod
	def delete_old_events(path=config["DATA"]['path']):

		with open(path, "r") as f:
			lines = f.readlines()
		with open(path, "w") as f:
			for line in lines:
				if OutputOperator.get_date_from_data(line) >= datetime.today():
					f.write(line)


	@staticmethod
	def delete_empty_lines(path= config["DATA"]["path"]):

		with open(path, "r") as f:
			lines = f.readlines()

		with open(path, "w") as f:
			for line in lines:
				# ha a nagysága 1(\n) vagy 0 akkor az üres sor
				print("Line",len(line),repr(line))
				if len(line) > 1:
					f.write(line)