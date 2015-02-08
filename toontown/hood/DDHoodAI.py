from toontown.classicchars import DistributedDonaldDockAI
from toontown.hood import HoodAI
from toontown.safezone import DistributedBoatAI
from toontown.safezone import DistributedTrolleyAI
from toontown.toonbase import ToontownGlobals
from toontown.ai import DistributedTrickOrTreatTargetAI
from toontown.ai import DistributedWinterCarolingTargetAI


class DDHoodAI(HoodAI.HoodAI):
    def __init__(self, air):
        HoodAI.HoodAI.__init__(self, air,
                               ToontownGlobals.DonaldsDock,
                               ToontownGlobals.DonaldsDock)

        self.trolley = None
        self.boat = None
        self.classicChar = None

        self.startup()

    def startup(self):
        HoodAI.HoodAI.startup(self)

        if simbase.config.GetBool('want-minigames', True):
            self.createTrolley()
        self.createBoat()
        if simbase.config.GetBool('want-classic-chars', True):
            if simbase.config.GetBool('want-donald-dock', True):
                self.createClassicChar()
                
        if simbase.air.wantHalloween:
            self.TrickOrTreatTargetManager = DistributedTrickOrTreatTargetAI.DistributedTrickOrTreatTargetAI(self.air)
            self.TrickOrTreatTargetManager.generateWithRequired(1834)
            
        if simbase.air.wantChristmas:
            self.WinterCarolingTargetManager = DistributedWinterCarolingTargetAI.DistributedWinterCarolingTargetAI(self.air)
            self.WinterCarolingTargetManager.generateWithRequired(1707)

    def createTrolley(self):
        self.trolley = DistributedTrolleyAI.DistributedTrolleyAI(self.air)
        self.trolley.generateWithRequired(self.zoneId)
        self.trolley.start()

    def createBoat(self):
        self.boat = DistributedBoatAI.DistributedBoatAI(self.air)
        self.boat.generateWithRequired(self.zoneId)
        self.boat.start()

    def createClassicChar(self):
        self.classicChar = DistributedDonaldDockAI.DistributedDonaldDockAI(self.air)
        self.classicChar.generateWithRequired(self.zoneId)
        self.classicChar.start()
