from SZHoodAI import SZHoodAI
from toontown.hood.HoodAI import *
from toontown.toonbase import ToontownGlobals
from toontown.classicchars import DistributedChipAI
from toontown.classicchars import DistributedDaleAI
from toontown.distributed.DistributedTimerAI import DistributedTimerAI
from toontown.safezone.DistributedPicnicBasketAI import DistributedPicnicBasketAI
from toontown.safezone.DistributedPicnicTableAI import DistributedPicnicTableAI

class OZHoodAI(SZHoodAI):
    HOOD = ToontownGlobals.OutdoorZone
    def __init__(self, air):    
     self.classicCharChip = None
     self.classicCharDale = None

    
    def createZone(self):
        SZHoodAI.createTreasurePlanner(self)
        self.timer = DistributedTimerAI(self.air)
        self.timer.generateWithRequired(self.HOOD)
        self.spawnObjects()
        if simbase.config.GetBool('want-classic-chars', True):
            if simbase.config.GetBool('want-chip-and-dale', True):
                self.createClassicChars()
        

    def spawnObjects(self):
        HoodAI.spawnObjects(self)
        filename = self.air.genDNAFileName(self.HOOD)
        self.air.dnaSpawner.spawnObjects(filename, self.HOOD)
        
    def createClassicChars(self):
        self.classicCharChip = DistributedChipAI.DistributedChipAI(self.air)
        self.classicCharChip.generateWithRequired(self.zoneId)
        self.classicCharChip.start()
        self.classicCharDale = DistributedDaleAI.DistributedDaleAI(self.air, self.classicCharChip.doId)
        self.classicCharDale.generateWithRequired(self.zoneId)
        self.classicCharDale.start()
        self.classicCharChip.setDaleId(self.classicCharDale.doId)
        
