from direct.distributed.DistributedObjectAI import DistributedObjectAI
import cPickle


class DistributedHQInteriorAI(DistributedObjectAI):
    notify = directNotify.newCategory('DistributedHQInteriorAI')

    def __init__(self, block, air, zoneId):
        DistributedObjectAI.__init__(self, air)
        self.block = block
        self.zoneId = zoneId
        self.tutorial = 0
        self.isDirty = False
        self.accept('leaderboardChanged', self.leaderboardChanged)
        self.accept('leaderboardFlush', self.leaderboardFlush)

    def delete(self):
        self.ignore('leaderboardChanged')
        self.ignore('leaderboardFlush')
        self.ignore('setLeaderBoard')
        self.ignore('AIStarted')
        DistributedObjectAI.delete(self)

    def getZoneIdAndBlock(self):
        return [self.zoneId, self.block]

    def leaderboardChanged(self):
        self.isDirty = True

    def leaderboardFlush(self):
        if self.isDirty:
            self.sendNewLeaderBoard()

    def sendNewLeaderBoard(self):
        if self.air:
            self.isDirty = False
            self.sendUpdate(
                'setLeaderBoard', [
                    cPickle.dumps(
                        self.air.trophyMgr.getLeaderInfo(), 1)])

    def getLeaderBoard(self):
        return cPickle.dumps(self.air.trophyMgr.getLeaderInfo(), 1)

    def getTutorial(self):
        return self.tutorial

    def setTutorial(self, flag):
        if self.tutorial != flag:
            self.tutorial = flag
            self.sendUpdate('setTutorial', [self.tutorial])
