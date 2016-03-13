from toontown.toonbase.ToonBaseGlobal import *
from direct.interval.IntervalGlobal import *
from direct.distributed.ClockDelta import *
from direct.showbase import Audio3DManager
from toontown.toonbase import ToontownGlobals
import cPickle
from DistributedToonInterior import DistributedToonInterior
from toontown.dna.DNADoor import DNADoor
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import ClassicFSM, State
from direct.distributed import DistributedObject
from direct.fsm import State
from direct.actor import Actor
import random
import time
import ToonInteriorColors
from toontown.hood import ZoneUtil
from toontown.toon import ToonDNA
from toontown.toon import ToonHead
from toontown.ai import HolidayGlobals
from toontown.toon import NPCToons
from otp.nametag.NametagConstants import *


class DistributedToonHallInterior(DistributedToonInterior):

	def __init__(self, cr):
		DistributedToonInterior.__init__(self, cr)
		self.npcs = False
		
	def setup(self):
		self.dnaStore = base.cr.playGame.dnaStore
		self.randomGenerator = random.Random()
		self.randomGenerator.seed(self.zoneId)
		interior = loader.loadModel('phase_3.5/models/modules/tt_m_ara_int_toonhall')
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
		DNADoor.setupDoor(doorNP, self.interior, door_origin,
						  self.dnaStore, str(self.block), color)
		doorFrame = doorNP.find('door_*_flat')
		doorFrame.wrtReparentTo(self.interior)
		doorFrame.setColor(color)
		del self.colors
		del self.dnaStore
		del self.randomGenerator
		self.interior.flattenMedium()
		self.enterSetup()
	
	def NpcMaker(self):
		self.npcs = True
		self.dimn = NPCToons.createLocalNPC(2018)
		self.dimn.reparentTo(self.interior.find('**/npc_origin_2'))
		self.dimn.setPickable(0)
		self.dimn.initializeBodyCollisions('toon')
		self.dimn.addActive()
		self.dimn.startBlink()
		self.dimn.setH(180)
		self.dimn.loop('scientistWork')
		meter = loader.loadModel('phase_4/models/props/tt_m_prp_acs_sillyReader')
		rHand = self.dimn.find('**/rightHand')
		placeholder = rHand.attachNewNode('ClipBoard')
		meter.reparentTo(placeholder)
		placeholder.setH(180)
		placeholder.setScale(1.0)
		placeholder.setPos(0, 0, 0.1)
		
		self.surlee = NPCToons.createLocalNPC(2019)
		self.surlee.reparentTo(self.interior.find('**/npc_origin_1'))
		self.surlee.setPickable(0)
		self.surlee.initializeBodyCollisions('toon')
		self.surlee.addActive()
		self.surlee.startBlink()
		self.surlee.rightHands = []
		self.surlee.setupToonNodes()
		self.surlee.setH(180)
		self.surlee.loop('scientistJealous')
		clipBoard = loader.loadModel('phase_4/models/props/tt_m_prp_acs_clipboard')
		rHand = self.surlee.find('**/rightHand')
		placeholder = rHand.attachNewNode('ClipBoard')
		clipBoard.reparentTo(placeholder)
		placeholder.setH(180)
		placeholder.setScale(1.0)
		placeholder.setPos(0, 0, 0.1)
		
		self.prepostera = NPCToons.createLocalNPC(2020)
		self.prepostera.reparentTo(self.interior.find('**/npc_origin_3'))
		self.prepostera.setPickable(0)
		self.prepostera.initializeBodyCollisions('toon')
		self.prepostera.addActive()
		self.prepostera.startBlink()
		self.prepostera.loop('victory')
		phrases = ['Toons be as silly as you can to bring the silly meter to its Maximum!', 'Keep being silly!', 'Doctor Surlee how is the resarch going?', 'Doctor Dimm, any shocking discoveries?', 'The Silly Levels are rising!', 'Gadzooks! The Silly Meter has come back to life!', "It's rising every day, and will reach the top soon!"]
		self.Talk = Sequence(Wait(3), Func(self.prepostera.setChatAbsolute, random.choice(phrases), CFSpeech | CFTimeout), Wait(5), Func(self.prepostera.setChatAbsolute, random.choice(phrases), CFSpeech | CFTimeout), Wait(10), Func(self.prepostera.setChatAbsolute, random.choice(phrases), CFSpeech | CFTimeout), Wait(5), Func(self.prepostera.setChatAbsolute, random.choice(phrases), CFSpeech | CFTimeout), Wait(5), Func(self.prepostera.setChatAbsolute,  random.choice(phrases), CFSpeech | CFTimeout), Wait(5), Func(self.prepostera.setChatAbsolute, random.choice(phrases), CFSpeech | CFTimeout), Wait(5), Func(self.prepostera.setChatAbsolute, random.choice(phrases), CFSpeech | CFTimeout), Wait(5))
		self.Talk.loop()
		
	def enterSetup(self):
		ropes = loader.loadModel('phase_4/models/modules/tt_m_ara_int_ropes')
		ropes.reparentTo(self.interior)
		self.flatDuck = loader.loadModel(
			'phase_3.5/models/modules/tt_m_ara_int_scientistDuckFlat')
		loc1 = self.interior.find('**/npc_origin_1')
		if loc1:
			self.flatDuck.reparentTo(loc1)
		self.flatDuck.hide()
		self.flatMonkey = loader.loadModel(
			'phase_3.5/models/modules/tt_m_ara_int_scientistMonkeyFlat')
		loc1 = self.interior.find('**/npc_origin_2')
		if loc1:
			self.flatMonkey.reparentTo(loc1)
		self.flatMonkey.hide()
		self.flatHorse = loader.loadModel(
			'phase_3.5/models/modules/tt_m_ara_int_scientistHorseFlat')
		loc1 = self.interior.find('**/npc_origin_3')
		if loc1:
			self.flatHorse.reparentTo(loc1)
		self.flatHorse.hide()
		self.audio3d = Audio3DManager.Audio3DManager(
			base.sfxManagerList[0], camera)
		self.phase1Sfx = self.audio3d.loadSfx(
			'phase_4/audio/sfx/tt_s_prp_sillyMeterPhaseOne.ogg')
		self.phase1Sfx.setLoop(True)
		self.phase2Sfx = self.audio3d.loadSfx(
			'phase_4/audio/sfx/tt_s_prp_sillyMeterPhaseTwo.ogg')
		self.phase2Sfx.setLoop(True)
		self.phase3Sfx = self.audio3d.loadSfx(
			'phase_4/audio/sfx/tt_s_prp_sillyMeterPhaseThree.ogg')
		self.phase3Sfx.setLoop(True)
		self.phase4Sfx = self.audio3d.loadSfx(
			'phase_4/audio/sfx/tt_s_prp_sillyMeterPhaseFour.ogg')
		self.phase4Sfx.setLoop(True)
		self.phase4To5Sfx = self.audio3d.loadSfx(
			'phase_4/audio/sfx/tt_s_prp_sillyMeterPhaseFourToFive.ogg')
		self.phase4To5Sfx.setLoop(False)
		self.phase5Sfx = self.audio3d.loadSfx(
			'phase_4/audio/sfx/tt_s_prp_sillyMeterPhaseFive.ogg')
		self.phase5Sfx.setLoop(True)
		self.arrowSfx = self.audio3d.loadSfx(
			'phase_4/audio/sfx/tt_s_prp_sillyMeterArrow.ogg')
		self.arrowSfx.setLoop(False)
		self.audio3d.setDropOffFactor(0.1)
		if HolidayGlobals.WhatHolidayIsIt() == 'April Toons':
			self.sillyMeter = Actor.Actor(
			'phase_4/models/props/tt_a_ara_ttc_sillyMeter_default',
				{
					'arrowTube': 'phase_4/models/props/tt_a_ara_ttc_sillyMeter_arrowFluid',
					'phaseOne': 'phase_4/models/props/tt_a_ara_ttc_sillyMeter_phaseOne',
					'phaseTwo': 'phase_4/models/props/tt_a_ara_ttc_sillyMeter_phaseTwo',
					'phaseThree': 'phase_4/models/props/tt_a_ara_ttc_sillyMeter_phaseThree',
					'phaseFour': 'phase_4/models/props/tt_a_ara_ttc_sillyMeter_phaseFour',
					'phaseFourToFive': 'phase_4/models/props/tt_a_ara_ttc_sillyMeter_phaseFourToFive',
					'phaseFive': 'phase_4/models/props/tt_a_ara_ttc_sillyMeter_phaseFive'})
			self.smPhase1 = self.sillyMeter.find('**/stage1')
			self.smPhase2 = self.sillyMeter.find('**/stage2')
			self.smPhase3 = self.sillyMeter.find('**/stage3')
			self.smPhase4 = self.sillyMeter.find('**/stage4')
			self.smPhase2.hide()
			self.smPhase3.hide()
			self.smPhase4.hide()
			thermometerLocator = self.sillyMeter.findAllMatches(
				'**/uvj_progressBar')[1]
			thermometerMesh = self.sillyMeter.find('**/tube')
			thermometerMesh.setTexProjector(
				thermometerMesh.findTextureStage('default'),
				thermometerLocator, self.sillyMeter)
			self.sillyMeter.flattenMedium()
			self.sillyMeter.makeSubpart(
				'arrow', ['uvj_progressBar*', 'def_springA'])
			self.sillyMeter.makeSubpart(
				'meter', ['def_pivot'], [
					'uvj_progressBar*', 'def_springA'])
			self.sillyMeter.reparentTo(self.interior)
			self.sillyMeter.enableBlend()
			self.sillyMeter.setControlEffect('arrowTube', 0.8)
			self.sillyMeter.setControlEffect('phaseFour', 0.8)
			self.sillyMeter.loop('arrowTube')
			self.sillyMeter.loop('phaseFour')
			self.phase4Sfx.play()
			self.NpcMaker()
		else:
			self.SillyMeter = loader.loadModel(
			'phase_3.5/models/modules/tt_m_ara_int_sillyMeterFlat')
			self.flatSillyMeter.reparentTo(self.interior)
			self.SillyMeter.show()
			self.flatDuck.show()
			self.flatMonkey.show()
			self.flatHorse.show()

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
		self.camChangeNP = base.localAvatar.getPart(
			'torso', '1000').attachNewNode(cn)
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

	def cleanUpSounds(self):

		def __cleanUpSound__(soundFile):
			if soundFile.status() == soundFile.PLAYING:
				soundFile.setLoop(False)
				soundFile.stop()

		if hasattr(self, 'audio3d'):
			self.audio3d.disable()
			del self.audio3d
		if hasattr(self, 'phase1Sfx'):
			__cleanUpSound__(self.phase1Sfx)
			del self.phase1Sfx
		if hasattr(self, 'phase2Sfx'):
			__cleanUpSound__(self.phase2Sfx)
			del self.phase2Sfx
		if hasattr(self, 'phase3Sfx'):
			__cleanUpSound__(self.phase3Sfx)
			del self.phase3Sfx
		if hasattr(self, 'phase4Sfx'):
			__cleanUpSound__(self.phase4Sfx)
			del self.phase4Sfx
		if hasattr(self, 'phase4To5Sfx'):
			__cleanUpSound__(self.phase4To5Sfx)
			del self.phase4To5Sfx
		if hasattr(self, 'phase5Sfx'):
			__cleanUpSound__(self.phase5Sfx)
			del self.phase5Sfx
		if hasattr(self, 'arrowSfx'):
			__cleanUpSound__(self.arrowSfx)
			del self.arrowSfx

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
		self.sillyMeter.removeNode()
		self.cleanUpSounds()
		DistributedToonInterior.disable(self)
		if self.npcs == True:
			self.dimn.stopBlink()
			self.dimn.removeActive()
			self.dimn.cleanup()
			self.dimn.removeNode()

			self.surlee.stopBlink()
			self.surlee.removeActive()
			self.surlee.cleanup()
			self.surlee.removeNode()
			
			self.Talk.finish()
			self.prepostera.stopBlink()
			self.prepostera.removeActive()
			self.prepostera.cleanup()
			self.prepostera.removeNode()
		else:
			self.flatDuck.removeNode()
			self.flatMonkey.removeNode()
			self.flatHorse.removeNode()

	def delete(self):
		DistributedToonInterior.delete(self)
