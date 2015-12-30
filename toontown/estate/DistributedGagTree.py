from direct.directnotify import DirectNotifyGlobal
from otp.ai.MagicWordGlobal import *
from toontown.estate.DistributedPlantBaseAI import DistributedPlantBaseAI
import GardenGlobals, time

ONE_DAY = 86400

PROBLEM_WILTED = 1
PROBLEM_NOT_GROWN = 2
PROBLEM_HARVESTED_LATELY = 4

class DistributedGagTreeAI(DistributedPlantBaseAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedGagTreeAI')
    GrowRate = config.GetBool('trees-grow-rate', 2)

    def __init__(self, mgr):
        DistributedPlantBaseAI.__init__(self, mgr)
        self.wilted = 0

    def announceGenerate(self):
        DistributedPlantBaseAI.announceGenerate(self)
        messenger.send(self.getEventName('generate'))

    def setWilted(self, wilted):
        self.wilted = wilted

    def d_setWilted(self, wilted):
        self.sendUpdate('setWilted', [wilted])

    def b_setWilted(self, wilted):
        self.setWilted(wilted)
        self.d_setWilted(wilted)

    def getWilted(self):
        return self.wilted

    def calculate(self, lastHarvested, lastCheck):
        now = int(time.time())
        if lastCheck == 0:
            lastCheck = now

        grown = 0

        # Water level
        elapsed = now - lastCheck
        while elapsed > ONE_DAY:
            if self.waterLevel >= 0:
                grown += self.GrowRate

            elapsed -= ONE_DAY
            self.waterLevel -= 1

        self.waterLevel = max(self.waterLevel, -2)

        # Growth level
        maxGrowth = self.growthThresholds[2]
        newGL = min(self.growthLevel + grown, maxGrowth)
        self.setGrowthLevel(newGL)

        self.setWilted(self.waterLevel == -2)

        self.lastCheck = now - elapsed
        self.lastHarvested = lastHarvested
        self.update()

    def calcDependencies(self):
        if self.getWilted():
            return

        missingPrevIndex = 0
        track, value = GardenGlobals.getTreeTrackAndLevel(self.typeIndex)
        while value:
            value -= 1
            if not self.mgr.hasTree(track, value):
                self.b_setWilted(1)
                continue

            tree = self.mgr.getTree(track, value)
            if not tree:
                self.b_setWilted(1)
                continue

            self.accept(self.getEventName('going-down', 666), self.ignoreAll)
            self.accept(self.getEventName('remove', track * 7 + value), self.calcDependencies)

    def getEventName(self, string, typeIndex=None):
        typeIndex = typeIndex if typeIndex is not None else self.typeIndex
        return 'garden-%d-%d-%s' % (self.ownerDoId, typeIndex, string)

    def delete(self):
        messenger.send(self.getEventName('remove'))
        self.ignoreAll()
        DistributedPlantBaseAI.delete(self)

    def update(self):
        mdata = map(list, self.mgr.data['trees'])
        mdata[self.treeIndex] = [self.typeIndex, self.waterLevel, self.lastCheck, self.getGrowthLevel(), self.lastHarvested]
        self.mgr.data['trees'] = mdata
        self.mgr.update()

    def isFruiting(self):
        problem = 0
        if self.getWilted():
            problem |= PROBLEM_WILTED

        if self.getGrowthLevel() < self.growthThresholds[2]:
            problem |= PROBLEM_NOT_GROWN

        if (self.lastCheck - self.lastHarvested) < ONE_DAY:
            problem |= PROBLEM_HARVESTED_LATELY

        return problem

    def getFruiting(self):
        return self.isFruiting() == 0

    def requestHarvest(self):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)
        if not av:
            return

        if avId != self.ownerDoId:
            self.air.writeServerEvent('suspicious', avId, 'tried to harvest someone else\'s tree!')
            return

        problem = self.isFruiting()
        if problem:
            self.air.writeServerEvent('suspicious', avId, 'tried to harvest a tree that\'s not fruiting!', problem=problem)
            return

        harvested = 0
        track, level = GardenGlobals.getTreeTrackAndLevel(self.typeIndex)
        while av.inventory.addItem(track, level) > 0 and harvested < 10:
            harvested += 1

        av.d_setInventory(av.getInventory())

        self.lastHarvested = int(time.time())
        self.sendUpdate('setFruiting', [self.getFruiting()])
        self.d_setMovie(GardenGlobals.MOVIE_HARVEST)
        self.update()

    def removeItem(self):
        avId = self.air.getAvatarIdFromSender()
        self.d_setMovie(GardenGlobals.MOVIE_REMOVE)

        def _remove(task):
            if not self.air:
                return

            plot = self.mgr.placePlot(self.treeIndex)
            plot.setPlot(self.plot)
            plot.setPos(self.getPos())
            plot.setH(self.getH())
            plot.setOwnerIndex(self.ownerIndex)
            plot.generateWithRequired(self.zoneId)

            self.air.writeServerEvent('remove-tree', avId, plot=self.plot)
            self.requestDelete()

            self.mgr.trees.remove(self)

            mdata = map(list, self.mgr.data['trees'])
            mdata[self.treeIndex] = self.mgr.getNullPlant()
            self.mgr.data['trees'] = mdata
            self.mgr.update()

            self.mgr.reconsiderAvatarOrganicBonus()

            return task.done

        taskMgr.doMethodLater(7, _remove,  self.uniqueName('do-remove'))

    def doGrow(self, grown):
        maxGrowth = self.growthThresholds[2]
        newGL = max(0, min(self.growthLevel + grown, maxGrowth))
        oldGrowthLevel = self.growthLevel

        self.b_setGrowthLevel(newGL)
        self.update()

        return newGL - oldGrowthLevel

@magicWord(category=CATEGORY_SYSADMIN, types=[int, int, int])
def satanGrow(track, index, grown=21):
    av = spellbook.getTarget()
    estate = av.air.estateManager._lookupEstate(av)

    if not estate:
        return 'Estate not found!'

    garden = estate.gardenManager.gardens.get(av.doId)
    if not garden:
        return 'Garden not found!'

    tree = garden.getTree(track, index)
    if not tree:
        return 'Tree not found!'

    result = tree.doGrow(grown)
    return 'Satan has grown %d units!' % result

@magicWord(category=CATEGORY_SYSADMIN, types=[int, int])
def satanFruit(track, index):
    av = spellbook.getTarget()
    estate = av.air.estateManager._lookupEstate(av)

    if not estate:
        return 'Estate not found!'

    garden = estate.gardenManager.gardens.get(av.doId)
    if not garden:
        return 'Garden not found!'

    tree = garden.getTree(track, index)
    if not tree:
        return 'Tree not found!'

    tree.calculate(0, tree.lastCheck)
    tree.sendUpdate('setFruiting', [tree.getFruiting()])
    return 'Satan is now fruiting!'
