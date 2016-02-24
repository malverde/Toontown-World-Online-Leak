import CatalogItem
from toontown.toonbase import ToontownGlobals
from toontown.fishing import FishGlobals
from direct.actor import Actor
from toontown.toonbase import TTLocalizer
from direct.interval.IntervalGlobal import *

class CatalogTankItem(CatalogItem.CatalogItem):
    sequenceNumber = 0

    def makeNewItem(self, maxTank):
        self.maxTank = maxTank
        CatalogItem.CatalogItem.makeNewItem(self)

    def getPurchaseLimit(self):
        return 1

    def reachedPurchaseLimit(self, avatar):
        return avatar.getMaxFishTank() >= self.maxTank or self in avatar.onOrder or self in avatar.mailboxContents

    def saveHistory(self):
        return 1

    def getTypeName(self):
        return TTLocalizer.TankTypeName

    def getName(self):
        return TTLocalizer.FishTank % TTLocalizer.FishTankNameDict[self.maxTank]

    def recordPurchase(self, avatar, optional):
        if self.maxTank < 0 or self.maxTank > FishGlobals.MaxTank:
            return ToontownGlobals.P_InvalidIndex
        if self.maxTank <= avatar.getMaxFishTank():
            return ToontownGlobals.P_ItemUnneeded
        avatar.b_setMaxFishTank(self.maxTank)
        return ToontownGlobals.P_ItemOnOrder

    def isGift(self):
        return 0

    def getDeliveryTime(self):
        return 1

    def getPicture(self, avatar):
        gui = loader.loadModel('phase_4/models/gui/fishingGui')
        bucket = gui.find('**/bucket')
        bucket.setScale(2.7)
        bucket.setPos(-3.15, 0, 3.2)

        frame = self.makeFrame()
        bucket.reparentTo(frame)
        gui.removeNode()
        return (frame, None)

    def getAcceptItemErrorText(self, retcode):
        if retcode == ToontownGlobals.P_ItemAvailable:
            return TTLocalizer.CatalogAcceptTank
        elif retcode == ToontownGlobals.P_ItemUnneeded:
            return TTLocalizer.CatalogAcceptTankUnneeded
        return CatalogItem.CatalogItem.getAcceptItemErrorText(self, retcode)

    def output(self, store = -1):
        return 'CatalogTankItem(%s%s)' % (self.maxTank, self.formatOptionalData(store))

    def compareTo(self, other):
        return self.maxTank - other.maxTank

    def getHashContents(self):
        return self.maxTank

    def getBasePrice(self):
        return FishGlobals.TankPriceDict[self.maxTank]

    def decodeDatagram(self, di, versionNumber, store):
        CatalogItem.CatalogItem.decodeDatagram(self, di, versionNumber, store)
        self.maxTank = di.getUint8()

    def encodeDatagram(self, dg, store):
        CatalogItem.CatalogItem.encodeDatagram(self, dg, store)
        dg.addUint8(self.maxTank)

def nextAvailableTank(avatar, duplicateItems):
    tank = avatar.getMaxFishTank()

    if not tank in FishGlobals.NextTank:
        return None

    return CatalogTankItem(FishGlobals.NextTank[tank])

def getAllTanks():
    list = []
    for old, new in FishGlobals.NextTank.iteritems():
        list.append(CatalogTankItem(new))

    return list
