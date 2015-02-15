########################## THE TOON LAND PROJECT ##########################
# Filename: FFPlayground.py
# Created by: Cody/Fd Green Cat Fd (January 31st, 2013)
####
# Description:
#
# The Funny Farm playground module.
####

import random
from toontown.safezone import Playground
from toontown.toonbase import ToontownGlobals
from direct.task.Task import Task
from toontown.launcher import DownloadForceAcknowledge
from toontown.hood import ZoneUtil
from direct.fsm import State

class FFPlayground(Playground.Playground):

    def __birds(self, task):
        if hasattr(self.loader, 'birdSound'):
            base.playSfx(random.choice(self.loader.birdSound))
            t = (random.random() * 20.0) + 1
            taskMgr.doMethodLater(t, self._FFPlayground__birds, 'FF-birds')
        return Task.done

    def __init__(self, loader, parentFSM, doneEvent):
        Playground.Playground.__init__(self, loader, parentFSM, doneEvent)
        self.parentFSM = parentFSM
        self.picnicBasketDoneEvent = 'picnicBasketDone'
        self.picnicBasketBlockDoneEvent = 'picnicBasketBlockDone'
        self.fsm.addState(State.State('picnicBasketBlock',
         self.enterPicnicBasketBlock, self.exitPicnicBasketBlock, ['walk']))
        state = self.fsm.getStateNamed('walk')
        state.addTransition('picnicBasketBlock')

    def detectedPicnicTableSphereCollision(self, picnicBasket):
        if picnicBasket.fullSeat2doId[picnicBasket.seatNumber] == 0:
            self.fsm.request('picnicBasketBlock', [picnicBasket])

    def enterPicnicBasketBlock(self, picnicBasket):
        base.localAvatar.laffMeter.start()
        base.localAvatar.cantLeaveGame = 1
        self.accept(self.picnicBasketDoneEvent, self.handlePicnicBasketDone)
        self.trolley = PicnicBasket.PicnicBasket(self, self.fsm,
         self.picnicBasketDoneEvent, picnicBasket.getDoId(), picnicBasket.seatNumber)
        self.trolley.load()
        self.trolley.enter()

    def exitPicnicBasketBlock(self):
        base.localAvatar.laffMeter.stop()
        base.localAvatar.cantLeaveGame = 0
        self.ignore(self.trolleyDoneEvent)
        self.trolley.unload()
        self.trolley.exit()
        del self.trolley

    def handlePicnicBasketDone(self, doneStatus):
        self.notify.debug('handling picnic basket done event')
        mode = doneStatus['mode']
        if mode == 'reject':
            self.fsm.request('walk')
        elif mode == 'exit':
            self.fsm.request('walk')
        else:
            self.notify.error('Unknown mode: ' + mode + ' in handlePicnicBasketDone')

    def doRequestLeave(self, requestStatus):
        self.fsm.request('trialerFA', [requestStatus])

    def enter(self, requestStatus):
        Playground.Playground.enter(self, requestStatus)
        taskMgr.doMethodLater(1, self._FFPlayground__birds, 'FF-birds')

    def exit(self):
        Playground.Playground.exit(self)
        taskMgr.remove('FF-birds')

    def load(self):
        Playground.Playground.load(self)

    def unload(self):
        Playground.Playground.unload(self)

    def enterDFA(self, requestStatus):
        doneEvent = 'dfaDoneEvent'
        self.accept(doneEvent, self.enterDFACallback, [requestStatus])
        self.dfa = DownloadForceAcknowledge.DownloadForceAcknowledge(doneEvent)
        hood = ZoneUtil.getCanonicalZoneId(requestStatus['hoodId'])
        if hood == ToontownGlobals.MyEstate:
            self.dfa.enter(base.cr.hoodMgr.getPhaseFromHood(ToontownGlobals.MyEstate))
        else:
            self.dfa.enter(5)

    def showPaths(self):
        return None