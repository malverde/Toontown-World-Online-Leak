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
		day = str(datetime.datetime.now().strftime("%d"))
		month = str(datetime.datetime.now().strftime("%m"))
		task.delayTime = 1800
		invMgr = simbase.air.suitInvasionManager
		if invMgr.getInvading():
			print "There is already an invasion on this AI, cannot spawn Cogs!"
		else:
		# The next tick will occur in exactly an hour.

			# Tax Invasion
			# Invasion scheduled for 15th of April - Number Crunchers - nomral, 2,500 Cogs
			if str(datetime.datetime.now().strftime("%m")) == "04" and day ==  "15":
				name = 'nc'
				num = 2500
				special = 0
				invMgr.startInvasion(name, num,special)
				print "A Holiday Number Cruncher Invasion Has Been Spawned"
			else:
			    break

			# Ides of March
			# Invasion scheduled for 15th of March - Back Stabbers - nomral, 2,500 Cogs
			if str(datetime.datetime.now().strftime("%m")) == "03" and day == "15":
				name = 'bs'
				num = 2500
				special = 0
				invMgr.startInvasion(name, num, special)
				print "A Holiday Back Stabber Invasion Has Been Spawned"
			else:
			    break

			# Invasion scheduled for 15th Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec- Mover & Shaker - 2.0 Cogs, 2,500 Cogs
			if month == "01" or month == "02" or month == "03" or month == "05" or month == "06" or month == "07" or month == "08" or month == "09" or month == "10" or month == "11" or month == "12" and day ==  "15":
				name = 'ms'
				num = 2500
				special = 2
				invMgr.startInvasion(name, num,special)
				print "A Holiday 2.0 M&S Invasion Has Been Spawned"
			else:
			    break

			# Invasion scheduled for 31st Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec - Legal Eagle - Skelecog, 2,500 Cogs
			if month == "01" or month == "03" or month == "05" or month == "07" or month == "08" or month == "10" or month == "12" and day ==  "31":
				name = 'le'
				num = 2500
				special = 1
				invMgr.startInvasion(name, num,special)
				print "A Holiday Skelecog Legal Eagle Invasion Has Been Spawned"
			else:
			    break

			# Invasion scheduled for 30th of April, Jun, Sep - Legal Eagle - Skelecog, 2,500 Cogs
			if month == "04" or month == "06" or month == "09" or month == "11" and day ==  "30":
				name = 'le'
				num = 2500
				special = 1
				invMgr.startInvasion(name, num,special)
				print "A Holiday Skelecog Legal Eagle Invasion Has Been Spawned"
			else:
			    break

			# Invasion scheduled for 30th of Feb - Legal Eagle - Skelecog, 2,500 Cogs
			if month == "02" and day ==  "29":
				name = 'le'
				num = 2500
				special = 1
				invMgr.startInvasion(name, num,special)
				print "A Holiday Skelecog Legal Eagle Invasion Has Been Spawned"
			else:
			    break
		
		return task.again

