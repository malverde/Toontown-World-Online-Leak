import time
import datetime

day = int(datetime.datetime.now().strftime("%d"))

if int(datetime.datetime.now().strftime("%m")) == 12 and day >= 14  and day <= 31:
	HolidayName = 'Winter'
else:
    HolidayName = 'None'

if str(datetime.datetime.now().strftime("%m")) == 1 and day >= 1 and day  <= 4:
    HolidayName = 'Winter'
else:
    HolidayName = 'None'

if int(datetime.datetime.now().strftime("%m")) == 10 and day >= 21 and day <= 31:
    HolidayName = 'Halloween'
else:
    HolidayName = 'None'
    
if int(datetime.datetime.now().strftime("%m")) == 11 and day ==  1:
    HolidayName = 'Halloween'
else:
    HolidayName = 'None'

if int(datetime.datetime.now().strftime("%m")) == 3 and day >= 29 and day <= 31:
    HolidayName = 'April Toons'
else:
    HolidayName = 'None'

if int(datetime.datetime.now().strftime("%m")) == 4 and day >= 1 and day <= 11:
    HolidayName = 'April Toons'
else:
    HolidayName = 'None'

def WhatHolidayIsIt():
    return HolidayName