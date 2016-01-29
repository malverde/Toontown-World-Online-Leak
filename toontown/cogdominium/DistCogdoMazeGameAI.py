#Embedded file name: toontown.cogdominium.DistCogdoMazeGameAI
from direct.directnotify import DirectNotifyGlobal
from toontown.cogdominium.DistCogdoGameAI import DistCogdoGameAI
import CogdoMazeGameGlobals
from direct.distributed.ClockDelta import *
from direct.task import Timer
from toontown.battle import BattleBase
from toontown.building.ElevatorConstants import *
ALL_ABOARD_LAG = 3.5
BASE_TOON_UP = 10
JOKE_TOON_UP = 5

class DistCogdoMazeGameAI(DistCogdoGameAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistCogdoMazeGameAI')
    delayIntro = BattleBase.ELEVATOR_T + ElevatorData[ELEVATOR_NORMAL]['openTime']

    def __init__(self, air):
        DistCogdoGameAI.__init__(self, air)
        self.numSuits = (0, 0, 0)
        self.timer = Timer.Timer()
        self.doorRevealed = False
        self.toonsInDoor = []
        self.bosses = {}
        self.fastMinions = {}
        self.slowMinions = {}
        self.suitTypes = [self.bosses, self.fastMinions, self.slowMinions]
        self.numJokes = {}

    def announceGenerate(self):
        DistCogdoGameAI.announceGenerate(self)
        self.setupSuitsAI()

    def setupSuitsAI(self):
        bossHp = CogdoMazeGameGlobals.SuitData[0]['hp']
        fastMiniHp = CogdoMazeGameGlobals.SuitData[1]['hp']
        slowMiniHp = CogdoMazeGameGlobals.SuitData[2]['hp']
        serialNum = 0
        for i in range(self.numSuits[0]):
            self.bosses[serialNum] = bossHp
            serialNum += 1

        for i in range(self.numSuits[1]):
            self.fastMinions[serialNum] = fastMiniHp
            serialNum += 1

        for i in range(self.numSuits[2]):
            self.slowMinions[serialNum] = slowMiniHp
            serialNum += 1

    def setNumSuits(self, num):
        self.numSuits = num

    def getNumSuits(self):
        return self.numSuits

    def requestUseGag(self, x, y, h, timestamp):
        avId = self.air.getAvatarIdFromSender()
        self.sendUpdate('toonUsedGag', [avId,
         x,
         y,
         h,
         globalClockDelta.getRealNetworkTime()])

    def requestSuitHitByGag(self, suitType, suitNum):
        hitAI = self.hitSuitAI(suitType, suitNum)
        if not hitAI:
            self.notify.warning('Cannot hit suit!')
            return
        avId = self.air.getAvatarIdFromSender()
        self.sendUpdate('suitHitByGag', [avId, suitType, suitNum])

    def requestHitBySuit(self, suitType, suitNum, nettime):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)
        if av:
            lostHp = CogdoMazeGameGlobals.SuitData[suitType]['toonDamage'] * self.getDifficulty() * 10
            av.takeDamage(lostHp)
            networkTime = globalClockDelta.getRealNetworkTime()
            self.sendUpdate('toonHitBySuit', [avId,
             suitType,
             suitNum,
             networkTime])
            if av.getHp() < 1:
                self.toonWentSad(avId)

    def requestHitByDrop(self):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)
        if av:
            lostHp = CogdoMazeGameGlobals.DropDamage
            av.takeDamage(lostHp)
            self.sendUpdate('toonHitByDrop', [avId])

    def requestPickUp(self, pickupNum):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)
        if av:
            now = globalClockDelta.getRealNetworkTime()
            if avId in self.numJokes:
                self.numJokes[avId] += 1
            else:
                self.numJokes[avId] = 1
            self.sendUpdate('pickUp', [avId, pickupNum, now])

    def requestGag(self, coolerIndex):
        avId = self.air.getAvatarIdFromSender()
        self.sendUpdate('hasGag', [avId, globalClockDelta.getRealNetworkTime()])

    def hitSuitAI(self, suitType, suitNum):
        cogKey = None
        for cogNum in self.suitTypes[suitType].keys():
            if cogNum == suitNum:
                cogKey = cogNum
                break

        if cogKey == None:
            return 0
        cogHp = self.suitTypes[suitType][cogKey]
        cogHp -= 1
        self.suitTypes[suitType][cogKey] = cogHp
        if cogHp <= 0:
            del self.suitTypes[suitType][cogKey]
        return 1

    def handleStart(self):
        taskMgr.add(self.__checkGameDone, self.taskName('check-game-done'))
        taskMgr.add(self.__checkPlayersTask, self.taskName('check-players-task'))
        serverDelay = 1.0
        self.timer.startCallback(CogdoMazeGameGlobals.SecondsUntilTimeout + serverDelay, self.__handleGameOver)
        taskMgr.doMethodLater(serverDelay, self.clientCountdown, self.taskName('client_countdown'))
        taskMgr.add(self.__timeWarningTask, self.taskName('time-warning-task'))

    def clientCountdown(self, task):
        self.doAction(CogdoMazeGameGlobals.GameActions.Countdown, 0)
        return task.done

    def __handleGameOver(self):
        self.removeAll()
        self.gameDone(failed=True)

    def __checkGameDone(self, task):
        bossesLeft = self.bosses
        if len(bossesLeft) == 0:
            self.timer.stop()
            self.doAction(CogdoMazeGameGlobals.GameActions.OpenDoor, 0)
            self.__startTimeout()
            return task.done
        return task.again

    def __startTimeout(self):
        self.timer.startCallback(CogdoMazeGameGlobals.SecondsUntilGameEnds, self.__handleTimeout)

    def __handleTimeout(self):
        for toon in self.toons:
            if toon not in self.toonsInDoor:
                self.killToon(toon)

        self.removeAll()
        self.gameDone()

    def __timeWarningTask(self, task):
        if self.timer.getT() <= CogdoMazeGameGlobals.SecondsForTimeAlert:
            self.doAction(CogdoMazeGameGlobals.GameActions.TimeAlert, 0)
            return task.done
        return task.again

    def killToon(self, avId):
        av = self.air.doId2do.get(avId)
        if av:
            if av.getHp() > 0:
                av.takeDamage(av.getHp())
            self.toonWentSad(avId)
        self.__playerDisconnected(avId)

    def __checkPlayersTask(self, task):
        for toonId in self.toons:
            toon = self.air.doId2do.get(toonId)
            if not toon:
                self.__playerDisconnected(toonId)

        return task.again

    def __playerDisconnected(self, avId):
        self.sendUpdate('setToonDisconnect', [avId])
        self.toons.pop(self.toons.index(avId))
        if len(self.toons) == 0:
            self.removeAll()
            self.gameDone(failed=True)

    def doAction(self, action, data):
        self.sendUpdate('doAction', [action, data, globalClockDelta.getRealNetworkTime()])

    def requestAction(self, action, data):
        Globals = CogdoMazeGameGlobals
        avId = self.air.getAvatarIdFromSender()
        if action == Globals.GameActions.RevealDoor:
            if not self.doorRevealed:
                self.doAction(action, avId)
                self.doorRevealed = True
            else:
                self.notify.warning("Toon tried to reveal door but it's already revealed! Ignoring.")
        elif action == Globals.GameActions.EnterDoor:
            if avId not in self.toonsInDoor:
                self.doAction(action, avId)
                self.toonsInDoor.append(avId)
                self.toonUpToon(avId)
            else:
                self.notify.warning('Toon tried to enter into door but already entered! Ignoring.')
                return
            if len(self.toonsInDoor) >= len(self.toons):
                self.__handleAllAboard()
        else:
            self.notify.warning("Client requested unknown action '%s'" % action)

    def __handleAllAboard(self):
        if len(self.toonsInDoor) != len(self.toons):
            self.notify.warning('__handleAllAboard expect all toons aboard!')
            return
        self.removeAll()
        taskMgr.doMethodLater(ALL_ABOARD_LAG, lambda t: self.gameDone(), self.taskName('all-aboard-delay'))

    def toonUpToon(self, toonId):
        if toonId in self.toonsInDoor:
            toon = self.air.doId2do.get(toonId)
            if toon:
                val = min(BASE_TOON_UP + JOKE_TOON_UP * self.numJokes.get(toonId, 0), toon.getMaxHp())
                toon.toonUp(val)

    def removeAll(self):
        taskMgr.remove(self.taskName('check-game-done'))
        taskMgr.remove(self.taskName('check-players-task'))
        taskMgr.remove(self.taskName('time-warning-task'))
        taskMgr.remove(self.taskName('all-aboard-delay'))
        self.timer.stop()

    def disable(self):
        DistCogdoGameAI.disable(self)
        self.removeAll()


from otp.ai.MagicWordGlobal import *

@magicWord(category=CATEGORY_OVERRIDE)
def endMaze():
    if hasattr(simbase.air, 'cogdoGame'):
        maze = simbase.air.cogdoGame
        maze.doAction(CogdoMazeGameGlobals.GameActions.OpenDoor, 0)
        return 'Completed Maze Game'
