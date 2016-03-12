import AnimatedProp
from direct.actor import Actor
from direct.interval.IntervalGlobal import *
from toontown.effects.Splash import *
from toontown.effects.Ripples import *
import random

class FishAnimatedProp:

    def __init__(self, node):
        self.fish = Actor.Actor('phase_4/models/props/SZ_fish-mod', {'jump': 'phase_4/models/props/SZ_fish-jump', 'swim': 'phase_4/models/props/SZ_fish-swim'}, copy=0)
        self.fish.hide()
        self.fish.reparentTo(node)
        self.splashSfxList = (loader.loadSfx('phase_4/audio/sfx/TT_splash1.ogg'), loader.loadSfx('phase_4/audio/sfx/TT_splash2.ogg'))
        self.geom = self.fish.getGeomNode()
        self.exitRipples = Ripples(self.geom)
        self.exitRipples.setBin('fixed', 25, 1)
        self.exitRipples.setPosHprScale(-0.3, 0.0, 1.24, 0.0, 0.0, 0.0, 0.7, 0.7, 0.7)
        self.splash = Splash(self.geom, wantParticles=0)
        self.splash.setPosHprScale(-1, 0.0, 1.23, 0.0, 0.0, 0.0, 0.7, 0.7, 0.7)
        randomSplash = random.choice(self.splashSfxList)
        self.track = Sequence(Wait(5 + 10 * random.random()), Parallel(Func(self.fish.show), self.fish.actorInterval('jump'), Sequence(Wait(0.25), Func(self.exitRipples.play, 0.75)), Sequence(Wait(1.13), Func(self.splash.play), SoundInterval(randomSplash, volume = 0.3, node = self.fish), Func(self.fish.hide))))

    def delete(self):
        self.exitRipples.destroy()
        del self.exitRipples
        self.splash.destroy()
        del self.splash
        del self.track
        self.fish.removeNode()
        del self.fish
        del self.geom

    def enter(self):
        self.track.loop()

    def exit(self):
        self.track.finish()
        self.splash.stop()
        self.exitRipples.stop()