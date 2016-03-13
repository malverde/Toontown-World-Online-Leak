import time
import datetime


day = int(datetime.datetime.now().strftime("%d"))

holidays = []

# Holiday variable to send to client
# NOTE: Months are - 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 -
# Days are - 0 - Mon, 1 - Tues, 2 - Wed, 3 - Thurs, 4 - Friday, 5 - Sat, 6 - Sunday

if int(datetime.datetime.now().strftime("%m")) == 12 and day > 13: # December
	HolidayName = 'Winter'
	holidays.append(HolidayName)
else:
    HolidayName = 'None'

if int(datetime.datetime.now().strftime("%m")) == 1 and not day  > 4: # January
    HolidayName = 'Winter'
    holidays.append(HolidayName)
else:
    HolidayName = 'None'
    
if datetime.datetime.today().weekday() == 3 or datetime.datetime.today().weekday() == 5: # Wednesday and Saturday
    HolidayName = 'Bingo'
    holidays.append(HolidayName)
else:
    HolidayName = 'None'
    
if int(datetime.datetime.now().strftime("%m")) == 10 and day >= 21 and day <= 31: # October
    HolidayName = 'Halloween'  
    holidays.append(HolidayName)
else:
    HolidayName = 'None'
    
if int(datetime.datetime.now().strftime("%m")) == 11 and day ==  1: # November
    HolidayName = 'Halloween'
    holidays.append(HolidayName)
else:
    HolidayName = 'None'
    
if int(datetime.datetime.now().strftime("%m")) == 3 and day >= 29 and day <= 31: # March
    HolidayName = 'April Toons'
    holidays.append(HolidayName)
else:
    HolidayName = 'None'
    
if int(datetime.datetime.now().strftime("%m")) == 4 and day >= 1 and day <= 11: # April
    HolidayName = 'April Toons'
    holidays.append(HolidayName)
else:
    HolidayName = 'None'
if int(datetime.datetime.now().strftime("%m")) == 2: # Feburary
	HolidayName = 'Xp Booster'
	holidays.append(HolidayName)
else:
    HolidayName = 'None'

if int(datetime.datetime.now().strftime("%m")) == 4: # April
	HolidayName = 'Xp Booster'
	holidays.append(HolidayName)
else:
    HolidayName = 'None'

if int(datetime.datetime.now().strftime("%m")) == 3 and day >= 1 and day <= 25: # April
    HolidayName = 'April Toons'
    holidays.append(HolidayName)
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
else:
    Show = None

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
if datetime.datetime.today().weekday() == 3 or datetime.datetime.today().weekday() == 5: # Wednesday and Saturday
	bingo = True
else:
	bingo = False


# Animated Street props!! :D :D :D - logic
if datetime.datetime.today().weekday() == 5 or datetime.datetime.today().weekday() == 6 or int(datetime.datetime.now().strftime("%m")) == 2: # TODO: Remove - To show off Props
	props = True
else:
	props = False


def WhatHolidayIsItAI():
    return holidays
    
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

def IsProp():
	return props
