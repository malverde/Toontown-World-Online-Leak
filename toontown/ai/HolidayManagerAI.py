from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed.ClockDelta import *
from direct.task import Task
from toontown.toonbase import ToontownGlobals
from toontown.parties import PartyGlobals
# fireworks
from toontown.effects.DistributedFireworkShowAI import DistributedFireworkShowAI
from toontown.effects import FireworkShows
import random
import time
from toontown.ai import HolidayGlobals


class HolidayManagerAI:
	notify = directNotify.newCategory('HolidayManagerAI')

	def __init__(self, air):
		self.air = air
		self.currentHolidays = []

		# TODO: Properly create a holiday manager to run this.
		#if config.GetBool('want-hourly-fireworks', False):
		 #   self.__startFireworksTick()

	"""
	Fireworks Stuff
	"""

	def startFireworksTick(self):
		# Check seconds until next hour.
		ts = time.time()
		nextHour = 3600 - (ts % 3600)
		taskMgr.doMethodLater(
			nextHour,
			self.fireworksTick,
			'hourly-fireworks')

	def fireworksTick(self, task):
		# The next tick will occur in exactly an hour.
		task.delayTime = 3600
		#showName = config.GetString('hourly-fireworks-type', 'july4')

		#if showName == 'july4':
		 #   showType = ToontownGlobals.JULY4_FIREWORKS
        show = HolidayGlobals.IsItFireworks()
		if show == 'Nyear':
				showType = ToontownGlobals.NEWYEARS_FIREWORKS
		elif show == 'Summer':
			showType = PartyGlobals.FireworkShows.Summer
		elif show == 'Release':
			showType = ToontownGlobals.VICTORY_RELEASE_FIREWORKS
		elif show == 'None':
            return
	#	elif showName == 'random':
	#		shows = [
	#			ToontownGlobals.JULY4_FIREWORKS,
	#			ToontownGlobals.NEWYEARS_FIREWORKS,
	#			PartyGlobals.FireworkShows.Summer,
	#			ToontownGlobals.VICTORY_RELEASE_FIREWORKS]
	#		showType = random.choice(shows)


		numShows = len(FireworkShows.shows.get(showType, []))
		showIndex = random.randint(0, numShows - 1)
		for hood in self.air.hoods:
			if hood.HOOD == ToontownGlobals.GolfZone:
				continue
			fireworksShow = DistributedFireworkShowAI(self.air)
			fireworksShow.generateWithRequired(hood.HOOD)
			fireworksShow.b_startShow(
				showType, showIndex, globalClockDelta.getRealNetworkTime())
			self.notify.info(
				'Oh! A fireworks show has started in this District - next one in exactly 1 hours time!')
		return task.again

	def isHolidayRunning(self, *args):
		return True
		# TODO: this function needs to actually check holidays
