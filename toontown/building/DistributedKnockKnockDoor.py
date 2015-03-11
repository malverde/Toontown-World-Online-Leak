from direct.directnotify import DirectNotifyGlobal
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *

import DistributedAnimatedProp
from KnockKnockJokes import *
from toontown.chat.ChatGlobals import *
from toontown.distributed import DelayDelete
from toontown.nametag.NametagGlobals import *
from toontown.nametag.NametagGroup import NametagGroup
from toontown.toonbase import TTLocalizer
from toontown.toonbase import ToontownGlobals


class DistributedKnockKnockDoor(DistributedAnimatedProp.DistributedAnimatedProp):
    def __init__(self, cr):
        DistributedAnimatedProp.DistributedAnimatedProp.__init__(self, cr)

        self.fsm.setName('DistributedKnockKnockDoor')
        self.rimshot = None
        self.knockSfx = None

    def generate(self):
        DistributedAnimatedProp.DistributedAnimatedProp.generate(self)

        self.avatarTracks = []
        self.avatarId = 0

    def announceGenerate(self):
        DistributedAnimatedProp.DistributedAnimatedProp.announceGenerate(self)

        self.accept('exitKnockKnockDoorSphere_' + str(self.propId), self.exitTrigger)
        self.acceptAvatar()

    def disable(self):
        self.ignoreAll()

        DistributedAnimatedProp.DistributedAnimatedProp.disable(self)

    def delete(self):
        DistributedAnimatedProp.DistributedAnimatedProp.delete(self)

        if self.rimshot:
            self.rimshot = None
        if self.knockSfx:
            self.knockSfx = None

    def acceptAvatar(self):
        self.acceptOnce('enterKnockKnockDoorSphere_' + str(self.propId), self.enterTrigger)

    def setAvatarInteract(self, avatarId):
        DistributedAnimatedProp.DistributedAnimatedProp.setAvatarInteract(self, avatarId)

    def avatarExit(self, avatarId):
        if avatarId == self.avatarId:
            for track in self.avatarTracks:
                track.finish()
                DelayDelete.cleanupDelayDeletes(track)

            self.avatarTracks = []

    def knockKnockTrack(self, avatar, duration):
        if avatar is None:
            return
        self.rimshot = base.loadSfx('phase_5/audio/sfx/AA_heal_telljoke.ogg')
        self.knockSfx = base.loadSfx('phase_5/audio/sfx/GUI_knock_3.ogg')
        joke = KnockKnockJokes[self.propId % len(KnockKnockJokes)]
        place = base.cr.playGame.getPlace()
        doorName = TTLocalizer.DoorNametag
        self.nametag = None
        self.nametagNP = None
        doorNP = render.find('**/KnockKnockDoorSphere_' + str(self.propId) + ';+s')
        if doorNP.isEmpty():
            self.notify.warning('Could not find KnockKnockDoorSphere_%s' % self.propId)
            return
        self.nametag = NametagGroup()
        self.nametag.setAvatar(doorNP)
        toonFont = ToontownGlobals.getToonFont()
        self.nametag.setFont(toonFont)
        self.nametag.setChatFont(toonFont)
        self.nametag.setText(doorName)
        self.nametag.setActive(False)
        self.nametag.hideNametag()
        self.nametag.manage(base.marginManager)
        self.nametag.getNametag3d().setBillboardOffset(6)
        nametagNode = self.nametag.getNametag3d()
        self.nametagNP = render.attachNewNode(nametagNode)
        self.nametagNP.setName('knockKnockDoor_nt_' + str(self.propId))
        pos = doorNP.getBounds().getCenter()
        self.nametagNP.setPos(pos + Vec3(0, 0, avatar.getHeight() + 2))
        d = duration * 0.125
        track = Sequence(Parallel(Sequence(Wait(d * 0.5), SoundInterval(self.knockSfx)), Func(self.nametag.setChatText, TTLocalizer.DoorKnockKnock), Wait(d)), Func(avatar.setChatAbsolute, TTLocalizer.DoorWhosThere, CFSpeech | CFTimeout, openEnded=0), Wait(d), Func(self.nametag.setChatText, joke[0]), Wait(d), Func(avatar.setChatAbsolute, joke[0] + TTLocalizer.DoorWhoAppendix, CFSpeech | CFTimeout, openEnded=0), Wait(d), Func(self.nametag.setChatText, joke[1]), Parallel(SoundInterval(self.rimshot, startTime=2.0), Wait(d * 4)), Func(self.cleanupTrack))
        track.delayDelete = DelayDelete.DelayDelete(avatar, 'knockKnockTrack')
        return track

    def cleanupTrack(self):
        avatar = self.cr.doId2do.get(self.avatarId, None)
        if avatar:
            avatar.clearChat()
        if self.nametag:
            self.nametag.unmanage(base.marginManager)
            self.nametagNP.removeNode()
            self.nametag.destroy()
        self.nametag = None
        self.nametagNP = None
        return

    def enterOff(self):
        DistributedAnimatedProp.DistributedAnimatedProp.enterOff(self)

    def exitOff(self):
        DistributedAnimatedProp.DistributedAnimatedProp.exitOff(self)

    def enterAttract(self, ts):
        DistributedAnimatedProp.DistributedAnimatedProp.enterAttract(self, ts)
        self.acceptAvatar()

    def exitAttract(self):
        DistributedAnimatedProp.DistributedAnimatedProp.exitAttract(self)

    def enterPlaying(self, ts):
        DistributedAnimatedProp.DistributedAnimatedProp.enterPlaying(self, ts)
        if self.avatarId:
            avatar = self.cr.doId2do.get(self.avatarId, None)
            track = self.knockKnockTrack(avatar, 8)
            if track != None:
                track.start(ts)
                self.avatarTracks.append(track)
        return

    def exitPlaying(self):
        DistributedAnimatedProp.DistributedAnimatedProp.exitPlaying(self)
        for track in self.avatarTracks:
            track.finish()
            DelayDelete.cleanupDelayDeletes(track)

        self.avatarTracks = []
        self.avatarId = 0
