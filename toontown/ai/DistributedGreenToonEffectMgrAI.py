from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.distributed.ClockDelta import *
from direct.fsm.FSM import FSM

class DistributedGreenToonEffectMgrAI(DistributedObjectAI,  FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedGreenToonEffectMgrAI")

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        FSM.__init__(self, 'GreenToonFSM')
        self.air = air

    def enterOff(self):
        self.requestDelete()

    def addGreenToonEffect(self):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)
        av.b_setCheesyEffect(15, 0, 0)
        pass