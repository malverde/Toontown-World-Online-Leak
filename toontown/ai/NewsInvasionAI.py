from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed.ClockDelta import *
from direct.task import Task
import time
import datetime
from toontown.suit import SuitInvasionManagerAI
from toontown.ai import HolidayGlobals

class NewsInvasionAI:
	notify = directNotify.newCategory('NewsInvasion')

	def __init__(self, air):
		self.air = air
		self.SuitInvasionManagerAI = SuitInvasionManagerAI.SuitInvasionManagerAI(air)
		day = str(datetime.datetime.now().strftime("%d"))

		# TODO: Properly create a Holiday manager to run this.

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
		task.delayTime = 1800
		invMgr = simbase.air.suitInvasionManager
		if invMgr.getInvading():
			print "Invasion in-progress on AI, cannot spawn a different invasion!"
		else:
			try:
				listI = HolidayGlobals.IsItInvasion()
				var1 = str(listI[0])
				var2 = int(listI[1])
				var3 = int(listI[2])
				print var1 + ' ' + var2 + ' ' + var3
				suit = '%s' % var1
				invMgr.startInvasion(suit, var2, var3)
			except:
				pass
				print "Warning: there was an issue spawning an invasion (issue)" 
			
		return task.again

