from direct.directnotify import DirectNotifyGlobal
from toontown.estate.DistributedLawnDecorAI import DistributedLawnDecorAI
import GardenGlobals

class DistributedPlantBaseAI(DistributedLawnDecorAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPlantBaseAI')

    def __init__(self, mgr):
        DistributedLawnDecorAI.__init__(self, mgr)
        self.typeIndex = 0
        self.waterLevel = 0
        self.growthLevel = 0
    
    def setTypeIndex(self, typeIndex):
        self.typeIndex = typeIndex
        self.attributes = GardenGlobals.PlantAttributes[typeIndex]
        self.growthThresholds = self.attributes['growthThresholds']
        
    def d_setTypeIndex(self, typeIndex):
        self.sendUpdate('setTypeIndex', [typeIndex])
        
    def b_setTypeIndex(self, typeIndex):
        self.setTypeIndex(typeIndex)
        self.d_setTypeIndex(typeIndex)
        
    def getTypeIndex(self):
        return self.typeIndex

    def setWaterLevel(self, waterLevel):
        self.waterLevel = waterLevel
       
    def d_setWaterLevel(self, waterLevel):
        self.sendUpdate('setWaterLevel', [waterLevel])
        
    def b_setWaterLevel(self, waterLevel):
        self.setWaterLevel(waterLevel)
        self.d_setWaterLevel(waterLevel)
        
    def getWaterLevel(self):
        return self.waterLevel

    def setGrowthLevel(self, growthLevel):
        self.growthLevel = growthLevel
        
    def d_setGrowthLevel(self, growthLevel):
        self.sendUpdate('setGrowthLevel', [growthLevel])
        
    def b_setGrowthLevel(self, growthLevel):
        self.setGrowthLevel(growthLevel)
        self.d_setGrowthLevel(growthLevel)
        
    def getGrowthLevel(self):
        return self.growthLevel

    def waterPlant(self):
        av = self.air.doId2do.get(self.air.getAvatarIdFromSender())
        if not av:
            return
            
        level = max(1, self.getWaterLevel() + av.getWateringCan() + 1)
        level = min(20, level)
        self.b_setWaterLevel(level)
        
        self.d_setMovie(GardenGlobals.MOVIE_WATER)
        self.update()

    def waterPlantDone(self):
        av = self.air.doId2do.get(self.air.getAvatarIdFromSender())
        if not av:
            return
        
        if self.waterLevel < 6:
            av.b_setWateringCanSkill(av.getWateringCanSkill() + 1)
        else:
            av.b_setWateringCanSkill(av.getWateringCanSkill())
            
        self.d_setMovie(GardenGlobals.MOVIE_CLEAR)
        
    def update(self):
        pass
        