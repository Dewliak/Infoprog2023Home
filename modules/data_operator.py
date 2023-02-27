from datetime import datetime
import logging

from modules.event import Event

class DataOperator:

	@staticmethod
	def parse_items(data):
		"""
		data: takes a list as an argument, should be the naplo.txt input

		return Evenet object
		"""

		def utilty_parse_elements(element):
			"""
			Parses the element by the input schema: date,start,end,desc.
			"""
			element = element.split(',')

			#logging.debug(f"Elements: {element}")

			#date
			date_format = "%d-%m-%Y"
			date = datetime.strptime(element[0],date_format)

			time_format = "%H:%M"
			start_time = datetime.strptime(element[1],time_format)
			end_time = datetime.strptime(element[2],time_format)

			description = element[3]

			return Event(date,start_time,end_time,description)


		return list(map(utilty_parse_elements,data))
