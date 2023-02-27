from datetime import datetime

class Event:
	def __init__(self,date:datetime,start_time: datetime,end_time: datetime,description: int):
		"""
		
		date: Az esemény dátuma: nap,hónap,év forma - lehetséges formái(20. 01. 2023,20-1-2023,20. jan 2023, 20. január 2023.) - külön modul ellenözri 
			- fontos dolgok, dátum ellenörzése (érvényese szökőév miatt)

		start_time : kezdő idő
		end_time : végző idő

		---FONTOS: start_time < end_time---

		description: az esemény leírása max 250 karakter

		"""
		self.date = date
		self.start_time = start_time
		self.end_time = end_time
		self.description = description



	def check_time(self):
		if self.start_time <= self.end_time:
			return True
		else:
			return False



