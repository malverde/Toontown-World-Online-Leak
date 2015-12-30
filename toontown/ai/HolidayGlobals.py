from toontown.toonbase import ToontownGlobals, TTLocalizer
from toontown.toonbase import ToontownGlobals, TTLocalizer
from toontown.parties import ToontownTimeZone
import calendar, datetime

TIME_ZONE = ToontownTimeZone.ToontownTimeZone()
TRICK_OR_TREAT = 0
WINTER_CAROLING = 1
CAROLING_REWARD = 100
SCAVENGER_HUNT_LOCATIONS = 6


Holidays = {
    # ToontownGlobals.LAUGHING_MAN: {
    #     'startMonth': 6,
    #     'startDay': 22,
    #     'endMonth': 6,
    #     'endDay': 22,
    #     'startMessage': TTLocalizer.LaughingManHolidayStart,
    #     'ongoingMessage': TTLocalizer.LaughingManHolidayOngoing,
    #     'endMessage': TTLocalizer.LaughingManHolidayEnd
    # },
    ToontownGlobals.GRAND_PRIX: {
        'weekDay': 0,
        'startMessage': TTLocalizer.CircuitRaceStart,
        'ongoingMessage': TTLocalizer.CircuitRaceOngoing,
        'endMessage': TTLocalizer.CircuitRaceEnd
    },
    ToontownGlobals.FISH_BINGO: {
        'weekDay': 2,
        'startMessage': TTLocalizer.FishBingoStart,
        'ongoingMessage': TTLocalizer.FishBingoOngoing,
        'endMessage': TTLocalizer.FishBingoEnd
    },
    ToontownGlobals.SILLY_SATURDAY: {
        'weekDay': 5,
        'startMessage': TTLocalizer.SillySaturdayStart,
        'ongoingMessage': TTLocalizer.SillySaturdayOngoing,
        'endMessage': TTLocalizer.SillySaturdayEnd
    }
}

def getHoliday(id):
    return Holidays.get(id, {})

def getServerTime(date):
    epoch = datetime.datetime.fromtimestamp(0, TIME_ZONE)
    delta = date - epoch

    return delta.total_seconds()

def getStartDate(holiday, rightNow=None):
    if not rightNow:
        rightNow = datetime.datetime.now()

    startMonth = holiday['startMonth'] if 'startMonth' in holiday else rightNow.month
    startDay = holiday['startDay'] if 'startDay' in holiday else (rightNow.day if 'weekDay' in holiday else calendar.monthrange(rightNow.year, startMonth)[0])
    startDate = datetime.datetime(rightNow.year, startMonth, startDay, tzinfo=TIME_ZONE)

    return startDate

def getEndDate(holiday, rightNow=None):
    if not rightNow:
        rightNow = datetime.datetime.now()

    endMonth = holiday['endMonth'] if 'endMonth' in holiday else rightNow.month
    endDay = holiday['endDay'] if 'endDay' in holiday else (rightNow.day if 'weekDay' in holiday else calendar.monthrange(rightNow.year, endMonth)[1])
    endYear = rightNow.year

    if 'startMonth' in holiday and holiday['startMonth'] > endMonth:
        endYear += 1

    endDate = datetime.datetime(endYear, endMonth, endDay, tzinfo=TIME_ZONE)

    return endDate