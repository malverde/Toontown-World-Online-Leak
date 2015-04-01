import random

from TrolleyConstants import *
from direct.directnotify import DirectNotifyGlobal
from direct.distributed import DistributedObjectAI
from direct.distributed.ClockDelta import *
from direct.fsm import ClassicFSM, State
from otp.ai.AIBase import *
from toontown.golf import GolfGlobals
from toontown.golf import GolfManagerAI
from toontown.toonbase.ToontownGlobals import *


class DistributedGolfKartAI(DistributedObjectAI.DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedGolfKartAI')

    def __init__(self, air, golfCourse, x, y, z, h, p, r):
        DistributedObjectAI.DistributedObjectAI.__init__(self, air)
        self.seats = [None, None, None, None]
        self.golfCourse = golfCourse
        self.posHpr = (x, y, z, h, p, r)
        self.chooseColor()
        self.accepting = 0
        self.trolleyCountdownTime = simbase.config.GetFloat(
            'trolley-countdown-time', TROLLEY_COUNTDOWN_TIME)
        self.fsm = ClassicFSM.ClassicFSM(
            'DistributedGolfKartAI',
            [
                State.State('off', self.enterOff, self.exitOff, ['entering']),
                State.State('entering', self.enterEntering, self.exitEntering, ['waitEmpty']),
                State.State('waitEmpty', self.enterWaitEmpty, self.exitWaitEmpty, ['waitCountdown']),
                State.State('waitCountdown', self.enterWaitCountdown, self.exitWaitCountdown, ['waitEmpty', 'allAboard']),
                State.State('allAboard', self.enterAllAboard, self.exitAllAboard, ['leaving', 'waitEmpty']),
                State.State('leaving', self.enterLeaving, self.exitLeaving, ['entering'])
            ], 'off', 'off')
        self.fsm.enterInitialState()

    def delete(self):
        self.fsm.requestFinalState()
        del self.fsm
        DistributedObjectAI.DistributedObjectAI.delete(self)

    def findAvailableSeat(self):
        for i in xrange(len(self.seats)):
            if self.seats[i] is None:
                return i

    def findAvatar(self, avId):
        for i in xrange(len(self.seats)):
            if self.seats[i] == avId:
                return i

    def countFullSeats(self):
        avCounter = 0
        for i in self.seats:
            if i:
                avCounter += 1
        return avCounter

    def rejectingBoardersHandler(self, avId):
        self.rejectBoarder(avId)

    def rejectBoarder(self, avId):
        self.sendUpdateToAvatarId(avId, 'rejectBoard', [avId])

    def acceptingBoardersHandler(self, avId):
        self.notify.debug('acceptingBoardersHandler')
        seatIndex = self.findAvailableSeat()
        if seatIndex is None:
            self.rejectBoarder(avId)
        else:
            self.acceptBoarder(avId, seatIndex)

    def acceptBoarder(self, avId, seatIndex):
        self.notify.debug('acceptBoarder')
        if self.findAvatar(avId) is not None:
            return
        self.seats[seatIndex] = avId
        self.acceptOnce(
            self.air.getAvatarExitEvent(avId),
            self.__handleUnexpectedExit, extraArgs=[avId])
        self.timeOfBoarding = globalClock.getRealTime()
        self.sendUpdate('fillSlot' + str(seatIndex), [avId])
        self.waitCountdown()

    def __handleUnexpectedExit(self, avId):
        self.notify.warning('Avatar: ' + str(avId) + ' has exited unexpectedly')
        seatIndex = self.findAvatar(avId)
        if seatIndex is None:
            return
        self.clearFullNow(seatIndex)
        self.clearEmptyNow(seatIndex)
        if self.countFullSeats() == 0:
            self.waitEmpty()

    def rejectingExitersHandler(self, avId):
        self.rejectExiter(avId)

    def rejectExiter(self, avId):
        pass

    def acceptingExitersHandler(self, avId):
        self.acceptExiter(avId)

    def acceptExiter(self, avId):
        seatIndex = self.findAvatar(avId)
        if seatIndex is None:
            return
        self.clearFullNow(seatIndex)
        self.sendUpdate('emptySlot' + str(seatIndex), [avId, globalClockDelta.getRealNetworkTime()])
        if self.countFullSeats() == 0:
            self.waitEmpty()
        taskMgr.doMethodLater(
            TOON_EXIT_TIME, self.clearEmptyNow,
            self.uniqueName('clearEmpty-%s' % seatIndex),
            extraArgs=(seatIndex,))

    def clearEmptyNow(self, seatIndex):
        self.sendUpdate('emptySlot' + str(seatIndex), [0, globalClockDelta.getRealNetworkTime()])

    def clearFullNow(self, seatIndex):
        avId = self.seats[seatIndex]
        if avId == 0:
            self.notify.warning('Clearing an empty seat index: ' + str(seatIndex) + ' ... Strange...')
        else:
            self.seats[seatIndex] = None
            self.sendUpdate('fillSlot' + str(seatIndex), [0])
            if avId:
                self.ignore(self.air.getAvatarExitEvent(avId))

    def d_setState(self, state):
        self.sendUpdate('setState', [state, globalClockDelta.getRealNetworkTime()])

    def getState(self):
        return self.fsm.getCurrentState().getName()

    def requestBoard(self, *args):
        self.notify.debug('requestBoard')
        avId = self.air.getAvatarIdFromSender()
        if self.findAvatar(avId) != None:
            self.notify.warning('Ignoring multiple requests from %s to board.' % avId)
            return None
        av = self.air.doId2do.get(avId)
        if av:
            newArgs = (avId,) + args
            if av.hp > 0 and self.accepting:
                self.acceptingBoardersHandler(*newArgs)
            else:
                self.rejectingBoardersHandler(*newArgs)
        else:
            self.notify.warning('avid: %s does not exist, but tried to board a trolley' % avId)

    def requestExit(self, *args):
        self.notify.debug('requestExit')
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)
        if av:
            newArgs = (avId,) + args
            if self.accepting:
                self.acceptingExitersHandler(*newArgs)
            else:
                self.rejectingExitersHandler(*newArgs)
        else:
            self.notify.warning('avId: %s does not exist, but tried to exit a trolley' % avId)

    def start(self):
        self.enter()

    def enterOff(self):
        self.accepting = 0
        if hasattr(self, 'doId'):
            for seatIndex in xrange(4):
                taskMgr.remove(self.uniqueName('clearEmpty-' + str(seatIndex)))

    def exitOff(self):
        self.accepting = 0

    def enter(self):
        self.fsm.request('entering')

    def enterEntering(self):
        self.d_setState('entering')
        self.accepting = 0
        self.seats = [None, None, None, None]
        taskMgr.doMethodLater(
            TROLLEY_ENTER_TIME, self.waitEmptyTask,
            self.uniqueName('entering-timer'))

    def exitEntering(self):
        self.accepting = 0
        taskMgr.remove(self.uniqueName('entering-timer'))

    def waitEmptyTask(self, task):
        self.waitEmpty()
        return Task.done

    def waitEmpty(self):
        self.fsm.request('waitEmpty')

    def enterWaitEmpty(self):
        self.d_setState('waitEmpty')
        self.accepting = 1

    def exitWaitEmpty(self):
        self.accepting = 0

    def waitCountdown(self):
        self.fsm.request('waitCountdown')

    def enterWaitCountdown(self):
        self.d_setState('waitCountdown')
        self.accepting = 1
        taskMgr.doMethodLater(
            self.trolleyCountdownTime, self.timeToGoTask,
            self.uniqueName('countdown-timer'))

    def timeToGoTask(self, task):
        if self.countFullSeats() > 0:
            self.allAboard()
        else:
            self.waitEmpty()
        return Task.done

    def exitWaitCountdown(self):
        self.accepting = 0
        taskMgr.remove(self.uniqueName('countdown-timer'))

    def allAboard(self):
        self.fsm.request('allAboard')

    def enterAllAboard(self):
        self.accepting = 0
        currentTime = globalClock.getRealTime()
        elapsedTime = currentTime - self.timeOfBoarding
        self.notify.debug('elapsed time: ' + str(elapsedTime))
        waitTime = max(TOON_BOARD_TIME - elapsedTime, 0)
        taskMgr.doMethodLater(
            waitTime, self.leaveTask, self.uniqueName('waitForAllAboard'))

    def exitAllAboard(self):
        self.accepting = 0
        taskMgr.remove(self.uniqueName('waitForAllAboard'))

    def leaveTask(self, task):
        if self.countFullSeats() > 0:
            self.leave()
        else:
            self.waitEmpty()
        return Task.done

    def leave(self):
        self.fsm.request('leaving')

    def enterLeaving(self):
        self.d_setState('leaving')
        self.accepting = 0
        taskMgr.doMethodLater(
            TROLLEY_EXIT_TIME, self.trolleyLeftTask,
            self.uniqueName('leaving-timer'))

    def trolleyLeftTask(self, task):
        self.trolleyLeft()
        return Task.done

    def trolleyLeft(self):
        numPlayers = self.countFullSeats()
        avIdList = []
        if numPlayers > 0:
            for seatIndex in xrange(len(self.seats)):
                avId = self.seats[seatIndex]
                avIdList.append(avId)
                self.clearFullNow(seatIndex)
            golfManager = GolfManagerAI.GolfManagerAI()
            golfZone = golfManager.readyGolfCourse(avIdList, self.golfCourse)
            for avId in avIdList:
                if avId:
                    self.sendUpdateToAvatarId(avId, 'setGolfZone', [golfZone, 0])
        else:
            self.notify.warning('The trolley left, but was empty.')
        self.enter()

    def exitLeaving(self):
        self.accepting = 0
        self.chooseColor()
        self.sendUpdate('setColor', [self.color[0], self.color[1], self.color[2]])
        taskMgr.remove(self.uniqueName('leaving-timer'))

    def getGolfCourse(self):
        return self.golfCourse

    def getPosHpr(self):
        return self.posHpr

    def getColor(self):
        return self.color

    def chooseColor(self):
        self.color = (
            random.randint(
                GolfGlobals.KartColors[self.golfCourse][0][0],
                GolfGlobals.KartColors[self.golfCourse][0][1]
            ),
            random.randint(
                GolfGlobals.KartColors[self.golfCourse][1][0],
                GolfGlobals.KartColors[self.golfCourse][1][1]
            ),
            random.randint(
                GolfGlobals.KartColors[self.golfCourse][2][0],
                GolfGlobals.KartColors[self.golfCourse][2][1]
            )
        )
        if self.golfCourse == 1:
            if self.color[0] + self.color[1] <= 255:
                self.color = (
                    self.color[0],
                    self.color[0] + self.color[1],
                    self.color[2]
                )
            else:
                self.color = (self.color[0], 255, self.color[2])
