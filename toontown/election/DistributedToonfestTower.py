#Embedded file name: toontown.election.DistributedToonfestTower
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

class DistributedToonfestTower(DistributedObject, FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedToonfestTower')

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        FSM.__init__(self, 'ToonfestTowerFSM')
        self.towerGeom = loader.loadModel('phase_6/models/events/tf_tower')
        self.towerGeom.reparentTo(render)
        self.towerGeom.setH(-30)
        self.towerGeom.setPos(221, -61, 4.5)
        self.base1 = self.towerGeom.find('**/base1')
        self.base2 = self.towerGeom.find('**/base2')
        self.base3 = self.towerGeom.find('**/base3')

    def delete(self):
        self.demand('Off')
        self.towerGeom.removeNode()
        DistributedObject.delete(self)

    def changeTowerSpeed(self, operation, base):
        self.validOperations = ['SpeedUp', 'SlowDown', 'Reverse']
        if operation not in self.validOperations:
            print 'DistributedToonfestTower: Operation %s is not a valid operation.' % operation
            operation = 'SpeedUp'
        if base < 0 or base > 2:
            print 'DistributedToonfestTower: Invalid base ' + str(base)
            base = 0
        print 'Made base ' + str(base + 1) + ' ' + operation
