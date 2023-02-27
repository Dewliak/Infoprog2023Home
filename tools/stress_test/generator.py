import random
import time
from datetime import datetime

def str_time_prop(start, end, time_format, prop):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formatted in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """

    stime = time.mktime(time.strptime(start, time_format))
    etime = time.mktime(time.strptime(end, time_format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(time_format, time.localtime(ptime))


def random_date(start, end, prop):
    return str_time_prop(start, end, '%m/%d/%Y %I:%M %p', prop)
    


import string
"""
lines = open('naplo.txt').readlines()
random.shuffle(lines)
open('naplo.txt', 'w').writelines(lines)

"""

def generate_random():

    with open("data/naplo.txt", 'a', encoding ='utf-8') as file:
        for i in range(100):
            x = random_date("1/1/2008 1:30 PM", "1/1/2022 4:50 AM", random.random())
            r_date = datetime.strptime(x,'%m/%d/%Y %I:%M %p')
            for j in range(100):
                t = random_date("1/1/2008 1:30 PM", "1/1/2022 4:50 AM", random.random())
                r_time = datetime.strptime(t,'%m/%d/%Y %I:%M %p')
                start_time = datetime(year=1900,month=1,day=1,hour=r_time.hour,minute=r_time.minute)
                N = 20
                description = ''.join(random.choices(string.ascii_uppercase +
                                             string.digits, k=N))
                
                data = r_date.strftime("%d-%m-%Y") + "," + start_time.strftime("%H:%M") + "," + start_time.strftime("%H:%M") + "," + description
                file.write("\n")
                file.write(data)
