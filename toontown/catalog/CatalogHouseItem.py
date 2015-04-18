from toontown.catalog.CatalogItem import CatalogItem
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
from toontown.estate import HouseGlobals


class CatalogHouseItem(CatalogItem):
    def makeNewItem(self, houseType):
        self.houseType = houseType

        CatalogItem.makeNewItem(self)

    def decodeDatagram(self, di, versionNumber, store):
        CatalogItem.decodeDatagram(self, di, versionNumber, store)

        self.houseType = di.getUint8()

    def encodeDatagram(self, dg, store):
        CatalogItem.encodeDatagram(self, dg, store)

        dg.addUint8(self.houseType)

    def compareTo(self, other):
        return self.houseType - other.houseType

    def getHashContents(self):
        return (self.houseType,)

    def output(self, store = -1):
        return 'CatalogHouseItem(%s%s)' % (self.houseType, self.formatOptionalData(store))

    def getBasePrice(self):
        return ToontownGlobals.getHousePriceById(self.houseType)

    def getTypeName(self):
        return TTLocalizer.HouseTypeName

    def getName(self):
        return TTLocalizer.getHouseNameById(self.houseType)

    def reachedPurchaseLimit(self, avatar):
        return avatar.getHouseType() == self.houseType or self in avatar.onOrder or self in avatar.mailboxContents

    def isGift(self):
        return False

    def getPicture(self, avatar):
        self.model = loader.loadModel(HouseGlobals.houseModels[self.houseType])
        frame = self.makeFrame()
        self.model.reparentTo(frame)
        self.model.setScale(0.1)
        self.model.setH(90)
        self.model.setZ(-1)
        self.hasPicture = True
        return (frame, None)

    def cleanupPicture(self):
        CatalogItem.cleanupPicture(self)

        self.model.detachNode()
        self.model = None

    def recordPurchase(self, avatar, optional):
        if avatar:
            house = simbase.air.doId2do.get(avatar.getHouseId())
            if house:
                house.b_setHouseType(self.houseType)
        return ToontownGlobals.P_ItemAvailable