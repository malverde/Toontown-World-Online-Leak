from toontown.classicchars import DistributedMickeyAI
from toontown.hood import HoodAI
from toontown.safezone import ButterflyGlobals
from toontown.safezone import DistributedButterflyAI
from toontown.safezone import DistributedTrolleyAI
from toontown.toon import NPCToons
from toontown.toonbase import TTLocalizer
from toontown.toonbase import ToontownGlobals
from toontown.ai import DistributedTrickOrTreatTargetAI
from toontown.ai import DistributedWinterCarolingTargetAI
#from toontown.election.DistributedElectionEventAI import DistributedElectionEventAI


class TTHoodAI(HoodAI.HoodAI):
    def __init__(self, air):
        HoodAI.HoodAI.__init__(self, air,
                               ToontownGlobals.ToontownCentral,
                               ToontownGlobals.ToontownCentral)

        self.trolley = None
        self.classicChar = None

        self.startup()

    def startup(self):
        HoodAI.HoodAI.startup(self)

        if simbase.config.GetBool('want-minigames', True):
            self.createTrolley()
        if simbase.config.GetBool('want-classic-chars', True):
            if simbase.config.GetBool('want-mickey', True):
                self.createClassicChar()
        if simbase.config.GetBool('want-butterflies', True):
            self.createButterflies()
        if self.air.config.GetBool('want-doomsday', False):
            self.spawnElection()


        if simbase.air.wantYinYang:
            NPCToons.createNPC(
                simbase.air, 2021,
                (ToontownGlobals.ToontownCentral, TTLocalizer.NPCToonNames[2021], ('css', 'ms', 'm', 'm', 26, 0, 26, 26, 0, 27, 0, 27, 0, 27), 'm', 1, NPCToons.NPC_YIN),
                ToontownGlobals.ToontownCentral, posIndex=0)
            NPCToons.createNPC(
                simbase.air, 2022,
                (ToontownGlobals.ToontownCentral, TTLocalizer.NPCToonNames[2022], ('bss', 'ms', 'm', 'm', 0, 0, 0, 0, 0, 31, 0, 31, 0, 31), 'm', 1, NPCToons.NPC_YANG),
                ToontownGlobals.ToontownCentral, posIndex=0)
                
        if simbase.air.wantHalloween:
            self.TrickOrTreatTargetManager = DistributedTrickOrTreatTargetAI.DistributedTrickOrTreatTargetAI(self.air)
            self.TrickOrTreatTargetManager.generateWithRequired(2649)
        
        if simbase.air.wantChristmas:
            self.WinterCarolingTargetManager = DistributedWinterCarolingTargetAI.DistributedWinterCarolingTargetAI(self.air)
            self.WinterCarolingTargetManager.generateWithRequired(2659)

    def shutdown(self):
        HoodAI.HoodAI.shutdown(self)

        ButterflyGlobals.clearIndexes(self.zoneId)

    def createTrolley(self):
        self.trolley = DistributedTrolleyAI.DistributedTrolleyAI(self.air)
        self.trolley.generateWithRequired(self.zoneId)
        self.trolley.start()

    def createClassicChar(self):
        self.classicChar = DistributedMickeyAI.DistributedMickeyAI(self.air)
        self.classicChar.generateWithRequired(self.zoneId)
        self.classicChar.start()

    def createButterflies(self):
        ButterflyGlobals.generateIndexes(self.zoneId, ButterflyGlobals.TTC)
        for i in xrange(0, ButterflyGlobals.NUM_BUTTERFLY_AREAS[ButterflyGlobals.TTC]):
            for _ in xrange(0, ButterflyGlobals.NUM_BUTTERFLIES[ButterflyGlobals.TTC]):
                butterfly = DistributedButterflyAI(self.air, playground, i, self.zoneId)
                butterfly.generateWithRequired(self.zoneId)
                butterfly.start()
