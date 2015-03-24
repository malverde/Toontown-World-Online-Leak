from toontown.toonbase.ToonBaseGlobal import *
from direct.interval.IntervalGlobal import *
from direct.distributed.ClockDelta import *
from direct.showbase import Audio3DManager
from toontown.toonbase import ToontownGlobals
import cPickle
from DistributedToonInterior import DistributedToonInterior
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import ClassicFSM, State
from direct.distributed import DistributedObject
from toontown.dna.DNAParser import DNADoor
from direct.fsm import State
from direct.actor import Actor
import random
import time
import ToonInteriorColors
from toontown.hood import ZoneUtil
from toontown.toon import ToonDNA
from toontown.toon import ToonHead

class DistributedToonHallInterior(DistributedToonInterior):

    def __init__(self, cr):
        DistributedToonInterior.__init__(self, cr)
        
    def setup(self):
        self.dnaStore = base.cr.playGame.dnaStore
        self.randomGenerator = random.Random()
        self.randomGenerator.seed(self.zoneId)
        interior = self.randomDNAItem('TI_hall', self.dnaStore.findNode)
        self.interior = interior.copyTo(render)
        hoodId = ZoneUtil.getCanonicalHoodId(self.zoneId)
        self.colors = ToonInteriorColors.colors[hoodId]
        self.replaceRandomInModel(self.interior)
        doorModelName = 'door_double_round_ul'
        if doorModelName[-1:] == 'r':
            doorModelName = doorModelName[:-1] + 'l'
        else:
            doorModelName = doorModelName[:-1] + 'r'
        door = self.dnaStore.findNode(doorModelName)
        door_origin = render.find('**/door_origin;+s')
        doorNP = door.copyTo(door_origin)
        door_origin.setScale(0.8, 0.8, 0.8)
        door_origin.setPos(door_origin, 0, -0.025, 0)
        color = self.randomGenerator.choice(self.colors['TI_door'])
        DNADoor.setupDoor(doorNP, self.interior, door_origin, self.dnaStore, str(self.block), color)
        doorFrame = doorNP.find('door_*_flat')
        doorFrame.wrtReparentTo(self.interior)
        doorFrame.setColor(color)
        del self.colors
        del self.dnaStore
        del self.randomGenerator
        self.interior.flattenMedium()


	self.sillyMeter = Actor.Actor('phase_4/models/props/tt_a_ara_ttc_sillyMeter_default', {'arrowTube': 'phase_4/models/props/tt_a_ara_ttc_sillyMeter_arrowFluid',
         'phaseOne': 'phase_4/models/props/tt_a_ara_ttc_sillyMeter_phaseOne',
         'phaseTwo': 'phase_4/models/props/tt_a_ara_ttc_sillyMeter_phaseTwo',
         'phaseThree': 'phase_4/models/props/tt_a_ara_ttc_sillyMeter_phaseThree',
         'phaseFour': 'phase_4/models/props/tt_a_ara_ttc_sillyMeter_phaseFour',
         'phaseFourToFive': 'phase_4/models/props/tt_a_ara_ttc_sillyMeter_phaseFourToFive',
         'phaseFive': 'phase_4/models/props/tt_a_ara_ttc_sillyMeter_phaseFive'})
        self.sillyMeter.reparentTo(self.interior)
        self.sillyMeter.enableBlend()
        self.sillyMeter.setControlEffect('arrowTube', 1)
        self.sillyMeter.setControlEffect('phaseFour', 1)
        self.sillyMeter.loop('arrowTube')
        self.sillyMeter.loop('phaseFour')
        
    def enterFlat(self):
 
        self.flatSillyMeter.show()
        self.flatDuck.show()
        self.flatMonkey.show()
        self.flatHorse.show()

    def exitFlat(self):

        self.flatSillyMeter.hide()
        self.flatDuck.hide()
        self.flatMonkey.hide()
        self.flatHorse.hide()

    

    def enterToon(self):
        self.toonhallView = (Point3(0, -5, 3),
         Point3(0, 12.0, 7.0),
         Point3(0.0, 10.0, 5.0),
         Point3(0.0, 10.0, 5.0),
         1)
        self.setupCollisions(2.5)
        self.firstEnter = 1
        self.accept('CamChangeColl' + '-into', self.handleCloseToWall)

    def exitToon(self):
        pass

    def handleCloseToWall(self, collEntry):
        if self.firstEnter == 0:
            return
        interiorRopes = self.interior.find('**/*interior_ropes')
        if interiorRopes == collEntry.getIntoNodePath().getParent():
            return
        self.restoreCam()
        self.accept('CamChangeColl' + '-exit', self.handleAwayFromWall)

    def handleAwayFromWall(self, collEntry):
        if self.firstEnter == 1:
            self.cleanUpCollisions()
            self.setupCollisions(0.75)
            self.oldView = base.localAvatar.cameraIndex
            base.localAvatar.addCameraPosition(self.toonhallView)
            self.firstEnter = 0
            self.setUpToonHallCam()
            return
        flippy = self.interior.find('**/*Flippy*/*NPCToon*')
        if flippy == collEntry.getIntoNodePath():
            self.setUpToonHallCam()

    def setupCollisions(self, radius):
        r = base.localAvatar.getClampedAvatarHeight() * radius
        cs = CollisionSphere(0, 0, 0, r)
        cn = CollisionNode('CamChangeColl')
        cn.addSolid(cs)
        cn.setFromCollideMask(ToontownGlobals.WallBitmask)
        cn.setIntoCollideMask(BitMask32.allOff())
        self.camChangeNP = base.localAvatar.getPart('torso', '1000').attachNewNode(cn)
        self.cHandlerEvent = CollisionHandlerEvent()
        self.cHandlerEvent.addInPattern('%fn-into')
        self.cHandlerEvent.addOutPattern('%fn-exit')
        base.cTrav.addCollider(self.camChangeNP, self.cHandlerEvent)

    def cleanUpCollisions(self):
        base.cTrav.removeCollider(self.camChangeNP)
        self.camChangeNP.detachNode()
        if hasattr(self, 'camChangeNP'):
            del self.camChangeNP
        if hasattr(self, 'cHandlerEvent'):
            del self.cHandlerEvent

    
    def setUpToonHallCam(self):
        base.localAvatar.setCameraFov(75)
        base.localAvatar.setCameraSettings(self.toonhallView)

    def restoreCam(self):
        base.localAvatar.setCameraFov(ToontownGlobals.DefaultCameraFov)
        if hasattr(self, 'oldView'):
            base.localAvatar.setCameraPositionByIndex(self.oldView)

    def disable(self):
        self.setUpToonHallCam()
        base.localAvatar.removeCameraPosition()
        base.localAvatar.resetCameraPosition()
        self.restoreCam()
        self.ignoreAll()
        self.cleanUpCollisions()
        if hasattr(self, 'sillyFSM'):
            self.sillyFSM.requestFinalState()
            del self.sillyFSM
        DistributedToonInterior.disable(self)

    def delete(self):
        DistributedToonInterior.delete(self)
