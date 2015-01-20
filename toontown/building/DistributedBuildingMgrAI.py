import os
from direct.task.Task import Task
import cPickle
from otp.ai.AIBaseGlobal import *
import DistributedBuildingAI
import HQBuildingAI
import GagshopBuildingAI
#import PetshopBuildingAI
from toontown.building.KartShopBuildingAI import KartShopBuildingAI
#from toontown.building import DistributedAnimBuildingAI
from direct.directnotify import DirectNotifyGlobal
from toontown.hood import ZoneUtil
import time
import random

class DistributedBuildingMgrAI:
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBuildingMgrAI')

    def __init__(self, air, branchID, dnaStore, trophyMgr):
        self.branchID = branchID
        self.canonicalBranchID = ZoneUtil.getCanonicalZoneId(branchID)
        self.air = air
        self.__buildings = {}
        self.dnaStore = dnaStore
        self.trophyMgr = trophyMgr
        self.findAllLandmarkBuildings()
        self.doLaterTask = None
        self.air.buildingManagers[branchID] = self
        return

    def cleanup(self):
        taskMgr.remove(str(self.branchID) + '_delayed_save-timer')
        for building in self.__buildings.values():
            building.cleanup()

        self.__buildings = {}

    def isValidBlockNumber(self, blockNumber):
        return self.__buildings.has_key(blockNumber)

    def delayedSaveTask(self, task):
        self.save()
        self.doLaterTask = None
        return Task.done

    def isSuitBlock(self, blockNumber):
        return self.__buildings[blockNumber].isSuitBlock()

    def getSuitBlocks(self):
        blocks = []
        for i in self.__buildings.values():
            if i.isSuitBlock():
                blocks.append(i.getBlock()[0])

        return blocks

    def getEstablishedSuitBlocks(self):
        blocks = []
        for i in self.__buildings.values():
            if i.isEstablishedSuitBlock():
                blocks.append(i.getBlock()[0])

        return blocks

    def getToonBlocks(self):
        blocks = []
        for i in self.__buildings.values():
            if isinstance(i, HQBuildingAI.HQBuildingAI):
                continue
            if not i.isSuitBlock():
                blocks.append(i.getBlock()[0])

        return blocks

    def getBuildings(self):
        return self.__buildings.values()

    def getFrontDoorPoint(self, blockNumber):
        return self.__buildings[blockNumber].getFrontDoorPoint()

    def getBuildingTrack(self, blockNumber):
        return self.__buildings[blockNumber].track

    def getBuilding(self, blockNumber):
        return self.__buildings[blockNumber]

    def setFrontDoorPoint(self, blockNumber, point):
        return self.__buildings[blockNumber].setFrontDoorPoint(point)

    def getDNABlockLists(self):
        blocks = []
        hqBlocks = []
        gagshopBlocks = []
        petshopBlocks = []
        kartshopBlocks = []
        animBldgBlocks = []
        for blockId, block in self.dnaStore.getBlocks():
            blockNumber = blockId
            buildingType = block.buildingType
            if buildingType == 'hq':
                hqBlocks.append(blockNumber)
            elif buildingType == 'gagshop':
                gagshopBlocks.append(blockNumber)
            elif buildingType == 'petshop':
                petshopBlocks.append(blockNumber)
            elif buildingType == 'kartshop':
                kartshopBlocks.append(blockNumber)
            elif buildingType == 'animbldg':
                animBldgBlocks.append(blockNumber)
            else:
                blocks.append(blockNumber)

        return (blocks,
         hqBlocks,
         gagshopBlocks,
         petshopBlocks,
         kartshopBlocks,
         animBldgBlocks)

    def findAllLandmarkBuildings(self):
        backups = simbase.backups.load('blockinfo', (self.air.districtId, self.branchID), default={})
        (blocks, hqBlocks, gagshopBlocks, petshopBlocks, kartshopBlocks, animBldgBlocks) = self.getDNABlockLists()
        for block in blocks:
            self.newBuilding(block, backup=backups.get(block, None))

        for block in animBldgBlocks:
            self.newAnimBuilding(block, buildings.get(block, None))

        for block in hqBlocks:
            self.newHQBuilding(block)

        for block in gagshopBlocks:
            self.newGagshopBuilding(block)

        if simbase.wantPets:
            for block in petshopBlocks:
                self.newPetshopBuilding(block)

        if simbase.wantKarts:
            for block in kartshopBlocks:
                self.newKartShopBuilding(block)

        return

    def newBuilding(self, blockNumber, backup=None):
        building = DistributedBuildingAI.DistributedBuildingAI(
            self.air, blockNumber, self.branchID, self.trophyMgr)
        building.generateWithRequired(self.branchID)
        if backup is not None:
                building.track = backup.get('track', 'c')
                building.difficulty = backup.get('difficulty', 1)
                building.numFloors = backup.get('numFloors', 1)
                building.updateSavedBy(backup.get('savedBy'))
                building.becameSuitTime = backup.get('becameSuitTime', time.mktime(time.gmtime()))
                if ['state'] == 'suit':
                    building.setState('suit')
                elif ['state'] == 'cogdo':
                    building.setState('cogdo')
                else:
                    building.setState('toon')
        else:
            building.setState('toon')
        self.__buildings[blockNumber] = building
        return building

    def newAnimBuilding(self, blockNumber, blockData = None):
        return
        building = DistributedAnimBuildingAI.DistributedAnimBuildingAI(self.air, blockNumber, self.branchID, self.trophyMgr)
        building.generateWithRequired(self.branchID)
        if blockData:
            building.track = blockData.get('track', 'c')
            building.difficulty = int(blockData.get('difficulty', 1))
            building.numFloors = int(blockData.get('numFloors', 1))
            if not ZoneUtil.isWelcomeValley(building.zoneId):
                building.updateSavedBy(blockData.get('savedBy'))
            else:
                self.notify.warning('we had a cog building in welcome valley %d' % building.zoneId)
            building.becameSuitTime = blockData.get('becameSuitTime', time.time())
            if blockData['state'] == 'suit':
                building.setState('suit')
            else:
                building.setState('toon')
        else:
            building.setState('toon')
        self.__buildings[blockNumber] = building
        return building

    def newHQBuilding(self, blockNumber):
        dnaStore = self.air.dnaStoreMap[self.canonicalBranchID]
        exteriorZoneId = dnaStore.getBlock(blockNumber).zone
        exteriorZoneId = ZoneUtil.getTrueZoneId(exteriorZoneId, self.branchID)
        interiorZoneId = self.branchID - self.branchID % 100 + 500 + blockNumber
        self.notify.debug("Spawning HQ ext: {0} int: {1}".format(exteriorZoneId, interiorZoneId))
        building = HQBuildingAI.HQBuildingAI(self.air, exteriorZoneId, interiorZoneId, blockNumber)
        self.__buildings[blockNumber] = building
        return building

    def newGagshopBuilding(self, blockNumber):
        dnaStore = self.air.dnaStoreMap[self.canonicalBranchID]
        exteriorZoneId = dnaStore.getBlock(blockNumber).zone
        exteriorZoneId = ZoneUtil.getTrueZoneId(exteriorZoneId, self.branchID)
        interiorZoneId = self.branchID - self.branchID % 100 + 500 + blockNumber
        self.notify.debug("Spawning GagShop ext: {0} int: {1}".format(exteriorZoneId, interiorZoneId))
        building = GagshopBuildingAI.GagshopBuildingAI(self.air, exteriorZoneId, interiorZoneId, blockNumber)
        self.__buildings[blockNumber] = building
        return building

    def newPetshopBuilding(self, blockNumber):
        return
        dnaStore = self.air.dnaStoreMap[self.canonicalBranchID]
        exteriorZoneId = dnaStore.getBlock(blockNumber).zone
        exteriorZoneId = ZoneUtil.getTrueZoneId(exteriorZoneId, self.branchID)
        interiorZoneId = self.branchID - self.branchID % 100 + 500 + blockNumber
        building = PetshopBuildingAI.PetshopBuildingAI(self.air, exteriorZoneId, interiorZoneId, blockNumber)
        self.__buildings[blockNumber] = building
        return building

    def newKartShopBuilding(self, blockNumber):
        dnaStore = self.air.dnaStoreMap[self.canonicalBranchID]
        exteriorZoneId = dnaStore.getBlock(blockNumber).zone
        exteriorZoneId = ZoneUtil.getTrueZoneId(exteriorZoneId, self.branchID)
        interiorZoneId = self.branchID - self.branchID % 100 + 500 + blockNumber
        building = KartShopBuildingAI(self.air, exteriorZoneId, interiorZoneId, blockNumber)
        self.__buildings[blockNumber] = building
        return building


    def save(self):
        buildings = {}
        for blockNumber in self.getSuitBlocks():
            building = self.getBuilding(blockNumber)
            backup = {
                'state': building.fsm.getCurrentState().getName(),
                'block': building.block,
                'track': building.track,
                'difficulty': building.difficulty,
                'numFloors': building.numFloors,
                'savedBy': building.savedBy,
                'becameSuitTime': building.becameSuitTime
            }
            buildings[blockNumber] = backup
        simbase.backups.save('blockinfo', (self.air.districtId, self.branchID), buildings)
