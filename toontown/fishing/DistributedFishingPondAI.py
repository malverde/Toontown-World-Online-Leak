from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from toontown.safezone.DistributedFishingSpotAI import DistributedFishingSpotAI
from toontown.fishing.DistributedFishingTargetAI import DistributedFishingTargetAI
from toontown.fishing.DistributedPondBingoManagerAI import DistributedPondBingoManagerAI
from toontown.fishing import FishingTargetGlobals
from toontown.hood import ZoneUtil
from toontown.toon import NPCToons

class DistributedFishingPondAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedFishingPondAI")
	
    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.area = None
        self.targets = {}
        self.spots = {}
        self.bingoMgr = None
        
    def start(self):
        for _ in range(FishingTargetGlobals.getNumTargets(self.area)):
            fishingTarget = DistributedFishingTargetAI(simbase.air)
            fishingTarget.setPondDoId(self.doId)
            fishingTarget.generateWithRequired(self.zoneId)

    def hitTarget(self, target):
        avId = self.air.getAvatarIdFromSender()
        if self.targets.get(target) == None:
            self.air.writeServerEvent('suspicious', avId=avId, issue='Toon tried to hit nonexistent fishing target!')
            return
        spot = self.hasToon(avId)
        if spot:
            spot.rewardIfValid(target)
            return
        self.air.writeServerEvent('suspicious', avId=avId, issue='Toon tried to catch fish while not fishing!')
    def addTarget(self, target):
         self.targets[target.doId] = target

    def addSpot(self, spot):
         self.spots[spot.doId] = spot

    def setArea(self, area):
        self.area = area

    def getArea(self):
        return self.area
        
    def hasToon(self, avId):
        for spot in self.spots:
            if self.spots[spot].avId == avId:
                return self.spots[spot]
        return
  