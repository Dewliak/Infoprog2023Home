import collections
import logging
from datetime import datetime

from modules.event import Event
from modules.file_operator import FileOperator
from modules.output_operator import OutputOperator

import configparser

config = configparser.ConfigParser()
config.read("config/config.ini")


class DataContainer:
	def __init__(self):
		"""
		Szótár formában tároljuk az adatokat, azonbelül pedig az eseményeket egy
		szortírozott listában tároljuk

		"""
		#items in the container are Event objects
		self.date_data = collections.defaultdict(list) # store data by date, if not found create an empty list in itself stores sorted list


	def binary_search(self, search, array):
		"""
		A bináris keresést beszúráskor használjuk, mivel a lista már rendezett, így
		gyorsabb lesz a beszúrása.Kereséskor itt azt is figyelembe kell venni,
		hogy nem lesz olyan időpont, amit keresünk, mivel akkor nem lenne érvényes az
		adott időpont, így alulról határoljuk be a keresést.
		"""
		left = 0
		right = len(array) - 1
		target = -1

		if(len(array) == 0):
			return 0

		while(left <= right):

			mid  = (left + right) // 2

			if(array[mid].start_time == search.start_time):
				return mid
			if(array[mid].start_time < search.start_time):
				left = mid + 1
				target = mid # A keresett az adott időpont lehető legközelebb lévő kisebb időpont indexe

			else:
				right = mid - 1

		return target

	def sort_all(self):
		"""
		Minden dátumra szortírozza a bennelévő eseményeket
		"""
		for key in self.date_data.keys():
			self.date_data[key].sort(key = lambda x: x.start_time)


	def insert(self,event):

		self.date_data[event.date].append(event)

	def insert_binary(self,event:Event):
		"""
		Amikor csak egy-egy új eseményt szúrunk be, gyorsabb ezzel a módszerrel, mint újraszorszítrozni
		"""
		self.date_data[event.date].insert(self.binary_search(event,self.date_data[event.date]) + 1, event)

	def insert_new(self,event:Event):
		"""
		Az adatstruktúrán kívül a fájlhoz is hozzáadja
		"""
		self.insert_binary(event)
		self.insert_new_add_file(event)

	def insert_new_add_file(self,event:Event,path = config["DATA"]["path"]):

		if self.search_if_start_time_is_free(event) and event.check_time():
			self.insert(event)
			FileOperator.append_file(path=path, data = OutputOperator.format_event_to_output(event))
			logging.info("Successfully added the file")
		else:
			logging.error("Start time is in use, or the format is bad")

	def get_all_data(self):
		return self.date_data


	def delete_old_events(self):
		"""
		Kitörli a régi dátumokat
		"""
		old = []
		for event in self.date_data.keys():
			print(event)
			if event < datetime.today():
				old.append(event)

		for event in old:
			self.date_data.pop(event)

	def get_specific_date_data(self,date):
		return self.date_data[date]


	def get_data_sorted_by_date(self):
		"""visszaad egy listát, amelyben tuplek vannak pl.: [(key1, item1),(key2,item2),...] """
		return sorted(self.date_data.items())

	def search_if_start_time_is_free(self,event:Event):
		"""
		Leellenörzi, hogy az adott időpont szabad-e
		"""
		specific_day = self.get_specific_date_data(event.date)
		
		for e in specific_day:
			if(e.start_time == event.start_time):
				return False

		return True

	def __repr__(self):
		return self.date_data		
