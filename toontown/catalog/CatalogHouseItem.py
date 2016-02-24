import CatalogItem
from toontown.toonbase import TTLocalizer
from direct.showbase import PythonUtil
from direct.gui.DirectGui import *
from toontown.toonbase import ToontownGlobals
from toontown.estate import HouseGlobals

class CatalogHouseItem(CatalogItem.CatalogItem):
    def makeNewItem(self, houseId):
        self.houseId = houseId
        CatalogItem.CatalogItem.makeNewItem(self)

    def notOfferedTo(self, avatar):
        return 1

    def requestPurchase(self, phone, callback):
        from toontown.toontowngui import TTDialog
        avatar = base.localAvatar

        self.requestPurchaseCleanup()
        buttonCallback = PythonUtil.Functor(self.__handleFullPurchaseDialog, phone, callback)
        self.dialog = TTDialog.TTDialog(style=TTDialog.YesNo, text=TTLocalizer.CatalogPurchaseHouseType, text_wordwrap=15, command=buttonCallback)
        self.dialog.show()

    def requestPurchaseCleanup(self):
        if hasattr(self, 'dialog'):
            self.dialog.cleanup()
            del self.dialog

    def __handleFullPurchaseDialog(self, phone, callback, buttonValue):
        from toontown.toontowngui import TTDialog
        self.requestPurchaseCleanup()
        if buttonValue == DGG.DIALOG_OK:
            CatalogItem.CatalogItem.requestPurchase(self, phone, callback)
        else:
            callback(ToontownGlobals.P_UserCancelled, self)

    def getTypeName(self):
        return "House Type"

    def getName(self):
        return TTLocalizer.HouseNames[self.houseId]

    def getDeliveryTime(self):
        return 0

    def getEmblemPrices(self):
        return HouseGlobals.HouseEmblemPrices[self.houseId]

    def getPicture(self, avatar):
        model = loader.loadModel(HouseGlobals.houseModels[self.houseId])
        model.setBin('unsorted', 0, 1)
        self.hasPicture = True
        return self.makeFrameModel(model)

    def decodeDatagram(self, di, versionNumber, store):
        CatalogItem.CatalogItem.decodeDatagram(self, di, versionNumber, store)
        self.houseId = di.getUint8()

    def encodeDatagram(self, dg, store):
        CatalogItem.CatalogItem.encodeDatagram(self, dg, store)
        dg.addUint8(self.houseId)

    def recordPurchase(self, av, optional):
        house = simbase.air.doId2do.get(av.getHouseId())
        if house:
            house.b_setHouseType(self.houseId)
        return ToontownGlobals.P_ItemAvailable

def getAllHouses():
    return [CatalogHouseItem(i) for i in xrange(6)]
