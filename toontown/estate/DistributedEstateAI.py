#Embedded file name: toontown.estate.DistributedEstateAI
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from toontown.toonbase import ToontownGlobals
import HouseGlobals
import time, random

from toontown.fishing.DistributedFishingPondAI import DistributedFishingPondAI
from toontown.fishing import FishingTargetGlobals
from toontown.fishing.DistributedPondBingoManagerAI import DistributedPondBingoManagerAI
from toontown.fishing.DistributedFishingTargetAI import DistributedFishingTargetAI
from toontown.safezone import TreasureGlobals
from toontown.safezone.SZTreasurePlannerAI import SZTreasurePlannerAI

from toontown.safezone.DistributedFishingSpotAI import DistributedFishingSpotAI

from DistributedGardenBoxAI import *
from DistributedGardenPlotAI import *
from DistributedGagTreeAI import *
from DistributedFlowerAI import *
from DistributedStatuaryAI import *
from DistributedToonStatuaryAI import *
from DistributedAnimatedStatuaryAI import *
from DistributedChangingStatuaryAI import *
import GardenGlobals

from DistributedCannonAI import *
from DistributedTargetAI import *
import CannonGlobals


# planted, waterLevel, lastCheck, growthLevel, optional
NULL_PLANT = [-1, -1, 0, 0, 0]
NULL_TREES = [NULL_PLANT] * 8
NULL_FLOWERS = [NULL_PLANT] * 10
NULL_STATUARY = 0

NULL_DATA = {'trees': NULL_TREES, 'statuary': NULL_STATUARY, 'flowers': NULL_FLOWERS}

from direct.distributed.PyDatagramIterator import *
from direct.distributed.PyDatagram import *

class Garden:
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedEstateAI')

    WANT_FLOWERS = True # puke
    WANT_TREES = True
    WANT_STATUARY = True

    def __init__(self, air, avId):
        self.air = air
        self.avId = avId
        self.trees = set()
        self.flowers = set()
        self.objects = set()

        self.data = NULL_DATA.copy()
        self.data.pop('_id', None)

    def destroy(self):
        messenger.send('garden-%d-666-going-down' % self.avId)

        for tree in self.trees:
            tree.requestDelete()

        for flower in self.flowers:
            flower.requestDelete()

        for object in self.objects:
            object.requestDelete()

        self.air = None
        self.estateMgr = None

    def create(self, estateMgr):
        self.estateMgr = estateMgr

        if self.avId not in estateMgr.toons:
            estateMgr.notify.warning('Garden associated to unknown avatar %d, deleting...' % self.avId)
            return False

        houseIndex = estateMgr.toons.index(self.avId)

        if self.WANT_FLOWERS:
            boxIndex = 0
            boxes = []
            boxDefs = GardenGlobals.estateBoxes[houseIndex]
            for x, y, h, boxType in boxDefs:
                box = DistributedGardenBoxAI(self)

                box.setTypeIndex(boxType)
                box.setPos(x, y, 0)
                box.setH(h)
                box.setOwnerIndex(houseIndex)
                box.generateWithRequired(estateMgr.zoneId)

                self.objects.add(box)
                boxes.append(box)
                boxIndex += 1

            self._boxes = boxes

        plots = GardenGlobals.estatePlots[houseIndex]
        treeIndex = 0
        flowerIndex = 0
        for plot, (x, y, h, type) in enumerate(plots):
            if type == GardenGlobals.GAG_TREE_TYPE and self.WANT_TREES:
                data = self.data['trees'][treeIndex]

                planted, waterLevel, lastCheck, growthLevel, lastHarvested = data

                if planted != -1:
                    obj = self.plantTree(treeIndex, planted, waterLevel=waterLevel,
                                         lastCheck=lastCheck, growthLevel=growthLevel,
                                         lastHarvested=lastHarvested, generate=False)

                    self.trees.add(obj)

                else:
                    obj = self.placePlot(treeIndex)

                obj.setPos(x, y, 0)
                obj.setH(h)
                obj.setPlot(plot)
                obj.setOwnerIndex(houseIndex)
                obj.generateWithRequired(estateMgr.zoneId)
                treeIndex += 1

            elif type == GardenGlobals.FLOWER_TYPE and self.WANT_FLOWERS:
                data = self.data['flowers'][flowerIndex]

                planted, waterLevel, lastCheck, growthLevel, variety = data

                if planted != -1:
                    obj = self.plantFlower(flowerIndex, planted, variety, waterLevel=waterLevel,
                                           lastCheck=lastCheck, growthLevel=growthLevel,
                                           generate=False)

                else:
                    obj = self.placePlot(flowerIndex)
                    obj.flowerIndex = flowerIndex

                obj.setPlot(plot)
                obj.setOwnerIndex(houseIndex)
                obj.generateWithRequired(estateMgr.zoneId)

                index = (0, 1, 2, 2, 2, 3, 3, 3, 4, 4)[flowerIndex]
                idx = (0, 0, 0, 1, 2, 0, 1, 2, 0, 1)[flowerIndex]
                obj.sendUpdate('setBoxDoId', [boxes[index].doId, idx])
                flowerIndex += 1

            elif type == GardenGlobals.STATUARY_TYPE and self.WANT_STATUARY:
                data = self.data['statuary']
                if data == 0:
                    obj = self.placePlot(-1)

                else:
                    obj = self.placeStatuary(data, generate=False)

                obj.setPos(x, y, 0)
                obj.setH(h)
                obj.setPlot(plot)
                obj.setOwnerIndex(houseIndex)
                obj.generateWithRequired(estateMgr.zoneId)

        for tree in self.trees:
            tree.calcDependencies()

        self.reconsiderAvatarOrganicBonus()

        return True

    def hasTree(self, track, index):
        x = track * 7 + index
        for tree in self.data['trees']:
            if tree[0] == x:
                return True

        return False

    def getTree(self, track, index):
        for tree in self.trees:
            if tree.typeIndex == track * 7 + index:
                return tree

    def plantTree(self, treeIndex, value, plot=None, waterLevel=-1,
                  lastCheck=0, growthLevel=0, lastHarvested=0,
                  ownerIndex=-1, plotId=-1, pos=None, generate=True):
        if not self.air:
            return

        if plot:
            if plot not in self.objects:
                return

            plot.requestDelete()
            self.objects.remove(plot)

        tree = DistributedGagTreeAI(self)

        tree.setTypeIndex(value)
        tree.setWaterLevel(waterLevel)
        tree.setGrowthLevel(growthLevel)
        if ownerIndex != -1:
            tree.setOwnerIndex(ownerIndex)

        if plotId != -1:
            tree.setPlot(plotId)

        if pos is not None:
            pos, h = pos
            tree.setPos(pos)
            tree.setH(h)

        tree.treeIndex = treeIndex
        tree.calculate(lastHarvested, lastCheck)
        self.trees.add(tree)

        if generate:
            tree.generateWithRequired(self.estateMgr.zoneId)

        return tree

    def placePlot(self, treeIndex):
        obj = DistributedGardenPlotAI(self)
        obj.treeIndex = treeIndex
        self.objects.add(obj)

        return obj

    def plantFlower(self, flowerIndex, species, variety, plot=None, waterLevel=-1,
                    lastCheck=0, growthLevel=0, ownerIndex=-1, plotId=-1, generate=True):
        if not self.air:
            return

        if plot:
            if plot not in self.objects:
                return

            plot.requestDelete()
            self.objects.remove(plot)

        flower = DistributedFlowerAI(self)

        flower.setTypeIndex(species)
        flower.setVariety(variety)
        flower.setWaterLevel(waterLevel)
        flower.setGrowthLevel(growthLevel)
        if ownerIndex != -1:
            flower.setOwnerIndex(ownerIndex)

        if plotId != -1:
            flower.setPlot(plotId)

        flower.flowerIndex = flowerIndex
        flower.calculate(lastCheck)
        self.flowers.add(flower)

        if generate:
            flower.generateWithRequired(self.estateMgr.zoneId)

        return flower

    def placeStatuary(self, data, plot=None, plotId=-1, ownerIndex=-1,
                      pos=None, generate=True):
        if not self.air:
            return

        if plot:
            if plot not in self.objects:
                return

            plot.requestDelete()
            self.objects.remove(plot)

        data, lastCheck, index, growthLevel = self.S_unpack(data)

        dclass = DistributedStatuaryAI
        if index in GardenGlobals.ToonStatuaryTypeIndices:
            dclass = DistributedToonStatuaryAI

        elif index in GardenGlobals.ChangingStatuaryTypeIndices:
            dclass = DistributedChangingStatuaryAI

        elif index in GardenGlobals.AnimatedStatuaryTypeIndices:
            dclass = DistributedAnimatedStatuaryAI

        obj = dclass(self)
        obj.growthLevel = growthLevel
        obj.index = index
        obj.data = data

        if ownerIndex != -1:
            obj.setOwnerIndex(ownerIndex)

        if plotId != -1:
            obj.setPlot(plotId)

        if pos is not None:
            pos, h = pos
            obj.setPos(pos)
            obj.setH(h)

        obj.calculate(lastCheck)

        self.objects.add(obj)

        if generate:
            obj.announceGenerate()

        return obj

    # Data structure
    # VERY HIGH (vh) (64-bit)
    #    high high (H) = data (32-bit)
    #    high low (L) = lastCheck (32-bit)
    # VERY LOW (vl) (16-bit)
    #    low high (h) = index (8-bit)
    #    low low (l) = growthLevel (8-bit)

    @staticmethod
    def S_pack(data, lastCheck, index, growthLevel):
        vh = data << 32 | lastCheck
        vl = index << 8 | growthLevel

        return vh << 16 | vl

    @staticmethod
    def S_unpack(x):
        vh = x >> 16
        vl = x & 0xFFFF

        data = vh >> 32
        lastCheck = vh & 0xFFFFFFFF

        index = vl >> 8
        growthLevel = vl & 0xFF

        return data, lastCheck, index, growthLevel

    def getNullPlant(self):
        return NULL_PLANT

    def reconsiderAvatarOrganicBonus(self):
        av = self.air.doId2do.get(self.avId)
        if not av:
            return

        bonus = [-1] * 7
        for track in xrange(7):
            for level in xrange(8):  # 7
                if not self.hasTree(track, level):
                    break

                tree = self.getTree(track, level)
                if tree.getGrowthLevel() < tree.growthThresholds[1] or tree.getWilted():
                    break

            bonus[track] = level - 1

        av.b_setTrackBonusLevel(bonus)

    def update(self):
        print self.data
        # dclass = self.air.dclassesByName['DistributedGardenAI']
        # self.air.dbInterface.updateObject(self.air.dbId, dclass, sendNewProp, data)
        # self.air.dbGlobalCursor.gardens.update({'avId': self.avId}, {'$set': self.data}, upsert=True)

class GardenManager:
    def __init__(self, mgr):
        self.mgr = mgr
        self.gardens = {}

    def handleSingleGarden(self, avId):
        g = Garden(self.mgr.air, avId)
        g.gardenMgr = self
        res = g.create(self.mgr)
        if res:
            self.gardens[avId] = g

    def destroy(self):
        for garden in self.gardens.values():
            garden.destroy()

        del self.gardens


class Rental:

    def __init__(self, estate):
        self.estate = estate
        self.objects = set()

    def destroy(self):
        del self.estate
        for object in self.objects:
            if not object.isDeleted():
                object.requestDelete()
                taskMgr.remove(object.uniqueName('delete'))

        self.objects = set()


class CannonRental(Rental):

    def generateObjects(self):
        target = DistributedTargetAI(self.estate.air)
        target.generateWithRequired(self.estate.zoneId)
        for drop in CannonGlobals.cannonDrops:
            cannon = DistributedCannonAI(self.estate.air)
            cannon.setEstateId(self.estate.doId)
            cannon.setTargetId(target.doId)
            cannon.setPosHpr(*drop)
            cannon.generateWithRequired(self.estate.zoneId)
            self.objects.add(cannon)

        self.generateTreasures()
        self.estate.b_setClouds(1)

    def destroy(self):
        self.estate.b_setClouds(0)
        Rental.destroy(self)

    def generateTreasures(self):
        doIds = []
        z = 35
        for i in xrange(20):
            x = random.randint(100, 300) - 200
            y = random.randint(100, 300) - 200
            treasure = DistributedTreasureAI.DistributedTreasureAI(self.estate.air, self, 9, x, y, z)
            treasure.generateWithRequired(self.estate.zoneId)
            self.objects.add(treasure)
            doIds.append(treasure.doId)

        self.estate.sendUpdate('setTreasureIds', [doIds])

    def grabAttempt(self, avId, treasureId):
        av = self.estate.air.doId2do.get(avId)
        if av == None:
            self.estate.air.writeServerEvent('suspicious', avId, 'TreasurePlannerAI.grabAttempt unknown avatar')
            self.estate.notify.warning('avid: %s does not exist' % avId)
            return
        treasure = self.estate.air.doId2do.get(treasureId)
        if self.validAvatar(av):
            treasure.d_setGrab(avId)
            self.deleteTreasureSoon(treasure)
        else:
            treasure.d_setReject()

    def deleteTreasureSoon(self, treasure):
        taskName = treasure.uniqueName('delete')
        taskMgr.doMethodLater(5, self.__deleteTreasureNow, taskName, extraArgs=(treasure, taskName))

    def __deleteTreasureNow(self, treasure, taskName):
        treasure.requestDelete()

    def validAvatar(self, av):
        if av.getMaxHp() == av.getHp():
            return 0
        av.toonUp(3)
        return 1


class DistributedEstateAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedEstateAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.toons = [0,
                      0,
                      0,
                      0,
                      0,
                      0]
        self.items = [[],
                      [],
                      [],
                      [],
                      [],
                      []]
        self.decorData = []
        self.estateType = 0
        self.cloudType = 0
        self.dawnTime = 0
        self.lastEpochTimestamp = 0
        self.rentalTimestamp = 0
        self.houses = [None] * 6
        self.pond = None
        self.spots = []
        self.targets = []
        self.treasurePlanner = None
        self.rentalType = 0
        self.rentalHandle = None
        self.targets = []
        self.owner = None
        self.gardenManager = GardenManager(self)
        self.__pendingGardens = {}

    def generate(self):
        DistributedObjectAI.generate(self)
        self.pond = DistributedFishingPondAI(simbase.air)
        self.pond.setArea(ToontownGlobals.MyEstate)
        self.pond.generateWithRequired(self.zoneId)
        for i in range(FishingTargetGlobals.getNumTargets(ToontownGlobals.MyEstate)):
            target = DistributedFishingTargetAI(self.air)
            target.setPondDoId(self.pond.getDoId())
            target.generateWithRequired(self.zoneId)
            self.targets.append(target)

        for i in xrange(6):
            avItems = self.items[i]
            for item in avItems:
                type, hardPoint, waterLevel, growthLevel, optional = item
                if type == 2:
                    boxes = GardenGlobals.estateBoxes[i]
                    box = DistributedGardenBoxAI(self.air)
                    box.setPlot(i)
                    box.setOwnerIndex(i)
                    box.setTypeIndex(boxes[hardPoint][3])
                    box.setPosition(boxes[hardPoint][0], boxes[hardPoint][1], 20)
                    box.setHeading(boxes[hardPoint][2])
                    box.generateWithRequired(self.zoneId)

        spot = DistributedFishingSpotAI(self.air)
        spot.setPondDoId(self.pond.getDoId())
        spot.setPosHpr(49.1029, -124.805, 0.344704, 90, 0, 0)
        spot.generateWithRequired(self.zoneId)
        self.spots.append(spot)
        spot = DistributedFishingSpotAI(self.air)
        spot.setPondDoId(self.pond.getDoId())
        spot.setPosHpr(46.5222, -134.739, 0.390713, 75, 0, 0)
        spot.generateWithRequired(self.zoneId)
        self.spots.append(spot)
        spot = DistributedFishingSpotAI(self.air)
        spot.setPondDoId(self.pond.getDoId())
        spot.setPosHpr(41.31, -144.559, 0.375978, 45, 0, 0)
        spot.generateWithRequired(self.zoneId)
        self.spots.append(spot)
        spot = DistributedFishingSpotAI(self.air)
        spot.setPondDoId(self.pond.getDoId())
        spot.setPosHpr(46.8254, -113.682, 0.46015, 135, 0, 0)
        spot.generateWithRequired(self.zoneId)
        self.spots.append(spot)
        self.createTreasurePlanner()

    def destroy(self):
        for house in self.houses:
            if house:
                house.requestDelete()

        del self.houses[:]
        if self.pond:
            self.pond.requestDelete()
            for spot in self.spots:
                spot.requestDelete()

            for target in self.targets:
                target.requestDelete()

        self.gardenManager.destroy()
        if self.treasurePlanner:
            self.treasurePlanner.stop()
        self.requestDelete()

    def setEstateReady(self):
        pass

    def setClientReady(self):
        self.sendUpdate('setEstateReady', [])

    def setEstateType(self, type):
        self.estateType = type

    def d_setEstateType(self, type):
        self.sendUpdate('setEstateType', [type])

    def b_setEstateType(self, type):
        self.setEstateType(type)
        self.d_setEstateType(type)

    def getEstateType(self):
        return self.estateType

    def setClosestHouse(self, todo0):
        pass

    def setTreasureIds(self, todo0):
        pass

    def createTreasurePlanner(self):
        treasureType, healAmount, spawnPoints, spawnRate, maxTreasures = TreasureGlobals.SafeZoneTreasureSpawns[ToontownGlobals.MyEstate]
        self.treasurePlanner = SZTreasurePlannerAI(self.zoneId, treasureType, healAmount, spawnPoints, spawnRate, maxTreasures)
        self.treasurePlanner.start()

    def requestServerTime(self):
        avId = self.air.getAvatarIdFromSender()
        self.sendUpdateToAvatarId(avId, 'setServerTime', [time.time() % HouseGlobals.DAY_NIGHT_PERIOD])

    def setServerTime(self, todo0):
        pass

    def setDawnTime(self, dawnTime):
        self.dawnTime = dawnTime

    def d_setDawnTime(self, dawnTime):
        self.sendUpdate('setDawnTime', [dawnTime])

    def b_setDawnTime(self, dawnTime):
        self.setDawnTime(dawnTime)
        self.d_setDawnTime(dawnTime)

    def getDawnTime(self):
        return self.dawnTime

    def placeOnGround(self, todo0):
        pass

    def setDecorData(self, decorData):
        self.decorData = decorData

    def d_setDecorData(self, decorData):
        self.sendUpdate('setDecorData', [decorData])

    def b_setDecorData(self, decorData):
        self.setDecorData(decorData)
        self.d_setDecorData(decorData)

    def getDecorData(self):
        return self.decorData

    def setLastEpochTimeStamp(self, last):
        self.lastEpochTimestamp = last

    def d_setLastEpochTimeStamp(self, last):
        self.sendUpdate('setLastEpochTimeStamp', [last])

    def b_setLastEpochTimeStamp(self, last):
        self.setLastEpochTimeStamp(last)
        self.d_setLastEpochTimeStamp(last)

    def getLastEpochTimeStamp(self):
        return self.lastEpochTimestamp

    def setRentalTimeStamp(self, rental):
        self.rentalTimestamp = rental

    def d_setRentalTimeStamp(self, rental):
        self.sendUpdate('setRentalTimeStamp', [rental])

    def b_setRentalTimeStamp(self, rental):
        self.setRentalTimeStamp(rental)
        self.d_setRentalTimeStamp(rental)

    def getRentalTimeStamp(self):
        return self.rentalTimestamp

    def b_setRentalType(self, type):
        self.d_setRentalType(type)
        self.setRentalType(type)

    def d_setRentalType(self, type):
        self.sendUpdate('setRentalType', [type])

    def setRentalType(self, type):
        expirestamp = self.getRentalTimeStamp()
        if expirestamp == 0:
            expire = 0
        else:
            expire = int(expirestamp - time.time())
        if expire < 0:
            self.rentalType = 0
            self.d_setRentalType(0)
            self.b_setRentalTimeStamp(0)
        else:
            if self.rentalType == type:
                return
            self.rentalType = type
            if self.rentalHandle:
                self.rentalHandle.destroy()
                self.rentalHandle = None
            if self.rentalType == ToontownGlobals.RentalCannon:
                self.rentalHandle = CannonRental(self)
            else:
                self.notify.warning('Unknown rental %s' % self.rentalType)
                return
            self.rentalHandle.generateObjects()

    def getRentalType(self):
        return self.rentalType

    def rentItem(self, rentType, duration):
        self.rentalType = rentType
        self.b_setRentalTimeStamp(time.time() + duration * 60)
        self.b_setRentalType(rentType)

    def setSlot0ToonId(self, id):
        self.toons[0] = id

    def d_setSlot0ToonId(self, id):
        self.sendUpdate('setSlot0ToonId', [id])

    def b_setSlot0ToonId(self, id):
        self.setSlot0ToonId(id)
        self.d_setSlot0ToonId(id)

    def getSlot0ToonId(self):
        return self.toons[0]

    def setSlot0Items(self, items):
        self.items[0] = items

    def d_setSlot0Items(self, items):
        self.sendUpdate('setSlot5Items', [items])

    def b_setSlot0Items(self, items):
        self.setSlot0Items(items)
        self.d_setSlot0Items(items)

    def getSlot0Items(self):
        return self.items[0]

    def setSlot1ToonId(self, id):
        self.toons[1] = id

    def d_setSlot1ToonId(self, id):
        self.sendUpdate('setSlot1ToonId', [id])

    def b_setSlot1ToonId(self, id):
        self.setSlot1ToonId(id)
        self.d_setSlot1ToonId(id)

    def getSlot1ToonId(self):
        return self.toons[1]

    def setSlot1Items(self, items):
        self.items[1] = items

    def d_setSlot1Items(self, items):
        self.sendUpdate('setSlot2Items', [items])

    def b_setSlot1Items(self, items):
        self.setSlot2Items(items)
        self.d_setSlot2Items(items)

    def getSlot1Items(self):
        return self.items[1]

    def setSlot2ToonId(self, id):
        self.toons[2] = id

    def d_setSlot2ToonId(self, id):
        self.sendUpdate('setSlot2ToonId', [id])

    def b_setSlot2ToonId(self, id):
        self.setSlot2ToonId(id)
        self.d_setSlot2ToonId(id)

    def getSlot2ToonId(self):
        return self.toons[2]

    def setSlot2Items(self, items):
        self.items[2] = items

    def d_setSlot2Items(self, items):
        self.sendUpdate('setSlot2Items', [items])

    def b_setSlot2Items(self, items):
        self.setSlot2Items(items)
        self.d_setSlot2Items(items)

    def getSlot2Items(self):
        return self.items[2]

    def setSlot3ToonId(self, id):
        self.toons[3] = id

    def d_setSlot3ToonId(self, id):
        self.sendUpdate('setSlot3ToonId', [id])

    def b_setSlot3ToonId(self, id):
        self.setSlot3ToonId(id)
        self.d_setSlot3ToonId(id)

    def getSlot3ToonId(self):
        return self.toons[3]

    def setSlot3Items(self, items):
        self.items[3] = items

    def d_setSlot3Items(self, items):
        self.sendUpdate('setSlot3Items', [items])

    def b_setSlot3Items(self, items):
        self.setSlot3Items(items)
        self.d_setSlot3Items(items)

    def getSlot3Items(self):
        return self.items[3]

    def setSlot4ToonId(self, id):
        self.toons[4] = id

    def d_setSlot4ToonId(self, id):
        self.sendUpdate('setSlot4ToonId', [id])

    def b_setSlot5ToonId(self, id):
        self.setSlot4ToonId(id)
        self.d_setSlot4ToonId(id)

    def getSlot4ToonId(self):
        return self.toons[4]

    def setSlot4Items(self, items):
        self.items[4] = items

    def d_setSlot4Items(self, items):
        self.sendUpdate('setSlot4Items', [items])

    def b_setSlot4Items(self, items):
        self.setSlot4Items(items)
        self.d_setSlot4Items(items)

    def getSlot4Items(self):
        return self.items[4]

    def setSlot5ToonId(self, id):
        self.toons[5] = id

    def d_setSlot5ToonId(self, id):
        self.sendUpdate('setSlot5ToonId', [id])

    def b_setSlot5ToonId(self, id):
        self.setSlot5ToonId(id)
        self.d_setSlot5ToonId(id)

    def getSlot5ToonId(self):
        return self.toons[5]

    def setSlot5Items(self, items):
        self.items[5] = items

    def d_setSlot5Items(self, items):
        self.sendUpdate('setSlot5Items', [items])

    def b_setSlot5Items(self, items):
        self.setSlot5Items(items)
        self.d_setSlot5Items(items)

    def getSlot5Items(self):
        return self.items[5]

    def setIdList(self, idList):
        for i in range(len(idList)):
            if i >= 6:
                return
            self.toons[i] = idList[i]

    def d_setIdList(self, idList):
        self.sendUpdate('setIdList', [idList])

    def b_setIdList(self, idList):
        self.setIdList(idList)
        self.d_setIdLst(idList)

    def completeFlowerSale(self, flag):
        if not flag:
            return

        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)
        if not av:
            return

        collection = av.flowerCollection

        earning = 0
        newSpecies = 0
        for flower in av.flowerBasket.getFlower():
            if collection.collectFlower(flower) == GardenGlobals.COLLECT_NEW_ENTRY:
                newSpecies += 1

            earning += flower.getValue()

        av.b_setFlowerBasket([], [])
        av.d_setFlowerCollection(*av.flowerCollection.getNetLists())
        av.addMoney(earning)

        oldSpecies = len(collection) - newSpecies
        dt = abs(len(collection) // 10 - oldSpecies // 10)
        if dt:
            self.notify.info('%d is getting a gardening trophy!' % avId)

            maxHp = av.getMaxHp()
            maxHp = min(ToontownGlobals.MaxHpLimit, maxHp + dt)
            av.b_setMaxHp(maxHp)
            av.toonUp(maxHp)

            self.sendUpdate('awardedTrophy', [avId])

        av.b_setGardenTrophies(range(len(collection) // 10))

    def awardedTrophy(self, todo0):
        pass

    def setClouds(self, clouds):
        self.cloudType = clouds

    def d_setClouds(self, clouds):
        self.sendUpdate('setClouds', [clouds])

    def b_setClouds(self, clouds):
        self.setClouds(clouds)
        self.d_setClouds(clouds)

    def getClouds(self):
        return self.cloudType

    def cannonsOver(self):
        pass

    def gameTableOver(self):
        pass

    def updateToons(self):
        self.d_setSlot0ToonId(self.toons[0])
        self.d_setSlot1ToonId(self.toons[1])
        self.d_setSlot2ToonId(self.toons[2])
        self.d_setSlot3ToonId(self.toons[3])
        self.d_setSlot4ToonId(self.toons[4])
        self.d_setSlot5ToonId(self.toons[5])
        self.sendUpdate('setIdList', [self.toons])

    def updateItems(self):
        self.d_setSlot0Items(self.items[0])
        self.d_setSlot1Items(self.items[1])
        self.d_setSlot2Items(self.items[2])
        self.d_setSlot3Items(self.items[3])
        self.d_setSlot4Items(self.items[4])
        self.d_setSlot5Items(self.items[5])

        # Garden methods
    def getToonSlot(self, avId):
        if avId not in self.toons:
            return

        return self.toons.index(avId)

    def setSlot0Garden(self, flag):
        self.__pendingGardens[0] = flag

    def setSlot1Garden(self, flag):
        self.__pendingGardens[1] = flag

    def setSlot2Garden(self, flag):
        self.__pendingGardens[2] = flag

    def setSlot3Garden(self, flag):
        self.__pendingGardens[3] = flag

    def setSlot4Garden(self, flag):
        self.__pendingGardens[4] = flag

    def setSlot5Garden(self, flag):
        self.__pendingGardens[5] = flag

    def placeStarterGarden(self, avId, record=1):
        av = self.air.doId2do.get(avId)
        if not av:
            return

        slot = self.getToonSlot(avId)
        if slot is None:
            return

        if record:
            av.b_setGardenStarted(1)
            self.sendUpdate('setSlot%dGarden' % slot, ['started'])

        self.notify.info('placeStarterGarden %d %d' % (avId, slot))
        self.gardenManager.handleSingleGarden(avId)

    def announceGenerate(self):
        DistributedObjectAI.announceGenerate(self)
        self.sendUpdate('setIdList', [self.toons])

        for index, started in self.__pendingGardens.items():
            if started:
                self.gardenManager.handleSingleGarden(self.toons[index])

        self.__pendingGardens = {}
        if config.GetBool('fake-garden-started-ai', False):
            self.placeStarterGarden(100000002, 0)