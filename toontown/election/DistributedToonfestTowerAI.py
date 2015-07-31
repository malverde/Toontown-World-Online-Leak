#Embedded file name: toontown.election.DistributedToonfestTowerAI
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

class DistributedToonfestTowerAI(DistributedObjectAI, FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedToonfestTowerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        FSM.__init__(self, 'ToonfestTowerFSM')
        self.air = air
        self.air.toonfestTower = self

    def enterOff(self):
        self.requestDelete()
        self.air.toonfestTower = None

    def updateTower(self, operation, base):
        self.sendUpdate('changeTowerSpeed', [operation, base])
