from SZHoodAI import SZHoodAI
from toontown.hood.HoodAI import *
from toontown.toonbase import ToontownGlobals
from toontown.election import DistributedFlippyStandAI
from toontown.election import DistributedToonfestTowerBaseAI
from toontown.election import DistributedToonfestCogAI
from toontown.election import DistributedToonfestBalloonAI
from toontown.safezone.DistributedPicnicBasketAI import DistributedPicnicBasketAI
from toontown.safezone.DistributedPicnicTableAI import DistributedPicnicTableAI
from toontown.distributed.DistributedTimerAI import DistributedTimerAI

class TFHoodAI(SZHoodAI):
    HOOD = ToontownGlobals.FunnyFarm
    
    def createZone(self):
        SZHoodAI.createTreasurePlanner(self)
        self.flippyStand = DistributedFlippyStandAI.DistributedFlippyStandAI(self.air)
        self.flippyStand.generateWithRequired(self.HOOD)
        self.toonfestTower = DistributedToonfestTowerBaseAI.DistributedToonfestTowerBaseAI(self.air)
        self.toonfestTower.generateWithRequired(self.HOOD)
        self.balloon = DistributedToonfestBalloonAI.DistributedToonfestBalloonAI(self.air)
        self.balloon.generateWithRequired(self.HOOD)
        self.balloon.b_setState('Waiting')

        self.cogs = []
        
    def createCogs(self):
        posList = [[224,
          -146,
          4.597,
          1]]
        for pos in posList:
            self.cog = DistributedToonfestCogAI.DistributedToonfestCogAI(self.air)
            self.cog.generateWithRequired(self.HOOD)
            self.cog.setPos(pos[0], pos[1], pos[2])
            self.cog.setId(pos[3])
            self.cogs.append(self.cog)
