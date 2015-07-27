#Embedded file name: toontown.estate.DistributedTargetAI
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
import CannonGlobals
import random

class DistributedTargetAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedTargetAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.enabled = 0
        self.highscore = 0
        self.scoreDict = {}
        self.__newGame()

    def announceGenerate(self):
        DistributedObjectAI.announceGenerate(self)
        taskMgr.doMethodLater(10, self.__startNewGame, self.taskName('newGame'))

    def __newGame(self):
        self.power = 1
        self.time = CannonGlobals.CANNON_TIMEOUT

    def getPosition(self):
        return (0, 0, 40)

    def getState(self):
        return (self.enabled, 2 ** self.power, self.time)

    def d_updateState(self):
        self.sendUpdate('setState', self.getState())

    def d_setReward(self, reward):
        self.sendUpdate('setReward', [reward])

    def setResult(self, avId):
        if avId and self.enabled:
            self.power += 1
            self.time = int(CannonGlobals.CANNON_TIMEOUT / self.power)
            taskMgr.remove(self.taskName('gameover'))
            taskMgr.doMethodLater(self.time, self.__gameOver, self.taskName('gameover'))
            self.d_updateState()

    def __gameOver(self, task):
        self.enabled = 0
        self.time = 0
        self.d_updateState()
        minutes = random.randrange(0, 3)
        half = random.randrange(0, 2)
        if half or minutes == 0:
            minutes += 0.5
        taskMgr.doMethodLater(minutes * 60, self.__startNewGame, self.taskName('newGame'))
        for avId in self.scoreDict:
            av = self.air.doId2do.get(avId)
            if av:
                if av.zoneId == self.zoneId:
                    av.toonUp(2 ** self.power)

        return task.done

    def __startNewGame(self, task):
        self.enabled = 1
        self.__newGame()
        self.d_updateState()
        taskMgr.doMethodLater(self.time, self.__gameOver, self.taskName('gameover'))
        return task.done

    def setBonus(self, bonus):
        pass

    def setCurPinballScore(self, avId, score, bonus):
        av = self.air.doId2do.get(avId)
        if not av:
            return
        S = score * bonus
        self.scoreDict[avId] = S
        if S > self.highscore:
            self.highscore = S
            self.d_updateHighscore(av, S)

    def d_updateHighscore(self, av, score):
        self.sendUpdate('setPinballHiScorer', [av.getName()])
        self.sendUpdate('setPinballHiScore', [score])

    def delete(self):
        taskMgr.remove(self.taskName('newGame'))
        taskMgr.remove(self.taskName('gameover'))
