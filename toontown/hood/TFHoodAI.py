from SZHoodAI import SZHoodAI
from toontown.hood.HoodAI import *
from toontown.toonbase import ToontownGlobals
from toontown.safezone.DistributedPicnicBasketAI import DistributedPicnicBasketAI
from toontown.safezone.DistributedPicnicTableAI import DistributedPicnicTableAI

class TFHoodAI(SZHoodAI):
    HOOD = ToontownGlobals.FunnyFarm
    
    def createZone(self):
        SZHoodAI.createTreasurePlanner(self)
