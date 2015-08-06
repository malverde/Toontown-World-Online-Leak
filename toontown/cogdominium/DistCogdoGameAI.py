#Embedded file name: toontown.cogdominium.DistCogdoGameAI
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.distributed.ClockDelta import *
import CogdoGameConsts

class DistCogdoGameAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistCogdoGameAI')
    delayIntro = 0.1

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        air.cogdoGame = self
        self.interiorId = 0
        self.exteriorZone = 0
        self.difficultyOverrides = [2147483647, -1]
        self.requests = {}
        self.toons = []

    def announceGenerate(self):
        DistributedObjectAI.announceGenerate(self)
        self.finishEvent = self.uniqueName('CogdoMazeGameDone')
        self.gameOverEvent = self.uniqueName('CogdoMazeGameLose')
        self.resetRequests()

    def d_startIntro(self):
        self.sendUpdate('setVisible', [])
        taskMgr.doMethodLater(self.delayIntro, self.__startIntro, self.taskName('CogdoStartIntro'))

    def getInterior(self):
        return self.air.doId2do.get(self.interiorId)

    def resetRequests(self):
        interior = self.getInterior()
        toons = interior.getToons()[0]
        for toon in toons:
            self.requests[toon] = 0

    def __startIntro(self, task = None):
        self.sendUpdate('setIntroStart', [])
        if task:
            return task.done

    def setAvatarReady(self):
        avId = self.air.getAvatarIdFromSender()
        self.requests[avId] = 1
        if avId not in self.toons:
            self.toons.append(avId)
        if self.allToonsReady():
            self.handleStart()
            self.sendUpdate('setGameStart', [globalClockDelta.getRealNetworkTime()])

    def allToonsReady(self):
        interior = self.getInterior()
        toons = interior.getToons()[0]
        for toon in toons:
            if self.requests.get(toon, 0) == 0:
                return 0

        return 1

    def handleStart(self):
        pass

    def setInteriorId(self, id):
        self.interiorId = id

    def getInteriorId(self):
        return self.interiorId

    def setExteriorZone(self, zone):
        self.exteriorZone = zone

    def getExteriorZone(self):
        return self.exteriorZone

    def setDifficultyOverrides(self, difficulty, exteriorDifficulty):
        self.difficultyOverrides = [difficulty, exteriorDifficulty]

    def getDifficultyOverrides(self):
        return self.difficultyOverrides

    def toonWentSad(self, avId):
        self.sendUpdate('setToonSad', [avId])

    def setToons(self, toons):
        self.toons = toons

    def disable(self):
        DistributedObjectAI.disable(self)
        self.air.cogdoGame = None
        del self.air.cogdoGame

    def gameDone(self, failed = False):
        if not failed:
            if len(self.toons) == 0:
                failed = True
        if not failed:
            messenger.send(self.finishEvent, [self.toons])
        else:
            messenger.send(self.gameOverEvent)

    def getDifficulty(self):
        return CogdoGameConsts.getDifficulty(self.getSafezoneId())

    def getSafezoneId(self):
        return CogdoGameConsts.getSafezoneId(self.exteriorZone)
