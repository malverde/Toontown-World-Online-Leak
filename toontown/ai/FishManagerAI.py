import random

from otp.ai.MagicWordGlobal import *
from toontown.fishing import FishGlobals
from toontown.fishing.FishBase import FishBase
from toontown.toonbase import TTLocalizer


class FishManagerAI:
    def __init__(self, air):
        self.air = air
        self.ponds = {}
        self.requestedFish = {}

    def creditFishTank(self, av):
        totalFish = len(av.fishCollection)
        trophies = int(totalFish / 10)
        curTrophies = len(av.fishingTrophies)
        av.addMoney(av.fishTank.getTotalValue())
        av.b_setFishTank([], [], [])
        if trophies > curTrophies:
            av.b_setMaxHp(av.getMaxHp() + trophies - curTrophies)
            av.toonUp(av.getMaxHp())
            av.b_setFishingTrophies(range(trophies))
            return True
        return False

    def generateCatch(self, av, zoneId):
        if len(av.fishTank) >= av.getMaxFishTank():
            return [FishGlobals.OverTankLimit, 0, 0, 0]
        rand = random.random() * 100.0
        for cutoff in FishGlobals.SortedProbabilityCutoffs:
            if rand <= cutoff:
                itemType = FishGlobals.ProbabilityDict[cutoff]
                break
        if av.doId in self.requestedFish:
            genus, species = self.requestedFish[av.doId]
            weight = FishGlobals.getRandomWeight(genus, species)
            fish = FishBase(genus, species, weight)
            fishType = av.fishCollection.collectFish(fish)
            if fishType == FishGlobals.COLLECT_NEW_ENTRY:
                itemType = FishGlobals.FishItemNewEntry
            elif fishType == FishGlobals.COLLECT_NEW_RECORD:
                itemType = FishGlobals.FishItemNewRecord
            else:
                itemType = FishGlobals.FishItem
            netlist = av.fishCollection.getNetLists()
            av.d_setFishCollection(netlist[0], netlist[1], netlist[2])
            av.fishTank.addFish(fish)
            netlist = av.fishTank.getNetLists()
            av.d_setFishTank(netlist[0], netlist[1], netlist[2])
            del self.requestedFish[av.doId]
            return [itemType, genus, species, weight]
        if itemType == FishGlobals.FishItem:
            success, genus, species, weight = FishGlobals.getRandomFishVitals(zoneId, av.getFishingRod())
            fish = FishBase(genus, species, weight)
            fishType = av.fishCollection.collectFish(fish)
            if fishType == FishGlobals.COLLECT_NEW_ENTRY:
                itemType = FishGlobals.FishItemNewEntry
            elif fishType == FishGlobals.COLLECT_NEW_RECORD:
                itemType = FishGlobals.FishItemNewRecord
            else:
                itemType = FishGlobals.FishItem
            netlist = av.fishCollection.getNetLists()
            av.d_setFishCollection(netlist[0], netlist[1], netlist[2])
            av.fishTank.addFish(fish)
            netlist = av.fishTank.getNetLists()
            av.d_setFishTank(netlist[0], netlist[1], netlist[2])
            return [itemType, genus, species, weight]
        elif itemType == FishGlobals.BootItem:
            return [itemType, 0, 0, 0]
        elif itemType == FishGlobals.QuestItem:
            itemId = simbase.air.questManager.toonCaughtFishingItem(av)

            if itemId != -1:
                return [itemType, itemId, 0, 0]
            else:
                success, genus, species, weight = FishGlobals.getRandomFishVitals(zoneId, av.getFishingRod())
                fish = FishBase(genus, species, weight)
                fishType = av.fishCollection.collectFish(fish)
                if fishType == FishGlobals.COLLECT_NEW_ENTRY:
                    itemType = FishGlobals.FishItemNewEntry
                elif fishType == FishGlobals.COLLECT_NEW_RECORD:
                    itemType = FishGlobals.FishItemNewRecord
                else:
                    itemType = FishGlobals.FishItem
                netlist = av.fishCollection.getNetLists()
                av.d_setFishCollection(netlist[0], netlist[1], netlist[2])
                av.fishTank.addFish(fish)
                netlist = av.fishTank.getNetLists()
                av.d_setFishTank(netlist[0], netlist[1], netlist[2])
                return [itemType, genus, species, weight]
        else:
            money = FishGlobals.Rod2JellybeanDict[av.getFishingRod()]
            av.addMoney(money)
            return [itemType, money, 0, 0]


@magicWord(category=CATEGORY_ADMINISTRATOR, types=[str])
def fish(fishName):
    """
    Register/unregister the fish to be caught on the invoker.
    """
    invoker = spellbook.getInvoker()
    if fishName.lower() == 'remove':
        if invoker.doId not in simbase.air.fishManager.fishRequests:
            return 'You have not requested a fish.'
        del simbase.air.fishManager.fishRequests[invoker.doId]
        return 'Removed your fish request.'

    for genus, species in TTLocalizer.FishSpeciesNames:
        for name in species:
            if fishName.lower() != name.lower():
                continue
            fishRequest = (genus, species.index(name))
            simbase.air.fishManager.fishRequests[invoker.doId] = fishRequest
            return 'A request for the fish %s was saved.' % name

    return "Couldn't find a fish with the name %s!" % fishName
