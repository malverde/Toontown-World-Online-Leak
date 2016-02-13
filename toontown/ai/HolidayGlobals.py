import time
import datetime


day = int(datetime.datetime.now().strftime("%d"))

holidays = []

# Holiday variable to send to client

if int(datetime.datetime.now().strftime("%m")) == 12 and day > 13: # December
	HolidayName = 'Winter'
	holidys.append(HolidayName)
elif int(datetime.datetime.now().strftime("%m")) == 1 and not day  > 4: # January
    HolidayName = 'Winter'
    holidys.append(HolidayName)
elif datetime.datetime.today().weekday() == 3 or datetime.datetime.today().weekday() == 6: # Wednesday and Sunday
    HolidayName = 'Bingo'
    holidys.append(HolidayName)
elif int(datetime.datetime.now().strftime("%m")) == 10 and day >= 21 and day <= 31: # October
    HolidayName = 'Halloween'  
    holidys.append(HolidayName)
elif int(datetime.datetime.now().strftime("%m")) == 11 and day ==  1: # November
    HolidayName = 'Halloween'
    holidys.append(HolidayName)
elif int(datetime.datetime.now().strftime("%m")) == 3 and day >= 29 and day <= 31: # March
    HolidayName = 'April Toons'
    holidys.append(HolidayName)
elif int(datetime.datetime.now().strftime("%m")) == 4 and day >= 1 and day <= 11: # April
    HolidayName = 'April Toons'
    holidys.append(HolidayName)
elif int(datetime.datetime.now().strftime("%m")) == 2: # Feburary
	HolidayName = 'Xp Booster'
	holidys.append(HolidayName)
elif int(datetime.datetime.now().strftime("%m")) == 4: # April
	HolidayName = 'Xp Booster'
	holidys.append(HolidayName)
else:
    HolidayName = 'None'


# AI/Client logic

# XP Booster logic

if int(datetime.datetime.now().strftime("%m")) == 2: # Febuary
    Xp = 2.0
elif int(datetime.datetime.now().strftime("%m")) == 4: # April
	Xp = 2.0
elif int(datetime.datetime.now().strftime("%m")) == 7 and day == 29 or day == 30: # July
    Xp = 3.0
else:
    Xp = 1.0


# Fireworks logic
if int(datetime.datetime.now().strftime("%m")) == 2: # Feburary
    Show = 'Release'
elif int(datetime.datetime.now().strftime("%m")) == 7 and day < 16: # July
    Show = 'Summer'
elif int(datetime.datetime.now().strftime("%m")) == 12 and day == 30 or day == 31: # December
    Show = 'Nyear'

# Invasions logic

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

# Bingo logic
if datetime.datetime.today().weekday() == 3 or datetime.datetime.today().weekday() == 6:
	bingo = True
else:
	bingo = False


# Animated Street props!! :D :D :D - logic
if datetime.datetime.today().weekday() == 5 or datetime.datetime.today().weekday() == 6 or int(datetime.datetime.now().strftime("%m")) == 2: # TODO: Remove - To show off Props
	props = True
else:
	props = False


def WhatHolidayIsIt():
    return holidays

def WhatIsXp():
    return Xp
    
def IsItFireworks():
    return Show

def IsItInvasion():
    return name, num, special

def IsBingo():
	return bingo

def IsProp():
	return props