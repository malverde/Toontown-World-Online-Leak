from pandac.PandaModules import *
from SafeZoneLoader import SafeZoneLoader
from Playground import Playground
from toontown.hood import ZoneUtil
from toontown.toonbase import ToontownGlobals
from toontown.effects import Bubbles
from toontown.safezone.TFPlayground import TFPlayground

class TFSafeZoneLoader(SafeZoneLoader):

    def __init__(self, hood, parentFSM, doneEvent):
        SafeZoneLoader.__init__(self, hood, parentFSM, doneEvent)
        self.playgroundClass = Playground
        self.musicFile = 'phase_6/audio/bgm/TF_SZ_1.ogg'
        self.activityMusicFile = 'phase_3.5/audio/bgm/TC_SZ_activity.ogg' # Temporary
        self.dnaFile = 'phase_6/dna/toonfest_sz.xml'
        self.safeZoneStorageDNAFile = 'phase_6/dna/storage_TF.xml'

    def load(self):
        SafeZoneLoader.load(self)




