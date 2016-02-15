from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from toontown.toonbase import ToontownGlobals
from otp.ai.MagicWordGlobal import *
from toontown.toonbase import TTLocalizerEnglish as TTLocalizer
from toontown.ai import HolidayManagerAI
# from toontown.ai import NewsInvasionAI
from toontown.ai import HolidayGlobals
import time

class NewsManagerAI(DistributedObjectAI):
	notify = DirectNotifyGlobal.directNotify.newCategory("NewsManagerAI")

	def __init__(self, air):
		DistributedObjectAI.__init__(self, air)
		self.accept('avatarEntered', self.__announceIfHoliday)
		self.HolidayManagerAI = HolidayManagerAI.HolidayManagerAI(air)
		# self.NewsInvasionAI = NewsInvasionAI.NewsInvasionAI(air)
		# self.NewsInvasionAI.startInvTick()
		self.HolidayManagerAI.startFireworksTick()
		self.HolidayName = []

	def __announceIfHoliday(self, avatar):
		try:
			holidayList = HolidayGlobals.WhatHolidayIsItAI()
			Holiday1 = holidayList[0]
			Holiday2 = holidayList[1]
			self.sendUpdateToAvatarId(avatar.getDoId(),
                                    'setHolidays',
                                    [ Holiday1])
			self.sendUpdateToAvatarId(avatar.getDoId(),
                                        'setHolidays',
                                        [Holiday2])
		except:
			holidayList = HolidayGlobals.WhatHolidayIsItAI()
			Holiday1 = holidayList[0]
			self.sendUpdateToAvatarId(avatar.getDoId(),
                                        'setHolidays',
                                        [Holiday1])

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

@magicWord(category=CATEGORY_DEBUG, types=[str])
def HolidayMessage(holiday):
	""" Sends A cleint A holiday massage out of Winter, Bingo, Halloween or Xp Booster """
	simbase.air.newsManager.sendUpdateToAvatarId(
		spellbook.getInvoker().getDoId(),
		'setHolidays',
		[holiday])
	return "Sent the message"
