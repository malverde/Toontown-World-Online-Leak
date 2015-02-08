from toontown.toonbase import ToontownGlobals
from SZHoodAI import SZHoodAI
from toontown.toon import NPCToons
from toontown.classicchars import DistributedDonaldAI
class DLHoodAI(SZHoodAI):
    HOOD = ToontownGlobals.DonaldsDreamland
    self.classicChar = None
    
    def createZone(self):
        SZHoodAI.createZone(self)
        if simbase.config.GetBool('want-classic-chars', True):
            if simbase.config.GetBool('want-donald-dreamland', True):
                self.createClassicChar()
        
        self.spawnObjects()
    def createClassicChar(self):
        self.classicChar = DistributedDonaldAI.DistributedDonaldAI(self.air)
        self.classicChar.generateWithRequired(self.zoneId)
        self.classicChar.start()
