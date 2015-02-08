from toontown.classicchars import DistributedDonaldAI
from toontown.hood import HoodAI
from toontown.safezone import DistributedTrolleyAI
from toontown.toonbase import ToontownGlobals
from toontown.ai import DistributedResistanceEmoteMgrAI
from toontown.ai import DistributedTrickOrTreatTargetAI
from toontown.ai import DistributedWinterCarolingTargetAI


class DLHoodAI(HoodAI.HoodAI):
    def __init__(self, air):
        HoodAI.HoodAI.__init__(self, air,
                               ToontownGlobals.DonaldsDreamland,
                               ToontownGlobals.DonaldsDreamland)

        self.trolley = None
        self.classicChar = None

        self.startup()

    def startup(self):
        HoodAI.HoodAI.startup(self)

        if simbase.config.GetBool('want-minigames', True):
            self.createTrolley()
        if simbase.config.GetBool('want-classic-chars', True):
            if simbase.config.GetBool('want-donald-dreamland', True):
                self.createClassicChar()
        
        self.resistanceEmoteManager = DistributedResistanceEmoteMgrAI.DistributedResistanceEmoteMgrAI(self.air)
        self.resistanceEmoteManager.generateWithRequired(9720)
        
        if simbase.air.wantHalloween:
            self.TrickOrTreatTargetManager = DistributedTrickOrTreatTargetAI.DistributedTrickOrTreatTargetAI(self.air)
            self.TrickOrTreatTargetManager.generateWithRequired(9619)
        
        if simbase.air.wantChristmas:
            self.WinterCarolingTargetManager = DistributedWinterCarolingTargetAI.DistributedWinterCarolingTargetAI(self.air)
            self.WinterCarolingTargetManager.generateWithRequired(9720)

    def createTrolley(self):
        self.trolley = DistributedTrolleyAI.DistributedTrolleyAI(self.air)
        self.trolley.generateWithRequired(self.zoneId)
        self.trolley.start()

    def createClassicChar(self):
        self.classicChar = DistributedDonaldAI.DistributedDonaldAI(self.air)
        self.classicChar.generateWithRequired(self.zoneId)
        self.classicChar.start()
