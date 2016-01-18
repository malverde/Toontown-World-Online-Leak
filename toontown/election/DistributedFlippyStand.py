#Embedded file name: toontown.election.DistributedFlippyStand
from panda3d.core import *
from otp.nametag.NametagConstants import *
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
from direct.distributed.DistributedObject import DistributedObject
from direct.fsm.FSM import FSM
from direct.actor import Actor
from direct.task import Task
from toontown.toon import NPCToons
from toontown.suit import DistributedSuitBase, SuitDNA
from toontown.toonbase import ToontownGlobals
from toontown.battle import BattleProps
from otp.margins.WhisperPopup import *
import ElectionGlobals
from direct.directnotify import DirectNotifyGlobal
from random import choice
from otp.speedchat import SpeedChatGlobals

class DistributedFlippyStand(DistributedObject, FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedFlippyStand')

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        FSM.__init__(self, 'FlippyStandFSM')
        self.flippyStand = Actor.Actor('phase_4/models/events/election_flippyStand-mod', {'idle': 'phase_4/models/events/election_flippyStand-idle'})
        self.flippyStand.reparentTo(render)
        self.flippyStand.setScale(0.55)
        self.flippyStand.setHpr(315, 0, 349.7)
        self.flippyStand.setPos(180, -250, 9.58)
        self.flippyStand.exposeJoint(None, 'modelRoot', 'LInnerShoulder')
        flippyTable = self.flippyStand.find('**/LInnerShoulder')
        self.flippyStand.exposeJoint(None, 'modelRoot', 'Box_Joint')
        wheelbarrowJoint = self.flippyStand.find('**/Box_Joint').attachNewNode('Pie_Joint')
        wheelbarrow = self.flippyStand.find('**/Box')
        wheelbarrow.setPosHprScale(-2.39, 0.0, 1.77, 0.0, 0.0, 6.0, 1.14, 1.54, 0.93)
        pie = loader.loadModel('phase_3.5/models/props/tart')
        pieS = pie.copyTo(flippyTable)
        pieS.setPosHprScale(-2.61, -0.37, -1.99, 355.6, 90.0, 4.09, 1.6, 1.6, 1.6)
        for pieSettings in ElectionGlobals.FlippyWheelbarrowPies:
            pieModel = pie.copyTo(wheelbarrowJoint)
            pieModel.setPosHprScale(*pieSettings)

        wheelbarrowJoint.setPosHprScale(3.94, 0.0, 1.06, 270.0, 344.74, 0.0, 1.43, 1.12, 1.0)
        self.restockSfx = loader.loadSfx('phase_9/audio/sfx/CHQ_SOS_pies_restock.ogg')
        cs = CollisionBox(Point3(7, 0, 0), 12, 5, 18)
        self.pieCollision = self.flippyStand.attachNewNode(CollisionNode('wheelbarrow_collision'))
        self.pieCollision.node().addSolid(cs)
        self.accept('enter' + self.pieCollision.node().getName(), self.handleWheelbarrowCollisionSphereEnter)
        self.flippyStand.loop('idle')

    def delete(self):
        self.demand('Off')
        self.ignore('enter' + self.pieCollision.node().getName())
        self.flippyStand.removeNode()
        DistributedObject.delete(self)

    def handleWheelbarrowCollisionSphereEnter(self, collEntry):
        if 0 <= base.localAvatar.numPies < 20:
            self.sendUpdate('wheelbarrowAvatarEnter', [])
            self.restockSfx.play()
