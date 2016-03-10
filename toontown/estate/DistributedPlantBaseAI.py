from toontown.estate.DistributedLawnDecorAI import DistributedLawnDecorAI
from toontown.estate import GardenGlobals


class DistributedPlantBaseAI(DistributedLawnDecorAI):
    notify = directNotify.newCategory("DistributedPlantBaseAI")

    def __init__(self, air, gardenManager, ownerIndex):
        DistributedLawnDecorAI.__init__(self, air, gardenManager, ownerIndex)

        self.typeIndex = None
        self.waterLevel = None
        self.growthLevel = None
        self.timestamp = None

    def d_setTypeIndex(self, index):
        self.sendUpdate('setTypeIndex', [index])

    def getTypeIndex(self):
        return self.typeIndex

    def d_setWaterLevel(self, waterLevel):
        self.sendUpdate('setWaterLevel', [waterLevel])

    def getWaterLevel(self):
        return self.waterLevel

    def d_setGrowthLevel(self, growthLevel):
        self.sendUpdate('setGrowthLevel', [growthLevel])

    def getGrowthLevel(self):
        return self.growthLevel

    def getGrowthThresholds(self):
        return GardenGlobals.PlantAttributes[self.typeIndex]['growthThresholds']

    def getGrowthState(self):
        state = 0
        for v in self.getGrowthThresholds():
            if self.growthLevel >= v:
                state += 1
        return state

    def waterPlant(self):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)
        if not av:
            return

        if self.waterLevel < GardenGlobals.getMaxWateringCanPower():
            self.waterLevel += GardenGlobals.getWateringCanPower(av.wateringCan, av.wateringCanSkill)
            self.d_setWaterLevel(self.waterLevel)

            self.gardenManager.updateGardenData()

        self.setMovie(GardenGlobals.MOVIE_WATER, self.air.getAvatarIdFromSender())

    def waterPlantDone(self):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)
        if not av:
            return

        currSkill = av.getWateringCanSkill()
        if self.waterLevel < GardenGlobals.getMaxWateringCanPower():
            av.b_setWateringCanSkill(currSkill + 1 + self.getGrowthState())

        self.setMovie(GardenGlobals.MOVIE_CLEAR, self.air.getAvatarIdFromSender())

    def construct(self, gardenData):
        DistributedLawnDecorAI.construct(self, gardenData)

        self.typeIndex = gardenData.getUint8()
        self.waterLevel = gardenData.getInt8()
        self.growthLevel = gardenData.getInt8()

        self.timestamp = gardenData.getUint32()

        self.updateFromTimestamp()

    def updateFromTimestamp(self):
        seconds = self.gardenManager.getTimestamp() - self.timestamp
        cycles = seconds / GardenGlobals.GROWTH_INTERVAL
        unwateredCycles = abs(self.growthLevel - cycles)
        self.waterLevel = max(self.waterLevel - unwateredCycles, -1)
        if self.waterLevel < 0:
            # This tree is wilted, don't grow it.
            return

        if self.waterLevel > 127:
            # Oh no, a broken garden!
            self.waterLevel = 0

        self.growthLevel = min(cycles, GardenGlobals.MAX_GROWTH_LEVEL)

    def pack(self, gardenData):
        DistributedLawnDecorAI.pack(self, gardenData)

        gardenData.addUint8(self.typeIndex)
        gardenData.addInt8(self.waterLevel)
        gardenData.addInt8(self.growthLevel)
        gardenData.addUint32(self.timestamp)
