#Embedded file name: toontown.election.DistributedToonfestTowerBaseAI
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

class DistributedToonfestTowerBaseAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedToonfestTowerBaseAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.air = air
        self.air.toonfestTowerBase = self

    def requestSpeedUp(self):
        pass

    def requestChangeDirection(self):
        pass

    def setSpeed(self, todo0, todo1, todo2):
        pass

    def playSpeedUp(self, todo0):
        pass

    def playChangeDirection(self, todo0):
        pass
