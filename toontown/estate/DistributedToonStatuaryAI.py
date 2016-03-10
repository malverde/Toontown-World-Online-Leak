from direct.directnotify import DirectNotifyGlobal
from toontown.estate.DistributedStatuaryAI import DistributedStatuaryAI
from toontown.estate import GardenGlobals

class DistributedToonStatuaryAI(DistributedStatuaryAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedToonStatuaryAI")

    def __init__(self, air, gardenManager, ownerIndex):
        DistributedStatuaryAI.__init__(self, air, gardenManager, ownerIndex)

        self.dnaCode = None
        self.occupier = GardenGlobals.ToonStatuaryPlot

    def d_setOptional(self, dnaCode):
        self.sendUpdate('setOptional', [dnaCode])

    def getOptional(self):
        return self.dnaCode

    def construct(self, gardenData):
        DistributedStatuaryAI.construct(self, gardenData)

        self.dnaCode = gardenData.getUint16()

    def pack(self, gardenData):
        DistributedStatuaryAI.construct(self, gardenData)

        self.dnaCode = gardenData.addUint16(self.dnaCode)
