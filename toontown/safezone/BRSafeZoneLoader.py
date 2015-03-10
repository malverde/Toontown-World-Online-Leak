from toontown.battle import BattleParticles
from toontown.safezone import BRPlayground
from toontown.safezone import SafeZoneLoader


class BRSafeZoneLoader(SafeZoneLoader.SafeZoneLoader):
    def __init__(self, hood, parentFSM, doneEvent):
        SafeZoneLoader.SafeZoneLoader.__init__(self, hood, parentFSM, doneEvent)
        self.playgroundClass = BRPlayground.BRPlayground
        self.musicFile = 'phase_8/audio/bgm/TB_nbrhood.ogg'
        self.activityMusicFile = 'phase_8/audio/bgm/TB_SZ_activity.ogg'
        self.dnaFile = 'phase_8/dna/the_burrrgh_sz.pdna'
        self.safeZoneStorageDNAFile = 'phase_8/dna/storage_BR_sz.pdna'

    def load(self):
        SafeZoneLoader.SafeZoneLoader.load(self)
        self.windSound = map(base.loadSfx, ['phase_8/audio/sfx/SZ_TB_wind_1.ogg',
                                            'phase_8/audio/sfx/SZ_TB_wind_2.ogg',
                                            'phase_8/audio/sfx/SZ_TB_wind_3.ogg'])
        self.snow = BattleParticles.loadParticleFile('snowdisk.ptf')
        self.snow.setPos(0, 0, 5)
        self.snowRender = self.geom.attachNewNode('snowRender')
        self.snowRender.setDepthWrite(0)
        self.snowRender.setBin('fixed', 1)

    def unload(self):
        SafeZoneLoader.SafeZoneLoader.unload(self)
        del self.windSound
        del self.snow
        del self.snowRender

    def enter(self, requestStatus):
        SafeZoneLoader.SafeZoneLoader.enter(self, requestStatus)
        self.snow.start(camera, self.snowRender)

    def exit(self):
        SafeZoneLoader.SafeZoneLoader.exit(self)
        self.snow.cleanup()
        self.snowRender.removeNode()