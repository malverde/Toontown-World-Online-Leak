from toontown.toonbase import ToontownGlobals
from SZHoodAI import SZHoodAI
from toontown.toon import NPCToons
from toontown.ai import DistributedTrickOrTreatTargetAI


class MMHoodAI(SZHoodAI):
    HOOD = ToontownGlobals.MinniesMelodyland

    def createZone(self):
        SZHoodAI.createZone(self)
        self.spawnObjects()

        if simbase.air.wantHalloween:
            self.TrickOrTreatTargetManager = DistributedTrickOrTreatTargetAI.DistributedTrickOrTreatTargetAI(self.air)
            self.TrickOrTreatTargetManager.generateWithRequired(4835)
