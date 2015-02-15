########################## THE TOON LAND PROJECT ##########################
# Filename: DistributedTrashCan.py
# Created by: Cody/Fd Green Cat Fd (February 16th, 2013)
####
# Description:
#
# The Trash Can actor, and client to client communications.
####

from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.actor.Actor import Actor
from direct.distributed import DistributedObject
from otp.otpbase import OTPGlobals

ESClosed = 0
ESOpen   = 1

class DistributedTrashCan(Actor, DistributedObject.DistributedObject):

    def __init__(self, cr, objectId, parent=render):
        Actor.__init__(self, 'phase_5/models/char/tt_r_ara_ttc_trashcan',
                      {'hiccup':'phase_5/models/char/tt_a_ara_ttc_trashcan_idleHiccup0'})
        self.waitDuration = self.getDuration('hiccup')
        self.persistenceFields = []
        self.bothFields = ['requestHiccup']
        self.reparentTo(parent)
        self.objectId = objectId
        self.doId = self.objectId
        self.triggerName = self.uniqueName('trigger')
        self.triggerEvent_enter = 'enter%s' % self.triggerName
        cs = CollisionSphere(0.0, 0.0, -1.4, 3.0)
        cs.setTangible(0)
        cn = CollisionNode(self.triggerName)
        cn.addSolid(cs)
        cn.setIntoCollideMask(OTPGlobals.WallBitmask)
        trigger = self.attachNewNode(cn)
        self.status = ESClosed
        self.accept(self.triggerEvent_enter, self.b_requestHiccup)

    def b_requestHiccup(self, collisionEntry):
        self.sendUpdate('requestHiccup', [])

    def toggleStatus(self):
        if self.status == ESClosed:
            self.status = ESOpen
        else:
            self.status = ESClosed

    def handleMessage(self, fieldName, args=[], sendToId=None, reciever=None):
        if fieldName == 'requestHiccup':
            if self.status != ESClosed:
                return None
            self.toggleStatus()
            self.animTrack = Sequence(Func(self.play, 'hiccup'),
             Wait(self.waitDuration), Func(self.toggleStatus)).start()

    def sendUpdate(self, fieldName, args=[], sendToId=None,
                    recieverId=None, overrideBoth=False, persistenceOverride=False):
        if sendToId == None:
            sendToId = base.localAvatar.doId
        if (fieldName in self.bothFields) and (not overrideBoth):
            self.handleMessage(fieldName, args, sendToId)
        if (fieldName in self.persistenceFields) and (not persistenceOverride):
            TTSendBuffer.TTSendBuffer.sendMessage(self.objectId, fieldName, args, sendToId, True)
        else:
            TTSendBuffer.TTSendBuffer.sendMessage(self.objectId, fieldName, args, sendToId, False)