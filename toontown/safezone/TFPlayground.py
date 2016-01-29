from panda3d.core import *
from toontown.toonbase import ToontownGlobals
import Playground
from toontown.launcher import DownloadForceAcknowledge
from toontown.building import Elevator
from toontown.toontowngui import TTDialog
from toontown.toonbase import TTLocalizer
from toontown.racing import RaceGlobals

from toontown.safezone import PicnicBasket
from toontown.safezone import GolfKart
from direct.task.Task import Task
from direct.fsm import ClassicFSM, State


class TFPlayground(Playground.Playground):

    def __init__(self, loader, parentFSM, doneEvent):
        Playground.Playground.__init__(self, loader, parentFSM, doneEvent)
        self.parentFSM = parentFSM
        self.activityFsm = ClassicFSM.ClassicFSM('Activity', [State.State('off', self.enterOff, self.exitOff, ['OnBase1', 'OnBase2', 'OnBase3']),
         State.State('OnBase1', self.enterOnBase1, self.exitOnBase1, ['off', 'OnBase2', 'OnBase3']),
         State.State('OnBase2', self.enterOnBase2, self.exitOnBase2, ['off', 'OnBase1', 'OnBase3']),
         State.State('OnBase3', self.enterOnBase3, self.exitOnBase3, ['off', 'OnBase2', 'OnBase1'])], 'off', 'off')
        self.activityFsm.enterInitialState()
        self.picnicBasketBlockDoneEvent = 'picnicBasketBlockDone'
        self.fsm.addState(State.State('picnicBasketBlock', self.enterPicnicBasketBlock, self.exitPicnicBasketBlock, ['walk']))
        state = self.fsm.getStateNamed('walk')
        state.addTransition('picnicBasketBlock')
        self.picnicBasketDoneEvent = 'picnicBasketDone'

    def load(self):
        Playground.Playground.load(self)

    def unload(self):
        Playground.Playground.unload(self)

    def enter(self, requestStatus):
        Playground.Playground.enter(self, requestStatus)

    def exit(self):
        Playground.Playground.exit(self)
        self.loader.hood.setNoFog()

    def doRequestLeave(self, requestStatus):
        self.fsm.request('trialerFA', [requestStatus])

    def enterPicnicBasketBlock(self, picnicBasket):
        base.localAvatar.laffMeter.start()
        base.localAvatar.b_setAnimState('off', 1)
        base.localAvatar.cantLeaveGame = 1
        self.accept(self.picnicBasketDoneEvent, self.handlePicnicBasketDone)
        self.trolley = PicnicBasket.PicnicBasket(self, self.fsm, self.picnicBasketDoneEvent, picnicBasket.getDoId(), picnicBasket.seatNumber)
        self.trolley.load()
        self.trolley.enter()

    def exitOff(self):
        return None

    def exitPicnicBasketBlock(self):
        base.localAvatar.laffMeter.stop()
        base.localAvatar.cantLeaveGame = 0
        self.ignore(self.trolleyDoneEvent)
        self.trolley.unload()
        self.trolley.exit()
        del self.trolley

    def enterOnBase1(self):
        base.localAvatar.b_setParent(ToontownGlobals.SPToonfestTowerLarge)

    def exitOnBase1(self):
        base.localAvatar.b_setParent(ToontownGlobals.SPRender)

    def enterOnBase2(self):
        base.localAvatar.b_setParent(ToontownGlobals.SPToonfestTowerMed)

    def exitOnBase2(self):
        base.localAvatar.b_setParent(ToontownGlobals.SPRender)

    def enterOnBase3(self):
        base.localAvatar.b_setParent(ToontownGlobals.SPToonfestTowerSmall)

    def exitOnBase3(self):
        base.localAvatar.b_setParent(ToontownGlobals.SPRender)

    def detectedPicnicTableSphereCollision(self, picnicBasket):
        self.fsm.request('picnicBasketBlock', [picnicBasket])

    def handleStartingBlockDone(self, doneStatus):
        self.notify.debug('handling StartingBlock done event')
        where = doneStatus['where']
        if where == 'reject':
            self.fsm.request('walk')
        elif where == 'exit':
            self.fsm.request('walk')
        elif where == 'racetrack':
            self.doneStatus = doneStatus
            messenger.send(self.doneEvent)
        else:
            self.notify.error('Unknown mode: ' + where + ' in handleStartingBlockDone')

    def handlePicnicBasketDone(self, doneStatus):
        self.notify.debug('handling picnic basket done event')
        mode = doneStatus['mode']
        if mode == 'reject':
            self.fsm.request('walk')
        elif mode == 'exit':
            self.fsm.request('walk')
        else:
            self.notify.error('Unknown mode: ' + mode + ' in handlePicnicBasketDone')
