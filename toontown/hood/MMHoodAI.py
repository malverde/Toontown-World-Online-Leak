from toontown.toonbase import ToontownGlobals
from SZHoodAI import SZHoodAI
from toontown.toon import NPCToons
from toontown.classicchars import DistributedMinnieAI
class MMHoodAI(SZHoodAI):
    HOOD = ToontownGlobals.MinniesMelodyland
    self.classicChar = None
    def createZone(self):
        SZHoodAI.createZone(self)        
        self.spawnObjects()
        if simbase.config.GetBool('want-classic-chars', True):
            if simbase.config.GetBool('want-minnie', True):
                self.createClassicChar        
    def createClassicChar(self):
        self.classicChar = DistributedMinnieAI.DistributedMinnieAI(self.air)
        self.classicChar.generateWithRequired(self.zoneId)
        self.classicChar.start()
