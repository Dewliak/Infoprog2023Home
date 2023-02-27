import datetime
from datetime import datetime

class OutputOperator:
	"""
	A class a fájlba való kiíráshoz megfelelő függvényeket tartalmazza
	"""
	@staticmethod
	def filter_old_events(data):
		return list(filter(lambda date: date[0] > datetime.today(),data))

	@staticmethod
	def format_event_data_to_output(data):
		"""
		Átformázza a DataContainer Event típusát, stringgé, amit kitudunk írni a fájlba
		"""
		def utility_function(event):
			string = event.date.strftime("%d-%m-%Y") + "," + event.start_time.strftime("%H:%M") + "," + event.end_time.strftime("%H:%M") + "," + str(event.description)

			return string
		
		return list(map(utility_function,data))

	@staticmethod
	def format_event_to_output(event):

		string = event.date.strftime("%d-%m-%Y") + "," + event.start_time.strftime("%H:%M") + "," + event.end_time.strftime("%H:%M") + "," + str(event.description)

		return string

	@staticmethod
	def get_date_from_data(data):
		"""
			Létrehoz egy datetime objektumot a dátumból, a napló formátumából
		"""

		date_format = "%d-%m-%Y"
		date = datetime.strptime(data.split(',')[0],date_format)

		return date

