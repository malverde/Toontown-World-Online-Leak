from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedNodeAI import DistributedNodeAI

class DistributedLawnDecorAI(DistributedNodeAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedLawnDecorAI")

    def __init__(self, mgr):
        self.mgr = mgr
        DistributedNodeAI.__init__(self, self.mgr.air)
        self.plot = 0
        self.ownerIndex = 0
          
    def setPlot(self, plot):
        self.plot = plot
          
    def getPlot(self):
        return self.plot

    def getHeading(self):
        return self.getH()

    def getPosition(self):
        return self.getPos()

    def setOwnerIndex(self, ownerIndex):
        self.ownerIndex = ownerIndex
        self.ownerDoId = self.mgr.gardenMgr.mgr.toons[ownerIndex]
        self.owner = self.air.doId2do.get(self.ownerDoId)
        
    def getOwnerIndex(self):
        return self.ownerIndex

    def d_setMovie(self, mode, avId=None):
        if avId is None:
            avId = self.air.getAvatarIdFromSender()
            
        self.sendUpdate('setMovie', [mode, avId])

    def d_interactionDenied(self):
        self.sendUpdate('interactionDenied', [self.air.getAvatarIdFromSender()])
