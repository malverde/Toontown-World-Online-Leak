#Embedded file name: toontown.parties.DistributedPartyActivityAI
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from toontown.parties import PartyGlobals, PartyUtils

class DistributedPartyActivityAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPartyActivityAI')

    def __init__(self, air, parent, activityTuple):
        DistributedObjectAI.__init__(self, air)
        self.parent = parent
        x, y, h = activityTuple[1:]
        self.x = PartyUtils.convertDistanceFromPartyGrid(x, 0)
        self.y = PartyUtils.convertDistanceFromPartyGrid(y, 1)
        self.h = h * PartyGlobals.PartyGridHeadingConverter
        self.toonsPlaying = []

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getH(self):
        return self.h

    def getPartyDoId(self):
        return self.parent

    def updateToonsPlaying(self):
        self.sendUpdate('setToonsPlaying', [self.toonsPlaying])

    def toonJoinRequest(self):
        self.notify.info('Toon join request')
        avId = self.air.getAvatarIdFromSender()
        self.toonsPlaying.append(avId)
        self.updateToonsPlaying()

    def toonExitRequest(self):
        self.notify.info('Toon exit request')

    def toonExitDemand(self):
        self.notify.info('Toon exit demand')
        avId = self.air.getAvatarIdFromSender()
        self.toonsPlaying.remove(avId)
        self.updateToonsPlaying()

    def toonReady(self):
        self.notify.info('Toon is ready')

    def joinRequestDenied(self, todo0):
        pass

    def exitRequestDenied(self, todo0):
        pass

    def setToonsPlaying(self, todo0):
        pass

    def setState(self, todo0, todo1):
        pass

    def showJellybeanReward(self, todo0, todo1, todo2):
        pass
