#Embedded file name: toontown.election.DistributedToonfestCogAI
from direct.interval.IntervalGlobal import *
from direct.fsm.FSM import FSM
from otp.ai.MagicWordGlobal import *
from toontown.election.DistributedHotAirBalloonAI import DistributedHotAirBalloonAI
from DistributedElectionCameraManagerAI import DistributedElectionCameraManagerAI
from DistributedSafezoneInvasionAI import DistributedSafezoneInvasionAI
from DistributedInvasionSuitAI import DistributedInvasionSuitAI
from InvasionMasterAI import InvasionMasterAI
from toontown.toonbase import ToontownGlobals
import SafezoneInvasionGlobals
import ElectionGlobals
import random
from otp.distributed.OtpDoGlobals import *
from direct.task import Task
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from toontown.election import *

class DistributedToonfestCogAI(DistributedObjectAI, FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedToonfestTowerAI')

    def __init__(self, air, operation = 'SpeedUp'):
        DistributedObjectAI.__init__(self, air)
        FSM.__init__(self, 'ToonfestCogFSM')
        self.air = air
        self.validOperations = ['SpeedUp', 'SlowDown', 'Reverse']
        if operation in self.validOperations:
            self.operation = operation
        else:
            print 'DistributedToonfestCogAI: Operation %s is not a valid operation.' % operation
            self.operation = 'SpeedUp'

    def enterOff(self):
        self.requestDelete()

    def setPos(self, x, y, z):
        self.sendUpdate('setPosThroughAI', [x, y, z])

    def setId(self, id):
        self.sendUpdate('setIdThroughAI', [id])

    def enterDown(self):
        pass

    def enterUp(self):
        pass

    def updateTower(self):
        if not isinstance(self.air.toonfestTower, DistributedToonfestTowerAI) or not self.air.toonfestTower:
            print 'DistributedToonfestCogAI: ERROR! Could not find the ToonFest Tower.'
        else:
            base = random.randrange(0, 3)
            self.air.toonfestTower.updateTower(self.operation, base)
            print 'DistributedToonfestCogAI: Told Tower to ' + self.operation + ' base number ' + str(base + 1)
