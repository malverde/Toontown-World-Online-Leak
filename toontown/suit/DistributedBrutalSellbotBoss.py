from pandac.PandaModules import Point3, VBase3

from toontown.suit.DistributedSellbotBoss import DistributedSellbotBoss
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
from toontown.chat import ChatGlobals
from toontown.coghq import CogDisguiseGlobals
from toontown.suit import SuitDNA
from toontown.battle import SuitBattleGlobals

from direct.interval.IntervalGlobal import *


class DistributedBrutalSellbotBoss(DistributedSellbotBoss):
    notify = directNotify.newCategory('DistributedBrutalSellbotBoss')

    ANIM_PLAYRATE = 3

    def announceGenerate(self):
        DistributedSellbotBoss.announceGenerate(self)

        self.setName(TTLocalizer.BrutalSellbotBossName)
        base.localAvatar.setCanUseUnites(False)

    def disable(self):
        DistributedSellbotBoss.disable(self)

        base.localAvatar.setCanUseUnites(True)

    def makeIntroductionMovie(self, delayDeletes):
        track = Parallel()
        camera.reparentTo(render)
        camera.setPosHpr(0, 25, 30, 0, 0, 0)
        localAvatar.setCameraFov(ToontownGlobals.CogHQCameraFov)
        dooberTrack = Parallel()

        if self.doobers:
            self._DistributedSellbotBoss__doobersToPromotionPosition(self.doobers[:4], self.battleANode)
            self._DistributedSellbotBoss__doobersToPromotionPosition(self.doobers[4:], self.battleBNode)
            turnPosA = ToontownGlobals.SellbotBossDooberTurnPosA
            turnPosB = ToontownGlobals.SellbotBossDooberTurnPosB
            self._DistributedSellbotBoss__walkDoober(self.doobers[0], 0, turnPosA, dooberTrack, delayDeletes)
            self._DistributedSellbotBoss__walkDoober(self.doobers[1], 4, turnPosA, dooberTrack, delayDeletes)
            self._DistributedSellbotBoss__walkDoober(self.doobers[2], 8, turnPosA, dooberTrack, delayDeletes)
            self._DistributedSellbotBoss__walkDoober(self.doobers[3], 12, turnPosA, dooberTrack, delayDeletes)
            self._DistributedSellbotBoss__walkDoober(self.doobers[7], 2, turnPosB, dooberTrack, delayDeletes)
            self._DistributedSellbotBoss__walkDoober(self.doobers[6], 6, turnPosB, dooberTrack, delayDeletes)
            self._DistributedSellbotBoss__walkDoober(self.doobers[5], 10, turnPosB, dooberTrack, delayDeletes)
            self._DistributedSellbotBoss__walkDoober(self.doobers[4], 14, turnPosB, dooberTrack, delayDeletes)

        toonTrack = Parallel()
        self._DistributedSellbotBoss__toonsToPromotionPosition(self.toonsA, self.battleANode)
        self._DistributedSellbotBoss__toonsToPromotionPosition(self.toonsB, self.battleBNode)
        delay = 0

        for toonId in self.toonsA:
            self._DistributedSellbotBoss__walkToonToPromotion(toonId, delay, self.toonsEnterA, toonTrack, delayDeletes)
            delay += 1

        for toonId in self.toonsB:
            self._DistributedSellbotBoss__walkToonToPromotion(toonId, delay, self.toonsEnterB, toonTrack, delayDeletes)
            delay += 1

        toonTrack.append(Sequence(Wait(delay), self.closeDoors))
        self.rampA.request('extended')
        self.rampB.request('extended')
        self.rampC.request('retracted')
        self.clearChat()
        self.cagedToon.clearChat()

        promoteDoobers = TTLocalizer.BrutalBossCogPromoteDoobers
        doobersAway = TTLocalizer.BrutalBossCogDoobersAway
        welcomeToons = TTLocalizer.BrutalBossCogWelcomeToons
        promoteToons = TTLocalizer.BrutalBossCogPromoteToons
        discoverToons = TTLocalizer.BrutalBossCogDiscoverToons
        attackToons = TTLocalizer.BrutalBossCogAttackToons
        interruptBoss = TTLocalizer.BrutalCagedToonInterruptBoss
        rescueQuery = TTLocalizer.BrutalCagedToonRescueQuery

        bossAnimTrack = Sequence(
            ActorInterval(self, 'Ff_speech', startTime=2, duration=10, loop=1),
            ActorInterval(self, 'ltTurn2Wave', duration=2),
            ActorInterval(self, 'wave', duration=4, loop=1),
            ActorInterval(self, 'ltTurn2Wave', startTime=2, endTime=0),
            ActorInterval(self, 'Ff_speech', duration=7, loop=1))
        track.append(bossAnimTrack)

        dialogTrack = Track(
            (0, Parallel(
                camera.posHprInterval(8, Point3(-22, -100, 35), Point3(-10, -13, 0), blendType='easeInOut'),
                IndirectInterval(toonTrack, 0, 18))),
            (5.6, Func(self.setChatAbsolute, promoteDoobers, ChatGlobals.CFSpeech)),
            (9, IndirectInterval(dooberTrack, 0, 9)),
            (10, Sequence(
                Func(self.clearChat),
                Func(camera.setPosHpr, -23.1, 15.7, 17.2, -160, -2.4, 0))),
            (12, Func(self.setChatAbsolute, doobersAway, ChatGlobals.CFSpeech)),
            (16, Parallel(
                Func(self.clearChat),
                Func(camera.setPosHpr, -25, -99, 10, -14, 10, 0),
                IndirectInterval(dooberTrack, 14),
                IndirectInterval(toonTrack, 30))),
            (18, Func(self.setChatAbsolute, welcomeToons, ChatGlobals.CFSpeech)),
            (22, Func(self.setChatAbsolute, promoteToons, ChatGlobals.CFSpeech)),
            (22.2, Sequence(
                Func(self.cagedToon.nametag3d.setScale, 2),
                Func(self.cagedToon.setChatAbsolute, interruptBoss, ChatGlobals.CFSpeech),
                ActorInterval(self.cagedToon, 'wave'),
                Func(self.cagedToon.loop, 'neutral'))),
            (25, Sequence(
                Func(self.clearChat),
                Func(self.cagedToon.clearChat),
                Func(camera.setPosHpr, -12, -15, 27, -151, -15, 0),
                ActorInterval(self, 'Ff_lookRt'))),
            (27, Sequence(
                Func(self.cagedToon.setChatAbsolute, rescueQuery, ChatGlobals.CFSpeech),
                Func(camera.setPosHpr, -12, 48, 94, -26, 20, 0),
                ActorInterval(self.cagedToon, 'wave'),
                Func(self.cagedToon.loop, 'neutral'))),
            (31, Sequence(
                Func(camera.setPosHpr, -20, -35, 10, -88, 25, 0),
                Func(self.setChatAbsolute, discoverToons, ChatGlobals.CFSpeech),
                Func(self.cagedToon.nametag3d.setScale, 1),
                Func(self.cagedToon.clearChat),
                ActorInterval(self, 'turn2Fb'))),
            (34, Sequence(
                Func(self.clearChat),
                self.loseCogSuits(self.toonsA, self.battleANode, (0, 18, 5, -180, 0, 0)),
                self.loseCogSuits(self.toonsB, self.battleBNode, (0, 18, 5, -180, 0, 0)))),
            (37, Sequence(
                self.toonNormalEyes(self.involvedToons),
                Func(camera.setPosHpr, -23.4, -145.6, 44.0, -10.0, -12.5, 0),
                Func(self.loop, 'Fb_neutral'),
                Func(self.rampA.request, 'retract'),
                Func(self.rampB.request, 'retract'),
                Parallel(self.backupToonsToBattlePosition(self.toonsA, self.battleANode),
                         self.backupToonsToBattlePosition(self.toonsB, self.battleBNode),
                         Sequence(
                             Wait(2),
                             Func(self.setChatAbsolute, attackToons, ChatGlobals.CFSpeech))))))
        track.append(dialogTrack)

        return Sequence(Func(self.stickToonsToFloor), track, Func(self.unstickToons), name=self.uniqueName('Introduction'))

    def enterPrepareBattleThree(self):
        self.cleanupIntervals()
        self.controlToons()
        self.clearChat()
        self.cagedToon.clearChat()
        self.reparentTo(render)
        self.rampA.request('retract')
        self.rampB.request('retract')
        self.rampC.request('extend')
        self.setCageIndex(4)
        camera.reparentTo(render)
        camera.setPosHpr(self.cage, 0, -17, 3.3, 0, 0, 0)
        localAvatar.setCameraFov(ToontownGlobals.CogHQCameraFov)
        self.hide()
        self.acceptOnce('doneChatPage', self._DistributedSellbotBoss__onToBattleThree)
        self.cagedToon.setLocalPageChat(TTLocalizer.BrutalCagedToonPrepareBattleThree, 1)
        base.playMusic(self.betweenBattleMusic, looping=1, volume=0.9)

    def _DistributedSellbotBoss__talkAboutPromotion(self, speech):
        if self.prevCogSuitLevel < ToontownGlobals.MaxCogSuitLevel:
            deptIndex = CogDisguiseGlobals.dept2deptIndex(self.style.dept)
            cogLevels = base.localAvatar.getCogLevels()
            newCogSuitLevel = cogLevels[deptIndex]
            cogTypes = base.localAvatar.getCogTypes()
            maxCogSuitLevel = (SuitDNA.levelsPerSuit-1) + cogTypes[deptIndex]
            if self.prevCogSuitLevel != maxCogSuitLevel:
                speech += TTLocalizer.BrutalCagedToonLevelPromotion
            if newCogSuitLevel == maxCogSuitLevel:
                if newCogSuitLevel != ToontownGlobals.MaxCogSuitLevel:
                    suitIndex = (SuitDNA.suitsPerDept*deptIndex) + cogTypes[deptIndex]
                    cogTypeStr = SuitDNA.suitHeadTypes[suitIndex]
                    cogName = SuitBattleGlobals.SuitAttributes[cogTypeStr]['name']
                    speech += TTLocalizer.CagedToonSuitPromotion % cogName
        else:
            speech += TTLocalizer.CagedToonMaxed % (ToontownGlobals.MaxCogSuitLevel + 1)
        return speech

    def _DistributedSellbotBoss__makeCageOpenMovie(self):
        speech = TTLocalizer.BrutalCagedToonThankYou
        speech = self._DistributedSellbotBoss__talkAboutPromotion(speech)
        name = self.uniqueName('CageOpen')
        seq = Sequence(
            Func(self.cage.setPos, self.cagePos[4]),
            Func(self.cageDoor.setHpr, VBase3(0, 0, 0)),
            Func(self.cagedToon.setPos, Point3(0, -2, 0)),
            Parallel(
                self.cage.posInterval(0.5, self.cagePos[5], blendType='easeOut'),
                SoundInterval(self.cageLowerSfx, duration=0.5)),
            Parallel(
                self.cageDoor.hprInterval(0.5, VBase3(0, 90, 0), blendType='easeOut'),
                Sequence(SoundInterval(self.cageDoorSfx), duration=0)),
            Wait(0.2),
            Func(self.cagedToon.loop, 'walk'),
            self.cagedToon.posInterval(0.8, Point3(0, -6, 0)),
            Func(self.cagedToon.setChatAbsolute, TTLocalizer.CagedToonYippee, ChatGlobals.CFSpeech),
            ActorInterval(self.cagedToon, 'jump'),
            Func(self.cagedToon.loop, 'neutral'),
            Func(self.cagedToon.headsUp, localAvatar),
            Func(self.cagedToon.setLocalPageChat, speech, 0),
            Func(camera.reparentTo, localAvatar),
            Func(camera.setPos, 0, -9, 9),
            Func(camera.lookAt, self.cagedToon, Point3(0, 0, 2)), name=name)
        return seq