########################## THE TOON LAND PROJECT ##########################
# Filename: DistributedPicnicBasket.py
# Created by: Cody/Fd Green Cat Fd (February 12th, 2013)
####
# Description:
#
# Handles the picnic tables in Funny Farm, as well as some
# client to client communications.
####

from toontown.safezone import DistributedPicnicBasket
from direct.distributed import DistributedObject
from toontown.toonbase import ToontownGlobals
from direct.fsm import ClassicFSM, State
from toontown.toon.LocalToon import globalClockDelta
from copy import deepcopy

class DistributedPicnicBasket(DistributedPicnicBasket.DistributedPicnicBasket):

    def __init__(self, cr):
        self.fullSeat2doId = [0, 0, 0, 0]
        self.persistenceFields = ['requestBoard']
        self.bothFields = ['requestBoard', 'requestExit']
        DistributedObject.DistributedObject.__init__(self, cr)
        self.localToonOnBoard = 0
        self.seed = 0
        self.random = None
        self.picnicCountdownTime = base.config.GetFloat('picnic-countdown-time',
         ToontownGlobals.PICNIC_COUNTDOWN_TIME)
        self.picnicBasketTrack = None
        self.fsm = ClassicFSM.ClassicFSM('DistributedTrolley', [State.State(
         'off', self.enterOff, self.exitOff, ['waitEmpty', 'waitCountdown']),
         State.State('waitEmpty', self.enterWaitEmpty, self.exitWaitEmpty, ['waitCountdown']),
         State.State('waitCountdown', self.enterWaitCountdown, self.exitWaitCountdown, ['waitEmpty'])],
         'off', 'off')
        self.fsm.enterInitialState()
        self._DistributedPicnicBasket__toonTracks = {}

    def handleMessage(self, fieldName, args=[], sendToId=None, reciever=None):
        if fieldName == 'requestBoard':
            if (sendToId in self.fullSeat2doId) or (self.fullSeat2doId[args[0]] != 0):
                return None
            if self.clockNode.currentTime == 0:
                self.fsm.request('waitCountdown', [globalClockDelta.getFrameNetworkTime()])
            if sendToId == base.localAvatar.doId:
                TTSendBuffer.TTSendBuffer.queued_messages.append((self.objectId, 'resyncTime', [], base.localAvatar.doId))
            self.fullSeat2doId[args[0]] = sendToId
            if reciever:
                base.cr.doId2do.get(sendToId).setPos(self.tablecloth.getPos())
            self.fillSlot(args[0], sendToId)
        elif fieldName == 'requestExit':
            if not sendToId in self.fullSeat2doId:
                return None
            if sendToId == base.localAvatar.doId:
                base.cr.playGame.getPlace().trolley.disableExitButton()
                for queuedMessage in deepcopy(TTSendBuffer.TTSendBuffer.queued_messages):
                    if queuedMessage[1] in ('requestBoard', 'resyncTime'):
                        index = TTSendBuffer.TTSendBuffer.queued_messages.index(queuedMessage)
                        del TTSendBuffer.TTSendBuffer.queued_messages[index]
            seatIndex = self.fullSeat2doId.index(sendToId)
            self.fullSeat2doId[seatIndex] = 0
            if self.fullSeat2doId == [0, 0, 0, 0]:
                self.clockNode.stop()
                self.clockNode.reset()
                ts = globalClockDelta.getFrameNetworkTime()
                self.setState('waitEmpty', self.seed, ts)
            self.emptySlot(seatIndex, sendToId, globalClockDelta.getFrameNetworkTime())
        elif fieldName == 'doneExit':
            distributedObject = base.cr.doId2do.get(sendToId)
            if distributedObject:
                distributedObject.startSmooth()
        elif fieldName == 'resyncTime':
            self.clockNode.countdown(args[0], self.handleExitButton)

    def sendUpdate(self, fieldName, args=[], sendToId=None,
                    recieverId=None, overrideBoth=False, persistenceOverride=False):
        if fieldName == 'resyncTime':
            return TTSendBuffer.TTSendBuffer.sendMessage(self.objectId, fieldName,
             [self.clockNode.currentTime], base.localAvatar.doId, reciever=recieverId)
        if sendToId == None:
            sendToId = base.localAvatar.doId
        if (fieldName in self.bothFields) and (not overrideBoth):
            self.handleMessage(fieldName, args, sendToId)
        if (fieldName in self.persistenceFields) and (not persistenceOverride):
            TTSendBuffer.TTSendBuffer.sendMessage(self.objectId, fieldName, args, sendToId, True)
        else:
            TTSendBuffer.TTSendBuffer.sendMessage(self.objectId, fieldName, args, sendToId, False)