#Embedded file name: toontown.estate.DistributedCannonAI
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.distributed.ClockDelta import *
from toontown.minigame import CannonGameGlobals
from toontown.toonbase import ToontownGlobals
import CannonGlobals

class DistributedCannonAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedCannonAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.estateId = 0
        self.targetId = 0
        self.posHpr = (0, 0, 0, 0, 0, 0)
        self.bumperPos = ToontownGlobals.PinballCannonBumperInitialPos
        self.active = 0
        self.avId = 0

    def setEstateId(self, estateId):
        self.estateId = estateId

    def getEstateId(self):
        return self.estateId

    def setTargetId(self, targetId):
        self.targetId = targetId

    def getTargetId(self):
        return self.targetId

    def setPosHpr(self, x, y, z, h, p, r):
        self.posHpr = (x,
         y,
         z,
         h,
         p,
         r)

    def getPosHpr(self):
        return self.posHpr

    def setActive(self, active):
        self.active = active
        self.sendUpdate('setActiveState', [active])

    def requestEnter(self):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)
        if not av:
            return
        if not self.avId:
            self.avId = avId
            self.d_setMovie(CannonGlobals.CANNON_MOVIE_LOAD)
            self.acceptOnce(self.air.getAvatarExitEvent(avId), self.__handleUnexpectedExit, extraArgs=[avId])
        else:
            self.air.writeServerEvent('suspicious', avId, 'DistributedCannonAI.requestEnter cannon already occupied')
            self.notify.warning('requestEnter() - cannon already occupied')

    def setMovie(self, mode, avId, extraInfo):
        self.avId = avId
        self.sendUpdate('setMovie', [mode, avId, extraInfo])

    def __handleUnexpectedExit(self, avId):
        self.notify.warning('avatar:' + str(avId) + ' has exited unexpectedly')
        self.__doExit()

    def __doExit(self, movie = CannonGlobals.CANNON_MOVIE_FORCE_EXIT):
        self.ignore(self.air.getAvatarExitEvent(self.avId))
        self.d_setMovie(movie)
        self.avId = 0

    def requestExit(self):
        pass

    def d_setMovie(self, movie):
        self.sendUpdate('setMovie', [movie, self.avId])

    def setCannonPosition(self, zRot, angle):
        self.sendUpdate('updateCannonPosition', [self.avId, zRot, angle])

    def setCannonLit(self, zRot, angle):
        avId = self.air.getAvatarIdFromSender()
        if avId != self.avId:
            return
        fireTime = CannonGameGlobals.FUSE_TIME
        self.sendUpdate('setCannonWillFire', [avId,
         fireTime,
         zRot,
         angle,
         globalClockDelta.getRealNetworkTime()])

    def setFired(self):
        pass

    def setLanded(self):
        self.__doExit(CannonGlobals.CANNON_MOVIE_CLEAR)
        self.sendUpdate('setCannonExit', [self.avId])

    def setCannonExit(self, todo0):
        pass

    def requestBumperMove(self, x, y, z):
        self.bumperPos = (x, y, z)
        self.sendUpdate('setCannonBumperPos', self.getCannonBumperPos())

    def getCannonBumperPos(self):
        return self.bumperPos
