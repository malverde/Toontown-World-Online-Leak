#Embedded file name: toontown.cogdominium.DistCogdoFlyingGameAI
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.ClockDelta import *
from toontown.battle import BattleBase
from toontown.building.ElevatorConstants import *
from toontown.cogdominium.DistCogdoGameAI import DistCogdoGameAI
import CogdoFlyingGameGlobals as Globals

class DistCogdoFlyingGameAI(DistCogdoGameAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistCogdoFlyingGameAI')
    delayIntro = BattleBase.ELEVATOR_T + ElevatorData[ELEVATOR_NORMAL]['openTime']

    def __init__(self, air):
        DistCogdoGameAI.__init__(self, air)
        self.completed = []
        self.eagles = {}
        self.totalMemos = 0

    def requestAction(self, action, data):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)
        if not av:
            return
        if action == Globals.AI.GameActions.LandOnWinPlatform:
            self.completed.append(avId)
            for toon in self.toons:
                if toon not in self.completed:
                    return

            self.gameDone()
        elif action == Globals.AI.GameActions.BladeLost:
            self.sendUpdate('toonBladeLost', [avId])
        elif action == Globals.AI.GameActions.SetBlades:
            self.sendUpdate('toonSetBlades', [avId, data])
        elif action == Globals.AI.GameActions.Died:
            damage = Globals.AI.SafezoneId2DeathDamage[self.getSafezoneId()]
            self.__damage(av, damage)
            self.sendUpdate('toonDied', [avId, globalClockDelta.getRealNetworkTime()])
        elif action == Globals.AI.GameActions.Spawn:
            self.sendUpdate('toonSpawn', [avId, globalClockDelta.getRealNetworkTime()])
        elif action == Globals.AI.GameActions.RequestEnterEagleInterest:
            if not self.eagles.get(data):
                self.eagles[data] = avId
                self.sendUpdate('toonSetAsEagleTarget', [avId, data, globalClockDelta.getRealNetworkTime()])
        elif action == Globals.AI.GameActions.RequestExitEagleInterest:
            if self.eagles.get(data) == avId:
                self.eagles[data] = 0
                self.sendUpdate('toonClearAsEagleTarget', [avId, data, globalClockDelta.getRealNetworkTime()])
        elif action == Globals.AI.GameActions.HitLegalEagle:
            damage = Globals.AI.SafezoneId2LegalEagleDamage[self.getSafezoneId()]
            self.__damage(av, damage)
        elif action == Globals.AI.GameActions.HitMinion:
            damage = Globals.AI.SafezoneId2MinionDamage[self.getSafezoneId()]
            self.__damage(av, damage)
        elif action == Globals.AI.GameActions.HitWhirlwind:
            damage = Globals.AI.SafezoneId2WhirlwindDamage[self.getSafezoneId()]
            self.__damage(av, damage)
        elif action == Globals.AI.GameActions.RanOutOfTimePenalty:
            damage = int(20 * self.getDifficulty())
            self.__damage(av, damage)
        else:
            self.notify.warning("Client requested unknown action '%s'" % action)

    def requestPickUp(self, pickupNum, pickupType):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)
        if not av:
            return
        if pickupType <= len(Globals.Level.GatherableTypes):
            self.sendUpdate('pickUp', [avId, pickupNum, globalClockDelta.getRealNetworkTime()])
            if pickupType == Globals.Level.GatherableTypes.LaffPowerup:
                av.toonUp(int(27 * self.getDifficulty()) + 3)
            if pickupType == Globals.Level.GatherableTypes.Memo:
                self.totalMemos += 1
        else:
            self.notify.warning("Client requested unknown pickup '%s'" % pickupType)

    def handleStart(self):
        for toon in self.toons:
            self.acceptOnce(self.air.getAvatarExitEvent(toon), self.__handleAvExit, [toon])

    def __handleAvExit(self, toon):
        if self.air:
            if toon in self.toons:
                self.toons.remove(toon)
                self.ignore(self.air.getAvatarExitEvent(toon))
                if not self.toons:
                    self.gameDone(failed=True)

    def requestDelete(self):
        DistCogdoGameAI.requestDelete(self)
        self.ignoreAll()

    def __removeToon(self, avId):
        if avId not in self.toons:
            return
        self.toons.pop(self.toons.index(avId))
        if len(self.toons) == 0:
            self.gameDone(failed=True)

    def __damage(self, av, damage):
        av.takeDamage(damage)
        if av.getHp() < 1:
            self.__removeToon(av.doId)

    def getTotalMemos(self):
        return self.totalMemos


from otp.ai.MagicWordGlobal import *

@magicWord(category=CATEGORY_OVERRIDE)
def endFlying():
    if hasattr(simbase.air, 'cogdoGame'):
        flyingGame = simbase.air.cogdoGame
        flyingGame.requestAction(Globals.AI.GameActions.LandOnWinPlatform, 0)
        return 'Ended Flying Game'
