from SZHoodAI import SZHoodAI
from toontown.hood.HoodAI import *
from toontown.toonbase import ToontownGlobals
#from toontown.election import DistributedFlippyStandAI
from toontown.election import DistributedToonfestTowerBaseAI
from toontown.safezone.DistributedPicnicBasketAI import DistributedPicnicBasketAI
from toontown.safezone.DistributedPicnicTableAI import DistributedPicnicTableAI

class TFHoodAI(SZHoodAI):
    HOOD = ToontownGlobals.FunnyFarm
    
    def createZone(self):
        SZHoodAI.createTreasurePlanner(self)
     #   self.flippyStand = DistributedFlippyStandAI.DistributedFlippyStandAI(self.air)
      #  self.flippyStand.generateWithRequired(self.HOOD)
        self.toonfestTower = DistributedToonfestTowerBaseAI.DistributedToonfestTowerBaseAI(self.air)
        self.toonfestTower.generateWithRequired(self.HOOD)
