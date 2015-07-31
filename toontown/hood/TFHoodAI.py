#Embedded file name: toontown.hood.TFHoodAI
from SZHoodAI import SZHoodAI
from toontown.hood.HoodAI import *
from toontown.toonbase import ToontownGlobals
from toontown.safezone.DistributedPicnicBasketAI import DistributedPicnicBasketAI
from toontown.safezone.DistributedPicnicTableAI import DistributedPicnicTableAI
from toontown.distributed.DistributedTimerAI import DistributedTimerAI
from toontown.election import DistributedFlippyStandAI
from toontown.election import DistributedToonfestBalloonAI
from toontown.election import DistributedToonfestTowerBaseAI
from toontown.election import DistributedToonfestCogAI
from direct.fsm.FSM import FSM
from pandac.PandaModules import *

class TFHoodAI(SZHoodAI):
    notify = directNotify.newCategory('SZHoodAI')
    notify.setInfo(True)
    HOOD = ToontownGlobals.ToonFest

    def createZone(self):
        self.notify.info('Creating zone... ToonFest')
        SZHoodAI.createZone(self, False)
        self.spawnObjects()
        self.timer = DistributedTimerAI(self.air)
        self.timer.generateWithRequired(self.HOOD)
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
