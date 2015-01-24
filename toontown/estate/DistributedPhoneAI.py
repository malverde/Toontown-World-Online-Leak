from direct.directnotify import DirectNotifyGlobal
from toontown.estate.DistributedFurnitureItemAI import DistributedFurnitureItemAI
from direct.distributed import ClockDelta
from PhoneGlobals import *

class DistributedPhoneAI(DistributedFurnitureItemAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedPhoneAI")

    def __init__(self, air, furnitureMgr, item):
        DistributedFurnitureItemAI.__init__(self, air, furnitureMgr, item)
        self.initialScale = (0.8, 0.8, 0.8)
        self.newScale = (0, 0, 0)
        ownerId = 0
        self.ownerId = ownerId
        self.busy = 0
        self.avId = None
    def setInitialScale(self, sx, sy, sz):
        self.initialScale = (sx, sy, sz)
        self.sendUpdate('setInitialScale', args=[sx, sy, sz])

    def getInitialScale(self):
        return self.initialScale

    def setNewScale(self, sx, sy, sz):
        self.newScale = (sx, sy, sz)
        self.sendUpdate('setNewScale', args=[sx, sy, sz])

    def getNewScale(self):
        return self.newScale

    def avatarEnter(self):
        avId = self.air.getAvatarIdFromSender()
        if self.avId:
            if self.avId == avId:
                self.air.writeServerEvent('suspicious', avId=avId, issue='Tried to use a phone twice!')
                return

            self.sendUpdateToAvatarId(avId, 'freeAvatar', [])
            return

        av = self.air.doId2do.get(avId)
        if not av:
            return

        if not av.houseId:
            # Let's not deal with toons that have no houses, pls.
            self.sendUpdateToAvatarId(avId, 'freeAvatar', [])
            return

        if len(av.monthlyCatalog) == 0 and len(av.weeklyCatalog) == 0 and len(av.backCatalog) == 0:
            self.d_setMovie(PhoneGlobals.PHONE_MOVIE_EMPTY, avId, globalClockDelta.getRealNetworkTime())
            taskMgr.doMethodLater(1, self.__resetMovie, 'resetMovie-%d' % self.getDoId(), extraArgs=[])
            self.notify.debug("No Catalogs")
            return

        self.air.questManager.toonCalledClarabelle(av)

        self.notify.debug("Loading the catalog")
        self.avId = avId
        self.d_setMovie(PhoneGlobals.PHONE_MOVIE_PICKUP, avId, globalClockDelta.getRealNetworkTime())

        house = self.air.doId2do.get(av.houseId)
        if house:
            numItems = len(house.interiorItems) + len(house.atticItems) + len(house.atticWallpaper) + len(house.atticWindows) + len (house.interiorWallpaper) + len(house.interiorWindows)
            self.sendUpdateToAvatarId(avId, 'setLimits', [numItems])
        else:
            self.air.dbInterface.queryObject(self.air.dbId, av.houseId, self.__gotHouse)

        av.b_setCatalogNotify(ToontownGlobals.NoItems, av.mailboxNotify)


    def avatarExit(self):
        self.sendExitMovie()
        self.sendClearMovie()

        self.busy = 0

    def freeAvatar(self, avId):
        self.sendUpdateToAvatarId(avId, 'freeAvatar', [])

    def setLimits(self, todo0):
        pass

    def setMovie(self, mode, avId):
        timestamp = ClockDelta.globalClockDelta.getRealNetworkTime(bits=32)
        self.sendUpdate('setMovie', args=[mode, avId, timestamp])

    def sendEnterMovie(self, avId):
        self.setMovie(PHONE_MOVIE_PICKUP, avId)

    def sendExitMovie(self):
        self.setMovie(PHONE_MOVIE_HANGUP, self.busy)

    def sendClearMovie(self):
        self.setMovie(PHONE_MOVIE_CLEAR, self.busy)

    def requestPurchaseMessage(self, context, blob, optional):
        pass

    def requestPurchaseResponse(self, context, retcode):
        self.sendUpdate('requestPurchaseResponse', args=[context, retcode])

    def requestGiftPurchaseMessage(self, context, target, blob, optional):
        pass

    def requestGiftPurchaseResponse(self, context, retcode):
        self.sendUpdate('requestGiftPurchaseResponse', args=[context, retcode])