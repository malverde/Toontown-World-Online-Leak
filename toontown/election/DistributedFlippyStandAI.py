#Embedded file name: toontown.election.DistributedFlippyStandAI
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

class DistributedFlippyStandAI(DistributedObjectAI, FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedFlippyStandAI')

    def __init__(self, air):
        #DistributedObjectAI.__init__(self, air)
        FSM.__init__(self, 'FlippyStandFSM')
        self.air = air
        self.pieTypeAmount = [4, 20, 1]

    def enterOff(self):
        self.requestDelete()

    def wheelbarrowAvatarEnter(self):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId, None)
        if not av:
            self.air.writeServerEvent('suspicious', avId=avId, issue="Got a request for pies from a toon that isn't on the district!")
            return
        if av.hp > 0:
            av.b_setPieType(self.pieTypeAmount[0])
            av.b_setNumPies(self.pieTypeAmount[1])
            av.b_setPieThrowType(self.pieTypeAmount[2])
