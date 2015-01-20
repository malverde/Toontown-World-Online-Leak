from SZHoodAI import SZHoodAI
from toontown.hood.HoodAI import *
from toontown.toonbase import ToontownGlobals
from toontown.distributed.DistributedTimerAI import DistributedTimerAI
from toontown.safezone.DistributedPicnicBasketAI import DistributedPicnicBasketAI
from toontown.safezone.DistributedPicnicTableAI import DistributedPicnicTableAI

class OZHoodAI(SZHoodAI):
    HOOD = ToontownGlobals.OutdoorZone
    
    def createZone(self):
        SZHoodAI.createTreasurePlanner(self)
        self.timer = DistributedTimerAI(self.air)
        self.timer.generateWithRequired(self.HOOD)
        self.spawnObjects()

    def spawnObjects(self):
        HoodAI.spawnObjects(self)
        filename = self.air.genDNAFileName(self.HOOD)
        self.air.dnaSpawner.spawnObjects(filename, self.HOOD)
