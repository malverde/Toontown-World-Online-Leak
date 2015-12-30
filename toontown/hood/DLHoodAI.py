from toontown.toonbase import ToontownGlobals
from SZHoodAI import SZHoodAI
from toontown.toon import NPCToons
from toontown.ai import DistributedResistanceEmoteMgrAI
from toontown.ai import DistributedTrickOrTreatTargetAI


class DLHoodAI(SZHoodAI):
    HOOD = ToontownGlobals.DonaldsDreamland

    def createZone(self):
        SZHoodAI.createZone(self)

        self.spawnObjects()

        self.resistanceEmoteManager = DistributedResistanceEmoteMgrAI.DistributedResistanceEmoteMgrAI(self.air)
        self.resistanceEmoteManager.generateWithRequired(9720)

        if simbase.air.wantHalloween:
            self.TrickOrTreatTargetManager = DistributedTrickOrTreatTargetAI.DistributedTrickOrTreatTargetAI(self.air)
            self.TrickOrTreatTargetManager.generateWithRequired(9619)
