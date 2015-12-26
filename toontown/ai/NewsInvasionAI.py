from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed.ClockDelta import *
from direct.task import Task
import time
import datetime
from toontown.suit import SuitInvasionManagerAI

class NewsInvasionAI:
	notify = directNotify.newCategory('NewsInvasion')

	def __init__(self, air):
		self.air = air
		self.SuitInvasionManagerAI = SuitInvasionManagerAI.SuitInvasionManagerAI(air)
		day = str(datetime.datetime.now().strftime("%d"))

		# TODO: Properly create a holiday manager to run this.

	"""
	Fireworks Stuff
	"""
	def startInvTick(self):
		# Check seconds until next hour.
		ts = time.time()
		nextHour = 1800 - (ts % 1800)
		taskMgr.doMethodLater(
			nextHour,
			self.InvTick,
			'hourly-fireworks')


	def InvTick(self, task):
		day = str(datetime.datetime.now().strftime("%d"))
		task.delayTime = 1800
		invMgr = simbase.air.suitInvasionManager
		if invMgr.getInvading():
			return "There is an invasaion!!"
		else:
		# The next tick will occur in exactly an hour.
			if str(datetime.datetime.now().strftime("%m")) == "4" and day ==  "15":
				name = 'nc'
				num = 2500
				special = 0
				invMgr.startInvasion(name, num,special)
				print "Loan invasion made"
		
		return task.again

