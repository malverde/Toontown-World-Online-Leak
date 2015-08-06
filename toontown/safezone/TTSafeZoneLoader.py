from pandac.PandaModules import *
import SafeZoneLoader
import TTPlayground
import random
from toontown.launcher import DownloadForceAcknowledge
from otp.nametag.NametagConstants import *
if config.GetBool('want-flippy-pet-intro', True):
	from toontown.pets import Pet
	from toontown.pets import PetDNA
	from toontown.toon import NPCToons
	from otp.nametag.NametagConstants import *
	from direct.actor import Actor


class TTSafeZoneLoader(SafeZoneLoader.SafeZoneLoader):

    def __init__(self, hood, parentFSM, doneEvent):
		SafeZoneLoader.SafeZoneLoader.__init__(self, hood, parentFSM, doneEvent)
		self.playgroundClass = TTPlayground.TTPlayground
		self.musicFile = 'phase_4/audio/bgm/TC_nbrhood.ogg'
		self.activityMusicFile = 'phase_3.5/audio/bgm/TC_SZ_activity.ogg'
		self.dnaFile = 'phase_4/dna/toontown_central_sz.xml'
		self.safeZoneStorageDNAFile = 'phase_4/dna/storage_TT_sz.xml'
		if config.GetBool('want-flippy-pet-intro', True):
			self.flippyBlatherSequence = Sequence()
			self.fluffy = None

 
    def load(self):
		if config.GetBool('want-flippy-pet-intro', True):
			self.flippy = NPCToons.createLocalNPC(2001)
			self.flippy.reparentTo(render)
			self.flippy.setPickable(0)
			self.flippy.setPos(188, -260, 11.187)
			self.flippy.setH(108.411)
			self.flippy.initializeBodyCollisions('toon')
			self.flippy.addActive()
			self.flippy.startBlink()
			self.flippyBlatherSequence = Sequence(Wait(10), Func(self.flippy.setChatAbsolute, 'Welcome Toons, far and wide!', CFSpeech | CFTimeout), Func(self.flippy.play, 'wave'), Func(self.flippy.loop, 'neutral'), Wait(5), Func(self.flippy.setChatAbsolute, "We're glad you could join us today!", CFSpeech | CFTimeout), Wait(8), Func(self.flippy.setChatAbsolute, "I'm here to open the first Toontown pet shop!", CFSpeech | CFTimeout), Wait(8), Func(self.flippy.setChatAbsolute, "We will open a pet shop in each playground!", CFSpeech | CFTimeout), Wait(8), Func(self.flippy.setChatAbsolute,  "Once you buy a 'doodle' you can go tou your estate and play with him or her!", CFSpeech | CFTimeout), Wait(8), Func(self.flippy.setChatAbsolute, 'Doctor Surlee says there are more types of these "doodles"', CFSpeech | CFTimeout), Wait(8), Func(self.flippy.setChatAbsolute, "Different pets behave differently!", CFSpeech | CFTimeout), Wait(8), Func(self.flippy.setChatAbsolute, 'Anyway, what are you waiting for?', CFSpeech | CFTimeout), Wait(8), Func(self.flippy.setChatAbsolute, 'Go in the pet shop and get a doodle!', CFSpeech | CFTimeout), Wait(8), Func(self.flippy.setChatAbsolute, 'Then go to your estate and play with your pet!', CFSpeech | CFTimeout))
			self.flippyBlatherSequence.loop()
			self.fluffy = Pet.Pet()
			self.fluffy.addActive()
			self.flippy.startBlink()
			self.fluffy.setDNA(PetDNA.getRandomPetDNA())
			self.fluffy.setName('Fluffy')
			self.fluffy.setPickable(0)
			self.fluffy.reparentTo(render)
			self.fluffy.setPos(191, -263, 11.382)
			self.fluffy.setH(829)
			self.fluffy.enterNeutralHappy()
			self.fluffy.initializeBodyCollisions('pet')
			SafeZoneLoader.SafeZoneLoader.load(self)
		self.birdSound = map(base.loadSfx, ['phase_4/audio/sfx/SZ_TC_bird1.ogg', 'phase_4/audio/sfx/SZ_TC_bird2.ogg', 'phase_4/audio/sfx/SZ_TC_bird3.ogg'])

    def unload(self):
		del self.birdSound
		SafeZoneLoader.SafeZoneLoader.unload(self)
		if config.GetBool('want-flippy-pet-intro', True):
			if self.flippy:
				self.flippy.stopBlink()
				self.flippy.removeActive()
				self.flippy.cleanup()
				self.flippy.removeNode()
			if self.fluffy:
				self.fluffy.stopBlink()
				self.fluffy.removeActive()
				self.fluffy.enterOff()
				self.fluffy.cleanup()
				self.fluffy.removeNode()

    def enter(self, requestStatus):
        SafeZoneLoader.enter(self, requestStatus)

    def exit(self):
        SafeZoneLoader.exit(self)

