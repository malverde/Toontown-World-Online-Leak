#Embedded file name: toontown.election.DistributedHotAirBalloon
from pandac.PandaModules import *
from otp.nametag.NametagConstants import *
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
from direct.distributed.DistributedObject import DistributedObject
from direct.fsm.FSM import FSM
from toontown.toon import NPCToons
from toontown.toonbase import ToontownGlobals
from direct.task import Task
from random import choice
import ElectionGlobals

class DistributedHotAirBalloon(DistributedObject, FSM):

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        FSM.__init__(self, 'HotAirBalloonFSM')
        self.avId = 0
        self.flightPathIndex = 0
        self.balloon = loader.loadModel('phase_4/models/events/election_slappyBalloon-static')
        self.balloon.reparentTo(base.render)
        self.balloon.setPos(*ElectionGlobals.BalloonBasePosition)
        self.balloon.setScale(ElectionGlobals.BalloonScale)
        self.cr.parentMgr.registerParent(ToontownGlobals.SPSlappysBalloon, self.balloon)
        self.collisionNP = self.balloon.find('**/Collision_Outer')
        self.slappy = NPCToons.createLocalNPC(2021)
        self.slappy.setPos(0.7, 0.7, 0.4)
        self.slappy.setH(150)
        self.slappy.setScale(1 / ElectionGlobals.BalloonScale)
        self.slappy.loop('neutral')
        self.flightPaths = ElectionGlobals.generateFlightPaths(self)
        self.toonFlightPaths = ElectionGlobals.generateToonFlightPaths(self)
        self.speechSequence = ElectionGlobals.generateSpeechSequence(self)

    def delete(self):
        self.demand('Off')
        self.ignore('enter' + self.collisionNP.node().getName())
        self.cr.parentMgr.unregisterParent(ToontownGlobals.SPSlappysBalloon)
        self.balloon.removeNode()
        if self.slappy:
            self.slappy.delete()
        DistributedObject.delete(self)

    def setState(self, state, timestamp, avId):
        if avId != self.avId:
            self.avId = avId
        self.demand(state, globalClockDelta.localElapsedTime(timestamp))

    def enterWaiting(self, offset):
        self.slappy.reparentTo(self.balloon)
        self.accept('enter' + self.collisionNP.node().getName(), self.__handleToonEnter)
        self.balloonIdle = Sequence(Wait(0.3), self.balloon.posInterval(3, (-15, 33, 1.5)), Wait(0.3), self.balloon.posInterval(3, (-15, 33, 1.1)))
        self.balloonIdle.loop()
        self.balloonIdle.setT(offset)

    def enterElectionIdle(self, offset):
        self.balloon.setPos(*ElectionGlobals.BalloonElectionPosition)
        self.balloon.setH(283)
        self.balloonElectionIdle = Sequence(self.balloon.posInterval(3, (166.5, 64.0, 52.0), blendType='easeInOut'), self.balloon.posInterval(3, (166.5, 64.0, 53.0), blendType='easeInOut'))
        self.balloonElectionIdle.loop()
        self.balloonElectionIdle.setT(offset)

    def enterElectionCrashing(self, offset):
        self.balloonElectionFall = Sequence(self.balloon.posHprInterval(17, (200.0, 20.0, 0.0), (105, -5, -5), blendType='easeInOut'), Func(self.balloon.hide))
        self.balloonElectionFall.start()
        self.balloonElectionFall.setT(offset)

    def __handleToonEnter(self, collEntry):
        if self.avId != 0:
            return
        if self.state != 'Waiting':
            return
        self.sendUpdate('requestEnter', [])

    def exitWaiting(self):
        self.balloonIdle.finish()
        self.ignore('enter' + self.collisionNP.node().getName())

    def exitElectionIdle(self):
        self.balloonElectionIdle.finish()

    def enterOccupied(self, offset):
        if self.avId == base.localAvatar.doId:
            base.localAvatar.disableAvatarControls()
            self.hopOnAnim = Sequence(Parallel(Func(base.localAvatar.b_setParent, ToontownGlobals.SPSlappysBalloon), Func(base.localAvatar.b_setAnimState, 'jump', 1.0)), base.localAvatar.posInterval(0.6, (0, 0, 2)), base.localAvatar.posInterval(0.4, (0, 0, 0.7)), Func(base.localAvatar.enableAvatarControls), Parallel(Func(base.localAvatar.b_setParent, ToontownGlobals.SPRender)))
            self.hopOnAnim.start()
        try:
            self.speechSequence = self.speechSequence
            self.speechSequence.start()
            self.speechSequence.setT(offset)
        except Exception as e:
            self.notify.debug('Exception: %s' % e)

    def exitOccupied(self):
        try:
            self.hopOnAnim.finish()
        except Exception as e:
            self.notify.debug('Exception: %s' % e)

    def setFlightPath(self, flightPathIndex):
        self.flightPathIndex = flightPathIndex

    def enterStartRide(self, offset):
        try:
            self.rideSequence = self.flightPaths[self.flightPathIndex]
            self.rideSequence.start()
            self.rideSequence.setT(offset)
        except Exception as e:
            self.notify.debug('Exception: %s' % e)

        if self.avId == base.localAvatar.doId:
            try:
                self.toonRideSequence = self.toonFlightPaths[self.flightPathIndex]
                self.toonRideSequence.start()
                self.toonRideSequence.setT(offset)
            except Exception as e:
                self.notify.debug('Exception: %s' % e)

    def exitStartRide(self):
        try:
            self.rideSequence.finish()
            self.speechSequence.finish()
        except Exception as e:
            self.notify.debug('Exception: %s' % e)

    def enterRideOver(self, offset):
        if self.avId == base.localAvatar.doId:
            base.localAvatar.disableAvatarControls()
            self.hopOffAnim = Sequence(Parallel(Func(base.localAvatar.b_setParent, ToontownGlobals.SPRender), Func(base.localAvatar.b_setAnimState, 'jump', 1.0)), Wait(0.3), base.localAvatar.posInterval(0.3, (-14, 25, 6)), base.localAvatar.posInterval(0.7, (-14, 20, 0)), Wait(0.3), Func(base.localAvatar.enableAvatarControls), Wait(0.3), Func(base.localAvatar.b_setAnimState, 'neutral'))
            self.hopOffAnim.start()
