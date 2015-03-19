from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed.ClockDelta import *
from direct.task import Task

from toontown.toonbase import ToontownGlobals
from toontown.parties import PartyGlobals

from toontown.effects.DistributedFireworkShowAI import DistributedFireworkShowAI
from toontown.effects import FireworkShows

import random
import time

class HolidayManagerAI:
    def __init__(self, air):
        self.air = air
        self.currentHolidays = []
        self.xpMultiplier = 1


    def setup(self):
        holidays = config.GetString('force-holiday-decorations', '')
        if holidays != '':
            for holiday in holidays.split(","):
                holiday = int(holiday)
                self.currentHolidays.append(holiday)
            base.cr.newsManager.setHolidayIdList([self.currentHolidays])

    def isHolidayRunning(self, holidayId):
        if holidayId in self.currentHolidays:
            return True

    def isMoreXpHolidayRunning(self):
        if ToontownGlobals.MORE_XP_HOLIDAY in self.currentHolidays:
            self.xpMultiplier = 2
            return True
        return False

    def getXpMultiplier(self):
        return self.xpMultiplier
