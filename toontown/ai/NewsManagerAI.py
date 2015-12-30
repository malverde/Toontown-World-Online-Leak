from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.distributed.ClockDelta import globalClockDelta
from direct.task import Task
from otp.ai.MagicWordGlobal import *
from toontown.effects.DistributedFireworkShowAI import DistributedFireworkShowAI
from toontown.effects import FireworkShows
from toontown.toonbase import ToontownGlobals
from toontown.ai import HolidayManagerAI
from toontown.ai import NewsInvasionAI
from toontown.parties import PartyGlobals
import HolidayGlobals
import datetime, random

class NewsManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("NewsManagerAI")

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.activeHolidays = []
        self.accept('avatarEntered', self.__announceIfHoliday)
        self.HolidayManagerAI = HolidayManagerAI.HolidayManagerAI(air)
        self.NewsInvasionAI = NewsInvasionAI.NewsInvasionAI(air)
        self.NewsInvasionAI.startInvTick()
        day = str(datetime.datetime.now().strftime("%d"))
        if str(datetime.datetime.now().strftime("%m")) == "12" and day ==  "30" or day == "31":
            self.HolidayManagerAI.startFireworksTick()


        elif str(datetime.datetime.now().strftime("%m")) == "12" and day == "14" or day == "15" or day == "16" or day == "17" or day == "18" or day == "19" or day == "20" or day == "21" or day == "22" or day == "23" or day == "24" or day == "25" or day == "26" or day == "27" or "28" or day == "29" or day == "30" or day == "31":
            self.HolidayName = 'Winter'

        elif str(datetime.datetime.now().strftime("%m")) == "1" and day == "2" or day == "3" or day == "4":
            self.HolidayName = 'Winter'

        elif str(datetime.datetime.now().strftime("%m")) == "10" and day ==  "21" or day == "22" or day == "23" or day == "25" or day == "26" or day == "27" or day == "28" or day == "29" or day == "30" or day == "31":
            self.HolidayName = 'Halloween'

        elif str(datetime.datetime.now().strftime("%m")) == "11" and day ==  "1":
            self.HolidayName = 'Halloween'

        elif str(datetime.datetime.now().strftime("%m")) == "3" and day ==  "14" or day == "15":
            self.HolidayName = 'Ides of March'

        elif str(datetime.datetime.now().strftime("%m")) == "7" and day ==  "29" or day == "30":
            self.HolidayName = 'Xp Booster'

        elif str(datetime.datetime.now().strftime("%m")) == "7" and day ==  "1" or day == "2" or day == "3" or day == "4" or day == "5" or day == "6" or day == "7" or day == "8" or day == "9" or day == "10" or day == "11" or day == "12" or day == "14" or day == "15":
            self.HolidayManagerAI.startFireworksTick()

        elif str(datetime.datetime.now().strftime("%m")) == "6" and day ==  "29" or "30":
            self.HolidayManagerAI.startFireworksTick()

        elif str(datetime.datetime.now().strftime("%m")) == "3" and day ==  "29" or day == "30" or day == "31":
            self.HolidayName = 'April Toons'

        elif str(datetime.datetime.now().strftime("%m")) == "4" and day == "1" or day == "2" or day == "3" or day == "4" or day == "5" or day == "6" or day == "7" or day == "9" or day == "10" or day == "11":
            self.HolidayName = 'April Toons'

        elif str(datetime.datetime.now().strftime("%m")) == "4" and day == "15":
            self.HolidayName = 'Tax Day'
        else:
            self.HolidayName = 'None'

    def __announceIfHoliday(self, avatar):
        self.sendUpdateToAvatarId(avatar.getDoId(),
                                  'setHolidays',
                                  [
                                      self.HolidayName])
        time.sleep(5)
        if self.air.suitInvasionManager.getInvading():
            self.sendUpdateToAvatarId(avatar.getDoId(),
                                      'setInvasionStatus',
                                      [ToontownGlobals.SuitInvasionBulletin,
                                       self.air.suitInvasionManager.suitName,
                                       self.air.suitInvasionManager.numSuits,
                                       self.air.suitInvasionManager.specialSuit])

    def announceGenerate(self):
        DistributedObjectAI.announceGenerate(self)
        self.__checkHolidays()
        self.accept('avatarEntered', self.__handleAvatarEntered)
        taskMgr.doMethodLater(15, self.__checkHolidays, 'holidayCheckTask')

    def delete(self):
        DistributedObjectAI.delete(self)
        self.deleteTasks()

    def __handleAvatarEntered(self, av):
        avId = av.getDoId()

    def deleteTasks(self):
        taskMgr.remove('holidayCheckTask')

    def getActiveHolidays(self):
        return self.activeHolidays

    def __checkHolidays(self, task=None):
        date = datetime.datetime.now(HolidayGlobals.TIME_ZONE)

        for id in HolidayGlobals.Holidays:
            holiday = HolidayGlobals.Holidays[id]
            running = self.isHolidayRunning(id)

            if self.isHolidayInRange(holiday, date):
                if not running:
                    self.startHoliday(id)
            elif running:
                self.endHoliday(id)

        return Task.again

    def isHolidayInRange(self, holiday, date):
        if 'weekDay' in holiday:
            return holiday['weekDay'] == date.weekday()
        else:
            return HolidayGlobals.getStartDate(holiday) <= date <= HolidayGlobals.getEndDate(holiday)

    def isHolidayRunning(self, *args):
        for id in args:
            if id in self.activeHolidays:
                return True

    def startHoliday(self, id):
        if id in self.activeHolidays or id not in HolidayGlobals.Holidays:
            return False

        self.activeHolidays.append(id)
        self.startSpecialHoliday(id)
        self.sendUpdate('startHoliday', [id])
        return True

    def endHoliday(self, id):
        if id not in self.activeHolidays or id not in HolidayGlobals.Holidays:
            return False

        self.activeHolidays.remove(id)
        self.endSpecialHoliday(id)
        self.sendUpdate('endHoliday', [id])
        return True

    def startSpecialHoliday(self, id):
        if id == ToontownGlobals.FISH_BINGO or id == ToontownGlobals.SILLY_SATURDAY:
            messenger.send('startBingo')
        elif id in [ToontownGlobals.SUMMER_FIREWORKS, ToontownGlobals.NEW_YEAR_FIREWORKS]:
            self.fireworkTasks.append(
                taskMgr.doMethodLater((60 - datetime.datetime.now().minute) * 60, self.startFireworkTask,
                                      'initialFireworkTask-%s' % id, extraArgs=[id]))

    def endSpecialHoliday(self, id):
        if id == ToontownGlobals.FISH_BINGO or id == ToontownGlobals.SILLY_SATURDAY:
            messenger.send('stopBingo')
        elif id in [ToontownGlobals.SUMMER_FIREWORKS, ToontownGlobals.NEW_YEAR_FIREWORKS]:
            self.deleteFireworkTasks()


            # def setPopulation(self, todo0):
            # 	pass
            #
            # def setBingoWin(self, todo0):
            # 	pass
            #
            # def setBingoStart(self):
            # 	pass
            #
            # def setBingoEnd(self):
            # 	pass
            #
            # def setCircuitRaceStart(self):
            # 	pass
            #
            # def setCircuitRaceEnd(self):
            # 	pass
            #
            # def setTrolleyHolidayStart(self):
            # 	pass
            #
            # def setTrolleyHolidayEnd(self):
            # 	pass
            #
            # def setTrolleyWeekendStart(self):
            # 	pass
            #
            # def setTrolleyWeekendEnd(self):
            # 	pass
            #
            # def setRoamingTrialerWeekendStart(self):
            # 	pass
            #
            # def setRoamingTrialerWeekendEnd(self):
            # 	pass
            #
            # def setInvasionStatus(self, todo0, todo1, todo2, todo3):
            # 	pass
            #
            # def setHolidayIdList(self, todo0):
            # 	pass
            #
            # def holidayNotify(self):
            # 	pass
            #
            # def setWeeklyCalendarHolidays(self, todo0):
            # 	pass
            #
            # def getWeeklyCalendarHolidays(self):
            # 	return []
            #
            # def setYearlyCalendarHolidays(self, todo0):
            # 	pass
            #
            # def getYearlyCalendarHolidays(self):
            # 	return []
            #
            # def setOncelyCalendarHolidays(self, todo0):
            # 	pass
            #
            # def getOncelyCalendarHolidays(self):
            # 	return []
            #
            # def setRelativelyCalendarHolidays(self, todo0):
            # 	pass
            #
            # def getRelativelyCalendarHolidays(self):
            # 	return []
            #
            # def setMultipleStartHolidays(self, todo0):
            # 	pass
            #
            # def getMultipleStartHolidays(self):
            # 	return []
            #
            # def sendSystemMessage(self, todo0, todo1):
            # 	pass


@magicWord(category=CATEGORY_SYSADMIN)
def newsShutdown():
    """
    Shutdown the news manager tasks.
    """
    simbase.air.newsManager.deleteTasks()
    return 'News manager shut down!'

@magicWord(category=CATEGORY_SYSADMIN, types=[int])
def startHoliday(holiday):
    """
    Start a holiday.
    """
    if simbase.air.newsManager.startHoliday(holiday):
        return 'Started holiday %s!' % holiday

    return 'Holiday %s is already running!' % holiday

@magicWord(category=CATEGORY_SYSADMIN, types=[int])
def stopHoliday(holiday):
    """
    Stop a holiday.
    """
    if simbase.air.newsManager.endHoliday(holiday):
        return 'Stopped holiday %s!' % holiday

    return 'Holiday %s is not running!' % holiday