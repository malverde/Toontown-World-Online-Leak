import time
import datetime

if str(datetime.datetime.now().strftime("%m")) == "12" and day == "14" or day == "15" or day == "16" or day == "17" or day == "18" or day == "19" or day == "20" or day == "21" or day == "22" or day == "23" or day == "24" or day == "25" or day == "26" or day == "27" or "28" or day == "29" or day == "30" or day == "31":
	HolidayName = 'Winter'
else:
    HolidayName = 'None'

if str(datetime.datetime.now().strftime("%m")) == "01" and day == "02" or day == "03" or day == "04":
    HolidayName = 'Winter'
else:
    HolidayName = 'None'

if str(datetime.datetime.now().strftime("%m")) == "10" and day ==  "21" or day == "22" or day == "23" or day == "25" or day == "26" or day == "27" or day == "28" or day == "29" or day == "30" or day == "31":
    HolidayName = 'Halloween'
else:
    HolidayName = 'None'
    
if str(datetime.datetime.now().strftime("%m")) == "11" and day ==  "01":
    HolidayName = 'Halloween'
else:
    HolidayName = 'None'

if str(datetime.datetime.now().strftime("%m")) == "03" and day ==  "29" or day == "30" or day == "31":
    HolidayName = 'April Toons'
else:
    HolidayName = 'None'

if str(datetime.datetime.now().strftime("%m")) == "03" and day ==  "29" or day == "30" or day == "31":
    HolidayName = 'April Toons'
else:
    HolidayName = 'None'

def WhatHolidayIsIt():
    return HolidayName