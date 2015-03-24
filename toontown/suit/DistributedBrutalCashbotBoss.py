from pandac.PandaModules import Point3, VBase3

from toontown.suit.DistributedCashbotBoss import DistributedCashbotBoss
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
from toontown.chat import ChatGlobals
from toontown.distributed.DelayDelete import DelayDelete

from direct.interval.IntervalGlobal import *


class DistributedBrutalCashbotBoss(DistributedCashbotBoss):
    notify = directNotify.newCategory('DistributedBrutalCashbotBoss')

    ANIM_PLAYRATE = 1.5

    def __init__(self, cr):
        DistributedCashbotBoss.__init__(self, cr)

        self.bossMaxDamage = ToontownGlobals.BrutalCashbotBossMaxDamage

    def announceGenerate(self):
        DistributedCashbotBoss.announceGenerate(self)

        self.setName(TTLocalizer.BrutalCashbotBossName)
        base.localAvatar.setCanUseUnites(False)

    def disable(self):
        DistributedCashbotBoss.disable(self)

        base.localAvatar.setCanUseUnites(True)

    def makeBossFleeMovie(self):
        hadEnough = TTLocalizer.BrutalCashbotBossHadEnough
        outtaHere = TTLocalizer.BrutalCashbotBossOuttaHere
        loco = loader.loadModel('phase_10/models/cogHQ/CashBotLocomotive')
        car1 = loader.loadModel('phase_10/models/cogHQ/CashBotBoxCar')
        car2 = loader.loadModel('phase_10/models/cogHQ/CashBotTankCar')
        trainPassingSfx = base.loadSfx('phase_10/audio/sfx/CBHQ_TRAIN_pass.ogg')
        boomSfx = loader.loadSfx('phase_3.5/audio/sfx/ENC_cogfall_apart.ogg')
        rollThroughDoor = self.rollBossToPoint(fromPos=Point3(120, -280, 0), fromHpr=None, toPos=Point3(120, -250, 0), toHpr=None, reverse=0)
        rollTrack = Sequence(Func(self.getGeomNode().setH, 180), rollThroughDoor[0], Func(self.getGeomNode().setH, 0))
        g = 80.0 / 300.0
        trainTrack = Track(
            (0 * g, loco.posInterval(0.5, Point3(0, -242, 0), startPos=Point3(150, -242, 0))),
            (1 * g, car2.posInterval(0.5, Point3(0, -242, 0), startPos=Point3(150, -242, 0))),
            (2 * g, car1.posInterval(0.5, Point3(0, -242, 0), startPos=Point3(150, -242, 0))),
            (3 * g, car2.posInterval(0.5, Point3(0, -242, 0), startPos=Point3(150, -242, 0))),
            (4 * g, car1.posInterval(0.5, Point3(0, -242, 0), startPos=Point3(150, -242, 0))),
            (5 * g, car2.posInterval(0.5, Point3(0, -242, 0), startPos=Point3(150, -242, 0))),
            (6 * g, car1.posInterval(0.5, Point3(0, -242, 0), startPos=Point3(150, -242, 0))),
            (7 * g, car2.posInterval(0.5, Point3(0, -242, 0), startPos=Point3(150, -242, 0))),
            (8 * g, car1.posInterval(0.5, Point3(0, -242, 0), startPos=Point3(150, -242, 0))),
            (9 * g, car2.posInterval(0.5, Point3(0, -242, 0), startPos=Point3(150, -242, 0))),
            (10 * g, car1.posInterval(0.5, Point3(0, -242, 0), startPos=Point3(150, -242, 0))),
            (11 * g, car2.posInterval(0.5, Point3(0, -242, 0), startPos=Point3(150, -242, 0))),
            (12 * g, car1.posInterval(0.5, Point3(0, -242, 0), startPos=Point3(150, -242, 0))),
            (13 * g, car2.posInterval(0.5, Point3(0, -242, 0), startPos=Point3(150, -242, 0))),
            (14 * g, car1.posInterval(0.5, Point3(0, -242, 0), startPos=Point3(150, -242, 0))))
        bossTrack = Track(
            (0.0, Sequence(
                Func(base.camera.reparentTo, render),
                Func(base.camera.setPosHpr, 105, -280, 20, -158, -3, 0),
                Func(self.reparentTo, render),
                Func(self.show),
                Func(self.clearChat),
                Func(self.setPosHpr, *ToontownGlobals.CashbotBossBattleThreePosHpr),
                Func(self.reverseHead),
                ActorInterval(self, 'Fb_firstHit'),
                ActorInterval(self, 'Fb_down2Up'))),
            (1.0, Func(self.setChatAbsolute, hadEnough, ChatGlobals.CFSpeech)),
            (5.5, Parallel(
                Func(base.camera.setPosHpr, 100, -315, 16, -20, 0, 0),
                Func(self.hideBattleThreeObjects),
                Func(self.forwardHead),
                Func(self.loop, 'Ff_neutral'),
                rollTrack,
                self.door3.posInterval(2.5, Point3(0, 0, 25), startPos=Point3(0, 0, 18)))),
            (5.5, Func(self.setChatAbsolute, outtaHere, ChatGlobals.CFSpeech)),
            (5.5, SoundInterval(trainPassingSfx)),
            (8.1, Func(self.clearChat)),
            (9.4, Sequence(
                Func(loco.reparentTo, render),
                Func(car1.reparentTo, render),
                Func(car2.reparentTo, render),
                trainTrack,
                Func(loco.detachNode),
                Func(car1.detachNode),
                Func(car2.detachNode),
                Wait(2))),
            (9.5, SoundInterval(boomSfx)),
            (9.5, Sequence(
                self.posInterval(0.4, Point3(0, -250, 0)),
                Func(self.stash))))
        return bossTrack

    def makeIntroductionMovie(self, delayDeletes):
        for toonId in self.involvedToons:
            toon = self.cr.doId2do.get(toonId)
            if toon:
                delayDeletes.append(DelayDelete(toon, 'CashbotBoss.makeIntroductionMovie'))

        rtTrack = Sequence()
        startPos = Point3(ToontownGlobals.CashbotBossOffstagePosHpr[0], ToontownGlobals.CashbotBossOffstagePosHpr[1], ToontownGlobals.CashbotBossOffstagePosHpr[2])
        battlePos = Point3(ToontownGlobals.CashbotBossBattleOnePosHpr[0], ToontownGlobals.CashbotBossBattleOnePosHpr[1], ToontownGlobals.CashbotBossBattleOnePosHpr[2])
        battleHpr = VBase3(ToontownGlobals.CashbotBossBattleOnePosHpr[3], ToontownGlobals.CashbotBossBattleOnePosHpr[4], ToontownGlobals.CashbotBossBattleOnePosHpr[5])
        bossTrack = Sequence()
        bossTrack.append(Func(self.reparentTo, render))
        bossTrack.append(Func(self.getGeomNode().setH, 180))
        bossTrack.append(Func(self.pelvis.setHpr, self.pelvisForwardHpr))
        bossTrack.append(Func(self.loop, 'Ff_neutral'))
        track, hpr = self.rollBossToPoint(startPos, None, battlePos, None, 0)
        bossTrack.append(track)
        track, hpr = self.rollBossToPoint(battlePos, hpr, battlePos, battleHpr, 0)
        bossTrack.append(track)
        bossTrack.append(Func(self.getGeomNode().setH, 0))
        bossTrack.append(Func(self.pelvis.setHpr, self.pelvisReversedHpr))
        goonTrack = self._DistributedCashbotBoss__makeGoonMovieForIntro()
        attackToons = TTLocalizer.CashbotBossCogAttack
        rToon = self.resistanceToon
        rToon.setPosHpr(*ToontownGlobals.CashbotRTBattleOneStartPosHpr)
        track = Sequence(
            Func(base.camera.setPosHpr, 82, -219, 5, 267, 0, 0),
            Func(rToon.setChatAbsolute, TTLocalizer.BrutalResistanceToonWelcome, ChatGlobals.CFSpeech),
            Wait(3),
            Sequence(goonTrack, duration=0),
            Parallel(
                base.camera.posHprInterval(4, Point3(108, -244, 4), VBase3(211.5, 0, 0)),
                Sequence(
                    Func(rToon.suit.setPlayRate, 1.4, 'walk'),
                    Func(rToon.suit.loop, 'walk'),
                    Parallel(
                        rToon.hprInterval(1, VBase3(180, 0, 0)),
                        rToon.posInterval(3, VBase3(120, -255, 0)),
                        Sequence(
                            Wait(2),
                            Func(rToon.clearChat))),
                        Func(rToon.suit.loop, 'neutral'),
                        self.door2.posInterval(3, VBase3(0, 0, 30)))),
                        Func(rToon.setHpr, 0, 0, 0),
                        Func(rToon.setChatAbsolute, TTLocalizer.ResistanceToonTooLate, ChatGlobals.CFSpeech),
                        Func(base.camera.reparentTo, render),
                        Func(base.camera.setPosHpr, 61.1, -228.8, 10.2, -90, 0, 0),
                        self.door1.posInterval(2, VBase3(0, 0, 30)),
                        Parallel(
                            bossTrack,
                            Sequence(
                                Wait(3),
                                Func(rToon.clearChat),
                                self.door1.posInterval(3, VBase3(0, 0, 0)))),
                            Func(self.setChatAbsolute, TTLocalizer.CashbotBossDiscoverToons1, ChatGlobals.CFSpeech),
                            base.camera.posHprInterval(1.5, Point3(93.3, -230, 0.7), VBase3(-92.9, 39.7, 8.3)),
                            Func(self.setChatAbsolute, TTLocalizer.BrutalCashbotBossDiscoverToons2, ChatGlobals.CFSpeech),
                            Wait(4),
                            Func(self.clearChat),
                            self.loseCogSuits(self.toonsA + self.toonsB, render, (113, -228, 10, 90, 0, 0)),
                            Wait(1),
                            Func(rToon.setHpr, 0, 0, 0),
                            self.loseCogSuits([rToon], render, (133, -243, 5, 143, 0, 0), True),
                            Func(rToon.setChatAbsolute, TTLocalizer.BrutalResistanceToonKeepHimBusy, ChatGlobals.CFSpeech),
                            Wait(1),
                            Func(self._DistributedCashbotBoss__showResistanceToon, False),
                            Sequence(
                                Func(rToon.animFSM.request, 'run'),
                                rToon.hprInterval(1, VBase3(180, 0, 0)),
                                Parallel(
                                    Sequence(
                                        rToon.posInterval(1.5, VBase3(109, -294, 0)),
                                        Parallel(Func(rToon.animFSM.request, 'jump')),
                                        rToon.posInterval(1.5, VBase3(93.935, -341.065, 2))),
                                    self.door2.posInterval(3, VBase3(0, 0, 0))),
                                    Func(rToon.animFSM.request, 'neutral')),
                                    self.toonNormalEyes(self.involvedToons),
                                    self.toonNormalEyes([self.resistanceToon], True),
                                    Func(rToon.clearChat),
                                    Func(base.camera.setPosHpr, 93.3, -230, 0.7, -92.9, 39.7, 8.3),
                                    Func(self.setChatAbsolute, attackToons, ChatGlobals.CFSpeech),
                                    Wait(2),
                                    Func(self.clearChat))
        return Sequence(Func(base.camera.reparentTo, render), track)


    def makePrepareBattleThreeMovie(self, delayDeletes):
        for toonId in self.involvedToons:
            toon = self.cr.doId2do.get(toonId)
            if toon:
                delayDeletes.append(DelayDelete(toon, 'CashbotBoss.makePrepareBattleThreeMovie'))

        startPos = Point3(ToontownGlobals.CashbotBossBattleOnePosHpr[0], ToontownGlobals.CashbotBossBattleOnePosHpr[1], ToontownGlobals.CashbotBossBattleOnePosHpr[2])
        battlePos = Point3(ToontownGlobals.CashbotBossBattleThreePosHpr[0], ToontownGlobals.CashbotBossBattleThreePosHpr[1], ToontownGlobals.CashbotBossBattleThreePosHpr[2])
        startHpr = Point3(ToontownGlobals.CashbotBossBattleOnePosHpr[3], ToontownGlobals.CashbotBossBattleOnePosHpr[4], ToontownGlobals.CashbotBossBattleOnePosHpr[5])
        battleHpr = VBase3(ToontownGlobals.CashbotBossBattleThreePosHpr[3], ToontownGlobals.CashbotBossBattleThreePosHpr[4], ToontownGlobals.CashbotBossBattleThreePosHpr[5])
        finalHpr = VBase3(135, 0, 0)
        bossTrack = Sequence()
        bossTrack.append(Func(self.reparentTo, render))
        bossTrack.append(Func(self.getGeomNode().setH, 180))
        bossTrack.append(Func(self.pelvis.setHpr, self.pelvisForwardHpr))
        bossTrack.append(Func(self.loop, 'Ff_neutral'))
        track, hpr = self.rollBossToPoint(startPos, startHpr, startPos, battleHpr, 0)
        bossTrack.append(track)
        track, hpr = self.rollBossToPoint(startPos, None, battlePos, None, 0)
        bossTrack.append(track)
        track, hpr = self.rollBossToPoint(battlePos, battleHpr, battlePos, finalHpr, 0)
        bossTrack.append(track)
        rToon = self.resistanceToon
        rToon.setPosHpr(93.935, -341.065, 0, -45, 0, 0)
        goon = self.fakeGoons[0]
        crane = self.cranes[0]
        track = Sequence(
            Func(self._DistributedCashbotBoss__hideToons),
            Func(crane.request, 'Movie'),
            Func(crane.accomodateToon, rToon),
            Func(goon.request, 'Stunned'),
            Func(goon.setPosHpr, 104, -316, 0, 165, 0, 0),
            Parallel(
                self.door2.posInterval(4.5, VBase3(0, 0, 30)),
                self.door3.posInterval(4.5, VBase3(0, 0, 30)),
                bossTrack),
            Func(rToon.loop, 'leverNeutral'),
            Func(base.camera.reparentTo, self.geom),
            Func(base.camera.setPosHpr, 105, -326, 5, 136.3, 0, 0),
            Func(rToon.setChatAbsolute, TTLocalizer.BrutalResistanceToonWatchThis, ChatGlobals.CFSpeech),
            Wait(2),
            Func(rToon.clearChat),
            Func(base.camera.setPosHpr, 105, -326, 20, -45.3, 11, 0),
            Func(self.setChatAbsolute, TTLocalizer.BrutalCashbotBossGetAwayFromThat, ChatGlobals.CFSpeech),
            Wait(2),
            Func(self.clearChat),
            base.camera.posHprInterval(1.5, Point3(105, -326, 5), Point3(136.3, 0, 0), blendType='easeInOut'),
            Func(rToon.setChatAbsolute, TTLocalizer.ResistanceToonCraneInstructions1, ChatGlobals.CFSpeech),
            Wait(4),
            Func(rToon.setChatAbsolute, TTLocalizer.ResistanceToonCraneInstructions2, ChatGlobals.CFSpeech),
            Wait(4),
            Func(rToon.setChatAbsolute, TTLocalizer.BrutalResistanceToonCraneInstructions3, ChatGlobals.CFSpeech),
            Wait(4),
            Func(rToon.setChatAbsolute, TTLocalizer.BrutalResistanceToonCraneInstructions4, ChatGlobals.CFSpeech),
            Wait(4),
            Func(rToon.clearChat),
            Func(base.camera.setPosHpr, 102, -323.6, 0.9, -10.6, 14, 0),
            Func(goon.request, 'Recovery'),
            Wait(2),
            Func(base.camera.setPosHpr, 95.4, -332.6, 4.2, 167.1, -13.2, 0),
            Func(rToon.setChatAbsolute, TTLocalizer.ResistanceToonGetaway, ChatGlobals.CFSpeech),
            Func(rToon.animFSM.request, 'jump'),
            Wait(1.8),
            Func(rToon.clearChat),
            Func(base.camera.setPosHpr, 109.1, -300.7, 13.9, -15.6, -13.6, 0),
            Func(rToon.animFSM.request, 'run'),
            Func(goon.request, 'Walk'),
            Parallel(
                self.door3.posInterval(3, VBase3(0, 0, 0)),
                rToon.posHprInterval(3, Point3(136, -212.9, 0), VBase3(-14, 0, 0), startPos=Point3(110.8, -292.7, 0), startHpr=VBase3(-14, 0, 0)),
                goon.posHprInterval(3, Point3(125.2, -243.5, 0), VBase3(-14, 0, 0), startPos=Point3(104.8, -309.5, 0), startHpr=VBase3(-14, 0, 0))),
            Func(self._DistributedCashbotBoss__hideFakeGoons),
            Func(crane.request, 'Free'),
            Func(self.getGeomNode().setH, 0),
            self.moveToonsToBattleThreePos(self.involvedToons),
            Func(self._DistributedCashbotBoss__showToons))
        return Sequence(Func(base.camera.reparentTo, self), Func(base.camera.setPosHpr, 0, -27, 25, 0, -18, 0), track)
