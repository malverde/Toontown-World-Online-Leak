#Embedded file name: toontown.estate.DistributedGardenBoxAI
from direct.directnotify import DirectNotifyGlobal
from toontown.estate.DistributedLawnDecorAI import DistributedLawnDecorAI

class DistributedGardenBoxAI(DistributedLawnDecorAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedGardenBoxAI')

    def __init__(self, air, gardenManager, ownerIndex):
        DistributedLawnDecorAI.__init__(self, air, gardenManager, ownerIndex)
        self.typeIndex = 0

    def setTypeIndex(self, index):
        self.typeIndex = index

    def getTypeIndex(self):
        return self.typeIndex
