from datetime import datetime
import math
from modules.data_operator import DataOperator
from modules.file_operator import FileOperator

"""
Segéd függvények a gui.py-hez, az átláthatóság kedvéért külön fájlba raktam, 
mivel ezeknek nincsen közük a tkinterhez
"""

def get_today():
    date = datetime.now()
    time = datetime(date.year,date.month,date.day)
    return time

def make_string_printable(string):

    ROW_SIZE = 70

    row_count = math.ceil(len(string)/ROW_SIZE)

    new_string = ""

    for i in range(row_count):
        new_string += string[i*ROW_SIZE:(i+1)*ROW_SIZE] + '\n'

    return new_string

def return_event_title(event):
    return f"{event.start_time.strftime('%H:%M')} - {event.end_time.strftime('%H:%M')}"

def load_file(path):
    data = FileOperator.read_file(path)
    parsed_items = DataOperator.parse_items(data)

    return parsed_items