#Embedded file name: toontown.election.InvasionSuitBrainAI
import random
from pandac.PandaModules import *
from direct.fsm.FSM import FSM
from InvasionPathDataAI import pathfinder

class AttackBehavior(FSM):
    REASSESS_INTERVAL = 2.0

    def __init__(self, brain, toonId):
        FSM.__init__(self, 'AttackFSM')
        self.brain = brain
        self.toonId = toonId
        self._walkingTo = None
        self._walkTask = None

    def getToon(self):
        return self.brain.suit.invasion.getToon(self.toonId)

    def start(self):
        self.assessDistance()

    def assessDistance(self):
        toon = self.getToon()
        if toon is None:
            self.brain.demand('Idle')
            return
        toonPos = Point2(toon.getComponentX(), toon.getComponentY())
        distance = (toonPos - self.brain.suit.getCurrentPos()).length()
        if distance < self.brain.getAttackRange():
            self.demand('Attack')
        else:
            if self._walkingTo and (self._walkingTo - toonPos).length() < self.brain.getAttackRange():
                return
            self.demand('Walk', toonPos.getX(), toonPos.getY())

    def enterAttack(self):
        self.brain.suit.attack(self.toonId)

    def enterWalk(self, x, y):
        if not self.brain.navigateTo(x, y, self.brain.getAttackRange()):
            self.brain.master.toonUnreachable(self.toonId)
            self.brain.demand('Idle')
            return
        self._walkingTo = Point2(x, y)
        if self._walkTask:
            self._walkTask.remove()
        self._walkTask = taskMgr.doMethodLater(self.REASSESS_INTERVAL, self.__reassess, self.brain.suit.uniqueName('reassess-walking'))

    def __reassess(self, task):
        self.assessDistance()
        return task.again

    def exitWalk(self):
        self._walkingTo = None
        if self._walkTask:
            self._walkTask.remove()

    def onArrive(self):
        if self.state != 'Walk':
            return
        self.assessDistance()

    def onAttackCompleted(self):
        if self.state != 'Attack':
            return
        self.brain.demand('Idle')


class HarassBehavior(AttackBehavior):
    ATTACK_COOLDOWN = 3.0

    def onAttackCompleted(self):
        self.demand('AttackCooldown')

    def enterAttackCooldown(self):
        self.brain.suit.idle()
        self.__wait = taskMgr.doMethodLater(self.ATTACK_COOLDOWN, self.__waitOver, self.brain.suit.uniqueName('harass-cooldown'))

    def __waitOver(self, task):
        self.assessDistance()
        return task.done

    def exitAttackCooldown(self):
        self.__wait.remove()


class UnclumpBehavior(FSM):
    UNCLUMP_SCAN_RADIUS = 30
    UNCLUMP_MOVE_DISTANCE = 5
    UNCLUMP_WAIT_TIME = 1.0

    def __init__(self, brain):
        FSM.__init__(self, 'UnclumpFSM')
        self.brain = brain

    def start(self):
        moveVector = Vec2()
        ourSuit = self.brain.suit
        ourPos = ourSuit.getCurrentPos()
        for otherSuit in self.brain.suit.invasion.suits:
            if otherSuit == ourSuit:
                continue
            otherPos = otherSuit.getCurrentPos()
            moveAway = ourPos - otherPos
            if moveAway.length() > self.UNCLUMP_SCAN_RADIUS:
                continue
            moveMag = 1.0 / max(moveAway.lengthSquared(), 0.1)
            moveAway.normalize()
            moveAway *= moveMag
            moveVector += moveAway

        moveVector.normalize()
        x, y = ourPos + moveVector * self.UNCLUMP_MOVE_DISTANCE
        self.brain.navigateTo(x, y)
        self.demand('Walking')

    def enterWalking(self):
        pass

    def onArrive(self):
        if self.state == 'Walking':
            self.brain.demand('Idle')

    def enterWait(self):
        self.brain.suit.idle()
        self._waitDelay = taskMgr.doMethodLater(self.UNCLUMP_WAIT_TIME, self._doneWaiting, self.brain.suit.uniqueName('unclump-wait'))

    def _doneWaiting(self, task):
        self.brain.demand('Idle')
        return task.done

    def exitWait(self):
        self._waitDelay.remove()


class InvasionSuitBrainAI(FSM):
    PROXEMICS_INTERVAL = 0.5
    PERSONAL_SPACE = 5

    def __init__(self, suit):
        FSM.__init__(self, 'InvasionSuitBrainFSM')
        self.suit = suit
        self.master = self.suit.invasion.master
        self.behavior = None
        self.__proxemicsTask = None
        self.__waypoints = []

    def start(self):
        if self.state != 'Off':
            return
        self.demand('Idle')

    def stop(self):
        if self.state == 'Off':
            return
        self.demand('Off')

    def getAttackRange(self):
        return 20.0

    def enterOff(self):
        self.__stopProxemics()

    def exitOff(self):
        self.__startProxemics()

    def enterUnclump(self):
        self.__stopProxemics()
        self.behavior = UnclumpBehavior(self)
        self.behavior.start()

    def exitUnclump(self):
        self.__startProxemics()
        self.behavior.demand('Off')
        self.behavior = None

    def __startProxemics(self):
        if not self.__proxemicsTask:
            self.__proxemicsTask = taskMgr.doMethodLater(self.PROXEMICS_INTERVAL, self.__proxemics, self.suit.uniqueName('proxemics'))

    def __stopProxemics(self):
        if self.__proxemicsTask:
            self.__proxemicsTask.remove()
            self.__proxemicsTask = None

    def __proxemics(self, task):
        for otherSuit in self.suit.invasion.suits:
            if otherSuit == self.suit:
                continue
            if otherSuit.getActualLevel() < self.suit.getActualLevel():
                continue
            elif otherSuit.getActualLevel() == self.suit.getActualLevel() and otherSuit.doId > self.suit.doId:
                continue
            ourPos = self.suit.getCurrentPos()
            otherPos = otherSuit.getCurrentPos()
            if (ourPos - otherPos).length() < self.PERSONAL_SPACE:
                self.demand('Unclump')
                return task.done

        return task.again

    def enterIdle(self):
        self.suit.idle()
        self.master.requestOrders(self)

    def enterAttack(self, toonId):
        self.behavior = AttackBehavior(self, toonId)
        self.behavior.start()

    def exitAttack(self):
        self.behavior.demand('Off')
        self.behavior = None

    def enterHarass(self, toonId):
        self.behavior = HarassBehavior(self, toonId)
        self.behavior.start()

    def exitHarass(self):
        self.behavior.demand('Off')
        self.behavior = None

    def suitFinishedNavigating(self):
        if self.behavior:
            self.behavior.onArrive()

    def suitFinishedAttacking(self):
        if hasattr(self.behavior, 'onAttackCompleted'):
            self.behavior.onAttackCompleted()

    def navigateTo(self, x, y, closeEnough = 0):
        self.__waypoints = pathfinder.planPath(self.suit.getCurrentPos(), (x, y), closeEnough)
        if self.__waypoints:
            self.__walkToNextWaypoint()
            return True
        else:
            return False

    def suitFinishedWalking(self):
        if self.__waypoints:
            self.__walkToNextWaypoint()
        else:
            self.suitFinishedNavigating()

    def __walkToNextWaypoint(self):
        x, y = self.__waypoints.pop(0)
        self.suit.walkTo(x, y)
