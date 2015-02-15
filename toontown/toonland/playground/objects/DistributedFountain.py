########################## THE TOON LAND PROJECT ##########################
# Filename: DistributedFountain.py
# Created by: Cody/Fd Green Cat Fd (February 17th, 2013)
####
# Description:
#
# Handles the fountains in Funny Farm, as well as some
# client to client communications.
####

import random
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.distributed import DistributedNode
from direct.actor.Actor import Actor
from otp.otpbase import OTPGlobals

class DistributedFountain(DistributedNode.DistributedNode):

    def __init__(self, cr, objectId):
        DistributedNode.DistributedNode.__init__(self, cr)
        NodePath.__init__(self, 'dgaFountain')
        self.persistenceFields = []
        self.bothFields = ['setGeyserAnim']
        self.done = True
        self.geyserTrack = None
        self.geyserModel = loader.loadModel('phase_6/models/golf/golf_geyser_model')
        self.geyserSound = loader.loadSfx('phase_6/audio/sfx/OZ_Geyser_No_Toon.mp3')
        self.fountainModel = loader.loadModel('phase_8/models/props/tt_m_ara_dga_fountain')
        self.fountainModel.reparentTo(self)
        self.fountainModel.find('**/fountainHead_dga').removeNode()
        geyserPlacer = self.attachNewNode('geyserPlacer')
        geyserPlacer.setPos(0, 0, 4)
        self.geyserSoundInterval = SoundInterval(self.geyserSound, node=geyserPlacer,
         listenerNode=base.camera, seamlessLoop=False, volume=0.6, cutOff=120)
        if self.geyserModel:
            self.geyserActor = Actor(self.geyserModel)
            self.geyserActor.loadAnims({'idle':'phase_6/models/golf/golf_geyser'})
            self.geyserActor.reparentTo(geyserPlacer)
            self.geyserActor.setScale(0.01)
            self.geyserActor.setPlayRate(8.6, 'idle')
            self.geyserActor.loop('idle')
            self.geyserActor.setDepthWrite(0)
            self.geyserActor.setTwoSided(True, 11)
            self.geyserActor.setColorScale(1.0, 1.0, 1.0, 1.0)
            self.geyserActor.setBin('fixed', 0)
            mesh = self.geyserActor.find('**/mesh_tide1')
            joint = self.geyserActor.find('**/uvj_WakeWhiteTide1')
            mesh.setTexProjector(mesh.findTextureStage('default'), joint, self.geyserActor)
            self.geyserActor.setZ(geyserPlacer.getZ() - 10.0)
            self.geyserPos = geyserPlacer.getPos()
            self.geyserPlacer = geyserPlacer
        self.objectId = objectId
        self.doId = self.objectId
        self.triggerName = self.uniqueName('trigger')
        self.triggerEvent_enter = 'enter%s' % self.triggerName
        cs = CollisionSphere(0.0, 0.0, -1.4, 4.0)
        cs.setTangible(0)
        cn = CollisionNode(self.triggerName)
        cn.addSolid(cs)
        cn.setIntoCollideMask(OTPGlobals.WallBitmask)
        trigger = self.attachNewNode(cn)
        self.accept(self.triggerEvent_enter, self.b_setGeyserAnim)

    def toggleGeyserDone(self):
        self.done = not self.done

    def b_setGeyserAnim(self, collisionEvent):
        self.sendUpdate('setGeyserAnim', [])

    def setGeyserAnim(self):
        if not self.done:
            return None
        self.toggleGeyserDone()
        maxSize = 0.12
        time = 1.0
        self.geyserTrack = Sequence()
        upPos = Vec3(self.geyserPos[0], self.geyserPos[1], self.geyserPos[2] - 8.0)
        downPos = Vec3(self.geyserPos[0], self.geyserPos[1], (self.geyserPos[2] - 8.0))
        self.geyserTrack.append(Parallel(LerpScaleInterval(self.geyserActor, (2.0 * time), 0.1, 0.01),
         LerpPosInterval(self.geyserActor, (2.0 * time), pos=downPos, startPos=downPos)))
        self.geyserTrack.append(Parallel(LerpScaleInterval(self.geyserActor, time, maxSize, 0.1),
         LerpPosInterval(self.geyserActor, time, pos=upPos, startPos=downPos)))
        self.geyserTrack.append(Parallel(LerpScaleInterval(self.geyserActor, (2.0 * time), 0.1, maxSize),
         LerpPosInterval(self.geyserActor, (2.0 * time), pos=downPos, startPos=upPos)))
        self.geyserTrack.append(Parallel(LerpScaleInterval(self.geyserActor, time, maxSize, 0.1),
         LerpPosInterval(self.geyserActor, time, pos=upPos, startPos=downPos)))
        self.geyserTrack.append(Parallel(LerpScaleInterval(self.geyserActor, (2.0 * time), 0.1, maxSize),
         LerpPosInterval(self.geyserActor, (2.0 * time), pos=downPos, startPos=upPos)))
        self.geyserTrack.append(Parallel(LerpScaleInterval(self.geyserActor, time, maxSize, 0.1),
         LerpPosInterval(self.geyserActor, time, pos=upPos, startPos=downPos)))
        self.geyserTrack.append(Parallel(LerpScaleInterval(self.geyserActor, (4.0 * time), 0.01, maxSize),
         LerpPosInterval(self.geyserActor, (4.0 * time), pos=downPos, startPos=upPos)))
        self.geyserTrack.append(Func(self.toggleGeyserDone))
        self.geyserTrack.start()
        self.geyserSoundInterval.start()

    def handleMessage(self, fieldName, args=[], sendToId=None, reciever=None):
        if fieldName == 'setGeyserAnim':
            self.setGeyserAnim()

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