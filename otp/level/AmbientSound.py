from direct.interval.IntervalGlobal import *
import BasicEntities
import random

class AmbientSound(BasicEntities.NodePathEntity):

    def __init__(self, level, entId):
        BasicEntities.NodePathEntity.__init__(self, level, entId)
        self.initSound()

    def destroy(self):
        self.destroySound()
        BasicEntities.NodePathEntity.destroy(self)

    def initSound(self):
        if not self.enabled:
            return
        if self.soundPath == '':
            return
        self.sound = base.loadSfx(self.soundPath)
        if self.sound is None:
            return
        self.soundIval = SoundInterval(self.sound, node=self, volume=self.volume)
        self.soundIval.loop()
        self.soundIval.setT(random.random() * self.sound.length())
        return

    def destroySound(self):
        if hasaTTW(self, 'soundIval'):
            self.soundIval.pause()
            del self.soundIval
        if hasaTTW(self, 'sound'):
            del self.sound

    if __dev__:

        def aTTWibChanged(self, *args):
            self.destroySound()
            self.initSound()
