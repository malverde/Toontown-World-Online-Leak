from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from toontown.toonbase import ToontownGlobals
from otp.ai.MagicWordGlobal import *
from toontown.toonbase import TTLocalizerEnglish as TTLocalizer
import datetime
from toontown.ai import HolidayManagerAI
from toontown.ai import NewsInvasionAI
import time

class NewsManagerAI(DistributedObjectAI):
	notify = DirectNotifyGlobal.directNotify.newCategory("NewsManagerAI")

	def __init__(self, air):
		DistributedObjectAI.__init__(self, air)
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

	def setPopulation(self, todo0):
		pass

	def setBingoWin(self, todo0):
		pass

	def setBingoStart(self):
		pass

	def setBingoEnd(self):
		pass

	def setCircuitRaceStart(self):
		pass

	def setCircuitRaceEnd(self):
		pass

	def setTrolleyHolidayStart(self):
		pass

	def setTrolleyHolidayEnd(self):
		pass

	def setTrolleyWeekendStart(self):
		pass

	def setTrolleyWeekendEnd(self):
		pass

	def setRoamingTrialerWeekendStart(self):
		pass

	def setRoamingTrialerWeekendEnd(self):
		pass

	def setInvasionStatus(self, todo0, todo1, todo2, todo3):
		pass

	def setHolidayIdList(self, todo0):
		pass

	def holidayNotify(self):
		pass

	def setWeeklyCalendarHolidays(self, todo0):
		pass

	def getWeeklyCalendarHolidays(self):
		return []

	def setYearlyCalendarHolidays(self, todo0):
		pass

	def getYearlyCalendarHolidays(self):
		return []

	def setOncelyCalendarHolidays(self, todo0):
		pass

	def getOncelyCalendarHolidays(self):
		return []

	def setRelativelyCalendarHolidays(self, todo0):
		pass

	def getRelativelyCalendarHolidays(self):
		return []

	def setMultipleStartHolidays(self, todo0):
		pass

	def getMultipleStartHolidays(self):
		return []

	def sendSystemMessage(self, todo0, todo1):
		pass


@magicWord(category=CATEGORY_DEBUG)
def invasionstatus():
	""" Returns the number of cogs available in an invasion in a pretty way. """
	simbase.air.newsManager.sendUpdateToAvatarId(
		spellbook.getInvoker().getDoId(),
		'setInvasionStatus',
		[
			ToontownGlobals.SuitInvasionUpdate,
			simbase.air.suitInvasionManager.suitName,
			simbase.air.suitInvasionManager.numSuits,
			simbase.air.suitInvasionManager.specialSuit])
