from direct.directnotify import DirectNotifyGlobal
from toontown.estate.DistributedFurnitureItemAI import DistributedFurnitureItemAI
from direct.distributed import ClockDelta
from PhoneGlobals import *

class DistributedPhoneAI(DistributedFurnitureItemAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedPhoneAI")

    def __init__(self, air, furnitureMgr, catalogItem, ownerId):
        DistributedFurnitureItemAI.__init__(self, air, furnitureMgr, catalogItem)
        self.initialScale = (0.8, 0.8, 0.8)
        self.newScale = (0, 0, 0)
        self.ownerId = ownerId
        self.busy = 0

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

        if not self.busy:
            self.sendEnterMovie(avId)
            self.air.questManager.toonUsedPhone(avId)
            self.busy = avId
        else:
            self.freeAvatar(avId)

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