import time
import datetime


day = int(datetime.datetime.now().strftime("%d"))

#Holidays

if int(datetime.datetime.now().strftime("%m")) == 12 and day > 13:
	HolidayName = 'Winter'
elif int(datetime.datetime.now().strftime("%m")) == 1 and not day  > 4:
    HolidayName = 'Winter'
elif datetime.datetime.today().weekday() == 5 or datetime.datetime.today().weekday() == 6:
    HolidayName = 'Bingo'
elif int(datetime.datetime.now().strftime("%m")) == 10 and day >= 21 and day <= 31:
    HolidayName = 'Halloween'  
elif int(datetime.datetime.now().strftime("%m")) == 11 and day ==  1:
    HolidayName = 'Halloween'
elif int(datetime.datetime.now().strftime("%m")) == 3 and day >= 29 and day <= 31:
    HolidayName = 'April Toons'
elif int(datetime.datetime.now().strftime("%m")) == 4 and day >= 1 and day <= 11:
    HolidayName = 'April Toons'
elif int(datetime.datetime.now().strftime("%m")) == 2:
	HolidayName = 'Xp Booster'
else:
    HolidayName = 'None'


#Xp 

if int(datetime.datetime.now().strftime("%m")) == 2:
    Xp = 2.0
elif int(datetime.datetime.now().strftime("%m")) == 7 and day == 29 or day == 30:
    Xp = 3.0
else:
    Xp = 1.0


#Fireworks
if int(datetime.datetime.now().strftime("%m")) == 2:
    Show = 'Release'
elif int(datetime.datetime.now().strftime("%m")) == 7 and day < 16:
    Show = 'Summer'
elif int(datetime.datetime.now().strftime("%m")) == 12 and day == 30 or day == 31:
    Show = 'Nyear'

#Invasions 

# Tax Invasion
# Invasion scheduled for 15th of April - Number Crunchers - nomral, 2,500 Cogs
if int(datetime.datetime.now().strftime("%m")) == 4 and day == 15:
	name = 'nc'
	num = 2500
	special = 0
	
# Ides of March
# Invasion scheduled for 15th of March - Back Stabbers - nomral, 2,500 Cogs
if int(datetime.datetime.now().strftime("%m")) == 3 and day == 15:
	name = 'bs'
	num = 2500
	special = 0
	
# Invasion scheduled for 15th Mover & Shaker - 2.0 Cogs, 2,500 Cogs
if day == 15:
	name = 'ms'
	num = 2500
	special = 2

#Legal Eagle - Skelecog, 2,500 Cogs
if day == 30 or day ==  31:
	name = 'le'
	num = 2500
	special = 1

#Bingo!!!
if datetime.datetime.today().weekday() == 5 or datetime.datetime.today().weekday() == 6:
	bingo = True
else:
	bingo = False

def WhatHolidayIsIt():
    return HolidayName

def WhatIsXp():
    return Xp
    
def IsItFireworks():
    return Show

def IsItInvasion():
    return name, num, special

def IsBingo():
	return bingo

