#Embedded file name: toontown.election.DistributedElectionEvent
from pandac.PandaModules import *
from otp.nametag.NametagConstants import *
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
from direct.distributed.DistributedObject import DistributedObject
from direct.fsm.FSM import FSM
from direct.actor import Actor
from direct.task import Task
from toontown.toon import NPCToons
from toontown.electionsuit import DistributedSuitBase, SuitDNA
from toontown.toonbase import ToontownGlobals
from toontown.battle import BattleProps
from otp.margins.WhisperPopup import *
import ElectionGlobals
from direct.directnotify import DirectNotifyGlobal
from random import choice
from otp.speedchat import SpeedChatGlobals

class DistributedElectionEvent(DistributedObject, FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedElectionEvent')

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        FSM.__init__(self, 'ElectionFSM')
        self.cr.election = self
        self.interactiveOn = False
        self.showFloor = NodePath('ShowFloor')
        self.showFloor.setPos(80, 0, 4)
        stage = loader.loadModel('phase_4/models/events/election_stage')
        stage.reparentTo(self.showFloor)
        stage.setHpr(270, 0, 0)
        stage.setScale(2.0, 1.8, 1.5)
        podium = loader.loadModel('phase_4/models/events/election_stagePodium')
        podium.reparentTo(self.showFloor)
        podium.setPosHpr(-6, 0, 3, 270, -2, 5)
        podium.setScale(0.65)
        self.counterLeft = Actor.Actor('phase_4/models/events/election_counterLeft-mod', {'body': 'phase_4/models/events/election_counterLeft-countSeq'})
        self.counterLeft.reparentTo(self.showFloor)
        self.counterLeft.setPosHpr(13.5, 10, 2.95, 270, 0, 0)
        self.counterLeft.setScale(2.0)
        self.counterRight = Actor.Actor('phase_4/models/events/election_counterRight-mod', {'body': 'phase_4/models/events/election_counterRight-countSeq'})
        self.counterRight.reparentTo(self.showFloor)
        self.counterRight.setPosHpr(13.5, -10, 3.25, 270, 0, 0)
        self.counterRight.setScale(2.0)
        rope = loader.loadModel('phase_4/models/events/election_rope')
        rope.reparentTo(self.showFloor)
        rope.setPosHpr(-34, 18, 0.46, 270, 0, 0)
        rope.setScale(2, 2, 2)
        rc = CollisionSphere(8.2, 15.5, 2.0, 13.5)
        rc2 = CollisionBox(Point3(8.88, 28.76, 0.0), 4.44, 6.38, 9.0)
        ropeCollision = rope.attachNewNode(CollisionNode('collision'))
        ropeCollision.node().addSolid(rc)
        ropeCollision.node().addSolid(rc2)
        self.flippyStand = Actor.Actor('phase_4/models/events/election_flippyStand-mod', {'idle': 'phase_4/models/events/election_flippyStand-idle'})
        self.flippyStand.reparentTo(self.showFloor)
        self.flippyStand.setPosHprScale(-43.6, -24.5, 0.01, 200, 0, 0, 0.55, 0.55, 0.55)
        self.flippyStand.exposeJoint(None, 'modelRoot', 'LInnerShoulder')
        flippyTable = self.flippyStand.find('**/LInnerShoulder')
        self.flippyStand.exposeJoint(None, 'modelRoot', 'Box_Joint')
        wheelbarrowJoint = self.flippyStand.find('**/Box_Joint').attachNewNode('Pie_Joint')
        wheelbarrow = self.flippyStand.find('**/Box')
        wheelbarrow.setPosHprScale(-2.39, 0.0, 1.77, 0.0, 0.0, 6.0, 1.14, 1.54, 0.93)
        self.slappyStand = Actor.Actor('phase_4/models/events/election_slappyStand-mod', {'idle': 'phase_4/models/events/election_slappyStand-idle',
         'watch-idle': 'phase_4/models/events/election_slappyStand-watch-idle',
         'sad': 'phase_4/models/events/election_slappyStand-reaction'})
        self.slappyStand.reparentTo(self.showFloor)
        self.slappyStand.setPosHprScale(-62.45, 14.39, 0.01, 325, 0, 0, 0.55, 0.55, 0.55)
        pie = loader.loadModel('phase_3.5/models/props/tart')
        pieS = pie.copyTo(flippyTable)
        pieS.setPosHprScale(-2.61, -0.37, -1.99, 355.6, 90.0, 4.09, 1.6, 1.6, 1.6)
        for pieSettings in ElectionGlobals.FlippyWheelbarrowPies:
            pieModel = pie.copyTo(wheelbarrowJoint)
            pieModel.setPosHprScale(*pieSettings)

        wheelbarrowJoint.setPosHprScale(3.94, 0.0, 1.06, 270.0, 344.74, 0.0, 1.43, 1.12, 1.0)
        self.restockSfx = loader.loadSfx('phase_9/audio/sfx/CHQ_SOS_pies_restock.ogg')
        self.splashSfx = loader.loadSfx('phase_9/audio/sfx/CHQ_FACT_paint_splash.ogg')
        cs = CollisionBox(Point3(7, 0, 0), 12, 5, 18)
        self.pieCollision = self.flippyStand.attachNewNode(CollisionNode('wheelbarrow_collision'))
        self.pieCollision.node().addSolid(cs)
        self.accept('enter' + self.pieCollision.node().getName(), self.handleWheelbarrowCollisionSphereEnter)
        csSlappy = CollisionBox(Point3(-4.2, 0, 0), 9.5, 5.5, 18)
        self.goopCollision = self.slappyStand.attachNewNode(CollisionNode('goop_collision'))
        self.goopCollision.node().addSolid(csSlappy)
        if not config.GetBool('want-doomsday', False):
            self.accept('enter' + self.goopCollision.node().getName(), self.handleSlappyCollisionSphereEnter)
        self.alec = NPCToons.createLocalNPC(2022)
        self.slappy = NPCToons.createLocalNPC(2021)
        self.flippy = NPCToons.createLocalNPC(2001)
        if config.GetBool('want-doomsday', False):
            self.characters = [self.alec, self.slappy, self.flippy]
        if not config.GetBool('want-doomsday', False):
            self.startInteractiveFlippy()
        self.flippyStand.loop('idle')
        self.slappyStand.loop('idle')
        self.alecNode = None
        self.surlee = NPCToons.createLocalNPC(20191)
        self.surlee.useLOD(1000)
        self.surlee.find('**/250').removeNode()
        self.surlee.find('**/500').removeNode()
        surleeLegs = self.surlee.find('**/legs')
        surleeLegs.setScale(1, 1, 1.5)
        surleeLegs.setZ(-0.26)
        self.surlee.find('**/__Actor_torso').setZ(1.1)
        self.surlee.find('**/torso-top').setPosHprScale(0.0, 0.0, -0.45, 0.0, 0.0, 0.0, 1.0, 0.98, 1.96)
        self.surlee.find('**/__Actor_head').setZ(0.7)
        self.surlee.find('**/neck').setZ(0.7)
        self.surlee.find('**/sleeves').setZ(0.7)
        self.surlee.find('**/arms').setZ(0.7)
        self.surlee.find('**/hands').setZ(0.7)
        self.surlee.setPos(-22, 7, 0)
        self.surlee.setH(110)
        rHand = self.surlee.find('**/def_joint_right_hold')
        clipBoard = loader.loadModel('phase_4/models/props/tt_m_prp_acs_clipboard')
        placeholder = rHand.attachNewNode('ClipBoard')
        clipBoard.instanceTo(placeholder)
        placeholder.setH(180)
        placeholder.setScale(render, 1.0)
        placeholder.setPos(0.5, 0.6, -0.1)
        placeholder.setScale(1.3)
        self.surleeR = NPCToons.createLocalNPC(2019)
        self.surleeR.useLOD(1000)
        self.surleeR.setPos(-22, 7, 0)
        self.surleeR.setH(110)
        self.surleeR.head = self.surleeR.find('**/__Actor_head')
        self.surleeR.initializeBodyCollisions('toon')
        if config.GetBool('want-doomsday', False):
            self.prepostera = NPCToons.createLocalNPC(20201)
            self.prepostera.useLOD(1000)
            self.prepostera.find('**/250').removeNode()
            self.prepostera.find('**/500').removeNode()
            preposteraLegs = self.prepostera.find('**/legs')
            preposteraLegs.setScale(1, 1, 0.5)
            self.prepostera.find('**/__Actor_torso').setZ(-0.9)
            self.prepostera.find('**/torso-top').setPosHprScale(0.0, 0.0, 0.2, 0.0, 0.0, 0.0, 1.0, 0.98, 0.5)
            self.prepostera.find('**/__Actor_head').setZ(-0.7)
            self.prepostera.find('**/neck').setZ(-0.7)
            self.prepostera.find('**/sleeves').setZ(-0.7)
            preposteraArms = self.prepostera.find('**/arms')
            preposteraArms.setZ(-0.4)
            preposteraArms.setScale(1, 1, 0.8)
            preposteraHands = self.prepostera.find('**/hands')
            preposteraHands.setZ(-0.4)
            preposteraHands.setScale(1, 1, 0.8)
            self.prepostera.setPos(-70, 10, 0.0)
            self.prepostera.setH(-50)
            self.prepostera.initializeBodyCollisions('toon')
            rHand = self.prepostera.find('**/def_joint_right_hold')
            clipBoard = loader.loadModel('phase_4/models/props/tt_m_prp_acs_clipboard')
            placeholder = rHand.attachNewNode('ClipBoard')
            clipBoard.instanceTo(placeholder)
            placeholder.setH(180)
            placeholder.setScale(render, 1.0)
            placeholder.setPos(0, -0.3, 0.3)
            self.dimm = NPCToons.createLocalNPC(2018)
            self.dimm.useLOD(1000)
            self.dimm.find('**/250').removeNode()
            self.dimm.find('**/500').removeNode()
            self.dimm.setPos(-72.36, 10.46, 0.0)
            self.dimm.setH(-50)
            self.dimm.initializeBodyCollisions('toon')
            rHand1 = self.dimm.find('**/def_joint_right_hold')
            sillyReader = loader.loadModel('phase_4/models/props/tt_m_prp_acs_sillyReader')
            placeholder1 = rHand1.attachNewNode('SillyReader')
            sillyReader.instanceTo(placeholder1)
            placeholder1.setH(180)
            placeholder1.setScale(render, 1.0)
            placeholder1.setPos(0, 0, 0.1)
            self.surlee.reparentTo(self.showFloor)
            self.surleeR.reparentTo(self.showFloor)
            self.prepostera.reparentTo(self.showFloor)
            self.dimm.reparentTo(self.showFloor)
            self.surlee.hide()
            self.surleeR.hide()
            self.prepostera.addActive()
            self.prepostera.startBlink()
            self.prepostera.loop('scientistWork')
            self.dimm.addActive()
            self.dimm.startBlink()
            self.dimm.loop('scientistWork')
        self.suit = DistributedSuitBase.DistributedSuitBase(cr)
        suitDNA = SuitDNA.SuitDNA()
        suitDNA.newSuit('ym')
        self.suit.setDNA(suitDNA)
        self.suit.setDisplayName('Yesman\nBossbot\nLevel 3')
        self.suit.setPickable(0)
        phasePath = 'phase_3.5/audio/dial/'
        self.speechMurmurSfx = loader.loadSfx(phasePath + 'COG_VO_murmur.ogg')
        self.speechStatementSfx = loader.loadSfx(phasePath + 'COG_VO_statement.ogg')
        self.speechQuestionSfx = loader.loadSfx(phasePath + 'COG_VO_question.ogg')
        self.speechGruntSfx = loader.loadSfx(phasePath + 'COG_VO_grunt.ogg')
        self.finishedPreShow = False
        self.finishedBegin = False
        self.finishedAlecSpeech = False
        self.finishedCogLanding = False
        self.finishedInvasion = False
        self.finishedInvasionEnding = False

    def enterOff(self, offset):
        base.cr.parentMgr.unregisterParent(ToontownGlobals.SPSlappysBalloon)
        self.showFloor.reparentTo(hidden)

    def exitOff(self):
        self.showFloor.reparentTo(render)

    def __cleanupNPCs(self):
        if config.GetBool('want-doomsday', False):
            npcs = [self.flippy,
             self.slappy,
             self.alec,
             self.surlee,
             self.surleeR,
             self.prepostera,
             self.dimm,
             self.suit]
        if not config.GetBool('want-doomsday', False):
            npcs = [self.flippy,
             self.slappy,
             self.alec,
             self.surlee,
             self.surleeR,
             self.suit]
        for npc in npcs:
            if npc:
                npc.removeActive()

    def delete(self):
        self.demand('Off', 0.0)
        self.ignore('entercnode')
        self.showFloor.removeNode()
        self.stopInteractiveFlippy()
        self.ignore('enter' + self.pieCollision.node().getName())
        self.ignore('enter' + self.goopCollision.node().getName())
        self.__cleanupNPCs()
        DistributedObject.delete(self)

    def enterIdle(self, offset):
        if config.GetBool('want-doomsday', False):
            self.surlee.show()
            self.surlee.addActive()
            self.surlee.startBlink()
            self.surlee.loop('scientistEmcee')
            self.surleeIntroInterval = Sequence(Wait(10), Func(self.surlee.setChatAbsolute, "Oh, uh, Hello! I suppose it's election time already?", CFSpeech | CFTimeout), Wait(5), Func(self.surlee.setChatAbsolute, "We're just minutes away from the most important event in the history of our town.", CFSpeech | CFTimeout), Wait(8), Func(self.surlee.setChatAbsolute, 'Alec Tinn is inside Toon Hall right now with the two candidates preparing for the announcement.', CFSpeech | CFTimeout), Wait(8), Func(self.surlee.setChatAbsolute, "When the clock strikes two we'll see them march through those doors and onto the stage. Are you toons ready?", CFSpeech | CFTimeout), Wait(8), Func(self.surlee.setChatAbsolute, "I must say, surprisingly, the silliness around here couldn't be higher at this time.", CFSpeech | CFTimeout), Wait(8), Func(self.surlee.setChatAbsolute, 'My fellow scientists of silliness, Professor Prepostera and Doctor Dimm, are over there tracking the amount of silliness being taken in from the campaign stands.', CFSpeech | CFTimeout), Wait(8), Func(self.surlee.setChatAbsolute, 'At least, I think they are. You never know with those goofs.', CFSpeech | CFTimeout), Wait(8), Func(self.surlee.setChatAbsolute, "I hope you haven't been standing here long, because I'm going to have to start repeating myself soon.", CFSpeech | CFTimeout))
            self.surleeIntroInterval.loop()
            self.surleeIntroInterval.setT(offset)
        self.counterLeft.pose('body', 0)
        self.counterRight.pose('body', 0)

    def exitIdle(self):
        if config.GetBool('want-doomsday', False):
            self.surleeIntroInterval.finish()

    def startInteractiveFlippy(self):
        self.flippy.reparentTo(self.showFloor)
        self.flippy.setPosHpr(-40.6, -18.5, 0.01, 20, 0, 0)
        self.flippy.initializeBodyCollisions('toon')
        self.interactiveOn = True
        self.flippyPhrase = None
        self.accept(SpeedChatGlobals.SCStaticTextMsgEvent, self.phraseSaidToFlippy)

    def stopInteractiveFlippy(self):
        self.ignore(SpeedChatGlobals.SCStaticTextMsgEvent)
        self.interactiveOn = False

    def phraseSaidToFlippy(self, phraseId):
        if self.flippy.nametag.getChat() != '':
            return
        if Vec3(base.localAvatar.getPos(self.flippy)).length() > 10:
            return
        for phraseIdList in ElectionGlobals.FlippyPhraseIds:
            if phraseId in phraseIdList:
                self.sendUpdate('phraseSaidToFlippy', [phraseId])
                break

    def flippySpeech(self, avId, phraseId):
        av = self.cr.doId2do.get(avId)
        if not av:
            self.notify.warning('Received unknown avId in flippySpeech from the AI.')
            return
        if not self.interactiveOn:
            self.notify.warning('Received flippySpeech from AI while Interactive Flippy is disabled on our client.')
            return
        if self.flippy.nametag.getChat() != '':
            return
        if phraseId == 1:
            taskMgr.doMethodLater(ElectionGlobals.FlippyDelayResponse, self.flippy.setChatAbsolute, 'interactive-flippy-chat-task', extraArgs=[choice(ElectionGlobals.FlippyGibPies).replace('__NAME__', av.getName()), CFSpeech | CFTimeout])
            return
        if len(ElectionGlobals.FlippyPhraseIds) != len(ElectionGlobals.FlippyPhrases):
            raise Exception('There is a mismatch in the number of phraseIds and the number of phrases for Flippy Interactive!')
            return
        for index, phraseIdList in enumerate(ElectionGlobals.FlippyPhraseIds):
            for pid in phraseIdList:
                if pid == phraseId:
                    taskMgr.doMethodLater(ElectionGlobals.FlippyDelayResponse, self.flippy.setChatAbsolute, 'interactive-flippy-chat-task', extraArgs=[ElectionGlobals.FlippyPhrases[index].replace('__NAME__', av.getName()), CFSpeech | CFTimeout])
                    return

    def handleWheelbarrowCollisionSphereEnter(self, collEntry):
        if base.localAvatar.numPies >= 0 and base.localAvatar.numPies < 20:
            self.sendUpdate('wheelbarrowAvatarEnter', [])
            self.restockSfx.play()

    def handleSlappyCollisionSphereEnter(self, collEntry):
        if base.localAvatar.savedCheesyEffect != 15:
            self.sendUpdate('slappyAvatarEnter', [])
            self.splashSfx.play()

    def enterEvent(self, offset):
        base.cr.playGame.hood.loader.music.stop()

    def catchUp(self):
        if self.finishedPreShow:
            self.cameras = []
            for cameraId in base.cr.cameraManager.cameraIds:
                if cameraId in base.cr.doId2do:
                    self.cameras.append(base.cr.doId2do[cameraId])

            self.surlee.hide()
            self.surlee.removeActive()
            self.surleeR.show()
            self.surleeR.addActive()
            self.surleeR.startBlink()
            self.surleeR.setPosHpr(-32, -15, 0, -40, 0, 0)
            base.cr.cameraManager.tv.show()
            base.cr.cameraManager.tv.setPos(87.85, -0.25, 21.0)
            base.cr.cameraManager.tvIdle.loop()
        if self.finishedBegin:
            for character in self.characters:
                character.reparentTo(self.showFloor)
                character.useLOD(1000)
                character.addActive()
                character.startBlink()
                character.initializeBodyCollisions('toon')
                character.head = character.find('**/__Actor_head')
                character.setH(90)

            self.slappyStand.loop('watch-idle')
            self.ignore('enter' + self.pieCollision.node().getName())
            self.alec.setPos(-4.5, -0.14, 3.13)
            self.slappy.setPos(1, 9, 3.03)
            self.flippy.setPos(2, -10, 3.23)
        if self.finishedCogLanding:
            self.slappyStand.pose('sad', 249)
            self.flippy.setPosHpr(-15, -12, 0, 0, 0, 0)
            self.alec.setPos(-1.5, -0.14, 3.13)
            self.slappy.hide()
            self.slappy.removeActive()
            self.surlee.setPosHpr(-32, -15, 0, 40, 0, 0)
            self.accept('enter' + self.pieCollision.node().getName(), self.handleWheelbarrowCollisionSphereEnter)
        if self.finishedInvasion:
            base.cr.cameraManager.disableScreen()
            self.surlee.setPosHpr(-32, -15, 0, 40, 0, 0)
            self.flippy.setPosHpr(-38, -18.5, 0, 75, 0, 0)
            self.alec.setPosHpr(18.0, 41.2, 0, -130, 0, 0)
        if self.finishedInvasionEnding:
            self.alec.setPosHpr(3, -7, 3.23, 165, 0, 0)
            self.flippy.setPos(2, -10, 3.23)
            self.flippy.setH(90)

    def enterPreShow(self, offset):
        self.cameras = []
        for cameraId in base.cr.cameraManager.cameraIds:
            self.cameras.append(base.cr.doId2do[cameraId])

        self.surleeLeaveInterval = Sequence(Wait(7), Parallel(Func(self.moveCamera, 3, 49, 14, 8, 213, 0), Func(base.cr.cameraManager.setMainCamera, self.cameras[3].getDoId())), Func(self.moveCamera, 0, 59, 12, 9, 237, 0), Parallel(Func(self.moveCamera, 1, 80, 20, 9.2, -180, 0), Func(self.moveCamera, 2, 72.5, -18, 9, 314, 0)), Parallel(Func(self.surlee.removeActive), Func(self.surlee.hide), Func(self.surleeR.show), Func(self.surleeR.addActive), Func(self.surleeR.startBlink)), Wait(3), Func(self.surleeR.setChatAbsolute, 'Hrm, you heard the HQ. I better get out of the way before Alec arrives.', CFSpeech | CFTimeout), Wait(1), Parallel(Func(self.surleeR.loop, 'walk'), self.surleeR.posHprInterval(4, (-20, 0, 0), (190, 0, 0)), Func(base.cr.cameraManager.tvFlyIn.start)), Parallel(Func(self.surleeR.loop, 'neutral'), self.surleeR.head.hprInterval(1, (75, 30, 0), blendType='easeInOut')), Wait(1), Func(self.surleeR.setChatAbsolute, "Oh, do you like it? Designed it myself. Don't worry about getting close to the ropes; the TV will be showing a live feed for everyone to get a great view.", CFSpeech | CFTimeout), Func(self.surleeR.loop, 'walk'), Parallel(self.surleeR.hprInterval(1, (80, 0, 0)), self.surleeR.head.hprInterval(1, (0, 0, 0), blendType='easeInOut')), Func(self.surleeR.loop, 'neutral'), Wait(8), Func(self.surleeR.setChatAbsolute, 'I know you all will keep trying to jump on top of each other for a better view anyway, though, so try not to hurt anyone.', CFSpeech | CFTimeout), Wait(3), Func(base.cr.cameraManager.setMainCamera, self.cameras[0].getDoId()), Func(self.moveCamera, 3, 39, -2, 7, 572, 0), Func(self.surleeR.loop, 'run'), self.surleeR.posHprInterval(2, (-17, -7, 0), (180, 0, 0)), self.surleeR.posHprInterval(1.5, (-15, -15, 0), (190, 0, 0)), Func(self.surleeR.loop, 'walk'), self.surleeR.posHprInterval(2, (-20, -18, 0), (90, 0, 0)), self.surleeR.posHprInterval(3.5, (-32, -19, 0), (35, 0, 0)), self.surleeR.posHprInterval(1, (-34, -17, 0), (0, 0, 0)), self.surleeR.posHprInterval(1.5, (-32, -15, 0), (-40, 0, 0)), Func(self.surleeR.loop, 'neutral'))
        self.surleeLeaveInterval.start()
        self.surleeLeaveInterval.setT(offset)

    def enterBegin(self, offset):
        self.finishedPreShow = True
        self.catchUp()
        for character in self.characters:
            character.reparentTo(self.showFloor)
            character.setPosHpr(35, -0.3, 0, 90, 0, 0)
            character.useLOD(1000)
            character.addActive()
            character.startBlink()
            character.head = character.find('**/__Actor_head')

        musicIntro = base.loadMusic(ElectionGlobals.IntroMusic)
        self.slappyStand.loop('watch-idle')
        self.ignore('enter' + self.pieCollision.node().getName())
        self.alecHallInterval = Sequence(Parallel(Func(self.alec.loop, 'walk'), Func(base.playMusic, musicIntro, looping=0, volume=0.8)), self.alec.posInterval(3, (12.96, -0.38, 0)), self.alec.posInterval(2, (4.2, -0.25, 3.13)), self.alec.posInterval(2, (-4.5, -0.14, 3.13)), Func(self.alec.loop, 'neutral'))
        self.slappyHallInterval = Sequence(Wait(1), Func(self.slappy.loop, 'walk'), self.slappy.posInterval(2.5, (12.96, -0.38, 0)), self.slappy.posHprInterval(2, (4.3, 2.72, 3.13), (70, 0, 0)), self.slappy.posHprInterval(1, (2.36, 5.18, 3.08), (40, 0, 0)), self.slappy.posHprInterval(1, (1, 9, 3.03), (90, 0, 0)), Func(self.slappy.loop, 'neutral'))
        self.flippyHallInterval = Sequence(Wait(2), Func(self.flippy.loop, 'walk'), self.flippy.posInterval(3, (12.96, -0.38, 0)), self.flippy.posHprInterval(1, (3.3, -2.39, 3.13), (120, 0, 0)), self.flippy.posHprInterval(1, (2.49, -6.09, 3.17), (155, 0, 0)), self.flippy.posHprInterval(1, (2, -10, 3.23), (90, 0, 0)), Func(self.flippy.loop, 'neutral'))
        self.alecHallInterval.start()
        self.alecHallInterval.setT(offset)
        self.slappyHallInterval.start()
        self.slappyHallInterval.setT(offset)
        self.flippyHallInterval.start()
        self.flippyHallInterval.setT(offset)

    def exitBegin(self):
        self.alecHallInterval.finish()
        self.slappyHallInterval.finish()
        self.flippyHallInterval.finish()
        self.surleeLeaveInterval.finish()

    def enterAlecSpeech(self, offset):
        self.finishedPreShow = True
        self.finishedBegin = True
        self.catchUp()
        self.alecSpeech = Sequence(Func(self.alec.setChatAbsolute, 'Hellooo Toontown~!', CFSpeech | CFTimeout), Wait(1), self.flippy.head.hprInterval(1, (-25, 0, 0), blendType='easeInOut'), Wait(1), self.slappy.head.hprInterval(1, (20, 3, 0), blendType='easeInOut'), Wait(1), Func(self.alec.setChatAbsolute, "As many of you know, I'm your Hilarious Host and Eccentric Elector: Alec Tinn!", CFSpeech | CFTimeout), Wait(8.5), Func(self.alec.setChatAbsolute, "And of course, we can't forget about our two toonerific toons who have been selected to fight for the Presidency...", CFSpeech | CFTimeout), Wait(9), Func(self.alec.setChatAbsolute, 'Slappy Quackintosh, and Flippy Doggenbottom!', CFSpeech | CFTimeout), Wait(3.3), Func(self.slappy.play, 'wave'), self.flippy.head.hprInterval(1, (-70, 0, 0), blendType='easeInOut'), Wait(1.2), self.flippy.head.hprInterval(1, (0, 0, 0), blendType='easeInOut'), Func(self.slappy.loop, 'neutral'), Func(self.alec.setChatAbsolute, 'I must say, this turnout is absolutely, positivley, extra-tooneriffically, astounding!', CFSpeech | CFTimeout), Wait(6), Func(self.alec.setChatAbsolute, "It's truly an honor to be here on this day, and I'm sure I speak for all of us when I thank you for coming.", CFSpeech | CFTimeout), Wait(8), Func(self.alec.setChatAbsolute, 'Now, the votes are almost ready to be tallied! Flippy, Slappy, do either of you have anything to say before the moment of truth?', CFSpeech | CFTimeout), Wait(10), Func(base.cr.cameraManager.setMainCamera, self.cameras[1].getDoId()), Func(self.slappy.setChatAbsolute, 'The only thing I have to say, no matter who wins...', CFSpeech | CFTimeout), Wait(2), Parallel(self.flippy.head.hprInterval(1, (-70, 0, 0), blendType='easeInOut'), Sequence(Wait(0.5), self.alec.head.hprInterval(1, (-70, 0, 0), blendType='easeInOut'))), Wait(3), Func(self.slappy.setChatAbsolute, 'I know that Toontown is going to grow to be even more... "Toontastic" than ever before.', CFSpeech | CFTimeout), Wait(8), Func(self.slappy.setChatAbsolute, 'All of you are truer-than-truly the best!', CFSpeech | CFTimeout), Wait(7), self.flippy.head.hprInterval(1, (0, 0, 0), blendType='easeInOut'), Wait(1), Func(base.cr.cameraManager.setMainCamera, self.cameras[2].getDoId()), Func(self.flippy.setChatAbsolute, "Like Slappy said, I can't even begin to thank all of you Toontastic toons for this.", CFSpeech | CFTimeout), Wait(1), self.alec.head.hprInterval(2, (70, 0, 0), blendType='easeInOut'), Wait(5), Func(self.flippy.setChatAbsolute, "Even after all of this terrific time together, I'm still speechless that I'm here today.", CFSpeech | CFTimeout), Wait(8), Func(self.flippy.setChatAbsolute, "Here's to Toontown, Slappy, and all of you!", CFSpeech | CFTimeout), Wait(3), self.slappy.head.hprInterval(1, (70, 0, 0), blendType='easeInOut'), Wait(3), Func(base.cr.cameraManager.setMainCamera, self.cameras[0].getDoId()), Func(self.alec.setChatAbsolute, 'Well said, the both of you!', CFSpeech | CFTimeout), self.alec.head.hprInterval(1, (0, 0, 0), blendType='easeInOut'), Wait(1), self.flippy.head.hprInterval(1, (-25, 0, 0), blendType='easeInOut'), Wait(1), self.slappy.head.hprInterval(1, (20, 3, 0), blendType='easeInOut'), Wait(1), Func(self.alec.setChatAbsolute, "Ooh, I'm just jittering with excitement. Are you toons ready to hear the winners?", CFSpeech | CFTimeout), Wait(7), Func(self.alec.setChatAbsolute, 'Without further ado, it is now time to start the GRAND ELECTORAL COUNTERS!', CFSpeech | CFTimeout), Wait(8), Func(self.alec.setChatAbsolute, 'Here we gooooo...', CFSpeech | CFTimeout), Wait(4))
        self.alecSpeech.start()
        self.alecSpeech.setT(offset)

    def exitAlecSpeech(self):
        self.alecSpeech.finish()

    def enterVoteBuildup(self, offset):
        self.finishedPreShow = True
        self.finishedBegin = True
        self.catchUp()
        musicAnnouncement = base.loadMusic(ElectionGlobals.AnnouncementMusic)
        sfxDrumroll = loader.loadSfx('phase_4/audio/sfx/EE_Drumroll.ogg')
        self.buildupSequence = Sequence(Func(self.alec.setChatAbsolute, 'The winner is...', CFSpeech | CFTimeout), Wait(4), Parallel(Func(self.counterLeft.play, 'body'), Func(self.counterRight.play, 'body')), Wait(3.7), Func(base.playSfx, sfxDrumroll), Wait(3.3), Func(self.alec.setChatAbsolute, 'Oh boy, you can feel the suspense!', CFSpeech | CFTimeout), Wait(9), Func(self.alec.setChatAbsolute, "It's...", CFSpeech | CFTimeout), Wait(4), Func(self.alec.setChatAbsolute, 'HOLY SMOKES!', CFSpeech | CFTimeout), Wait(7), Func(self.alec.setChatAbsolute, 'Well, there you have it. The new President of the Toon Council...', CFSpeech | CFTimeout), Wait(5), Func(base.playMusic, musicAnnouncement, looping=0, volume=0.8), self.alec.head.hprInterval(1, (-70, 0, 0), blendType='easeInOut'), Wait(1), Func(self.alec.setChatAbsolute, 'SLAPPYYYY~ QUACKINTOSH!', CFSpeech | CFTimeout), Wait(2), self.flippy.head.hprInterval(1, (-60, 0, 0), blendType='easeInOut'), Func(self.slappy.showLaughMuzzle), Func(base.cr.cameraManager.setMainCamera, self.cameras[1].getDoId()), ActorInterval(self.slappy, 'good-putt'), ActorInterval(self.slappy, 'happy-dance'), Func(self.slappy.loop, 'neutral'))
        self.buildupSequence.start()
        self.buildupSequence.setT(offset)

    def enterWinnerAnnounce(self, offset):
        self.finishedPreShow = True
        self.finishedBegin = True
        self.catchUp()
        musicVictory = base.loadMusic(ElectionGlobals.VictoryMusic)
        self.victorySequence = Sequence(Func(base.playMusic, musicVictory, looping=0, volume=0.8), Wait(0.3), Func(self.slappy.setChatAbsolute, "Holy smokes... I don't even know where to begin!", CFSpeech | CFTimeout), Wait(4), Func(self.slappy.setChatAbsolute, 'I know without any doubt that I hereby accept my duty as your President...', CFSpeech | CFTimeout), Wait(5), Func(self.slappy.setChatAbsolute, '...and will Presently Preside with full Presidential Priorities of this Presidentliness!', CFSpeech | CFTimeout))
        self.victorySequence.start()
        self.victorySequence.setT(offset)

    def exitWinnerAnnounce(self):
        self.victorySequence.finish()

    def enterCogLanding(self, offset):
        self.finishedPreShow = True
        self.finishedBegin = True
        self.catchUp()
        musicSad = base.loadMusic(ElectionGlobals.SadMusic)
        sfxSad = loader.loadSfx('phase_5/audio/sfx/ENC_Lose.ogg')
        mtrack = self.suit.beginSupaFlyMove(Point3(65, 3.6, 4.0), 1, 'fromSky', walkAfterLanding=False)
        self.slappyStandDie = Sequence(ActorInterval(self.slappyStand, 'sad'))
        self.pie = BattleProps.globalPropPool.getProp('creampie')
        self.cogSequence = Sequence(Parallel(Func(self.moveCamera, 1, 56, 26, 9, 204, 0), Func(base.cr.cameraManager.setMainCamera, self.cameras[1].getDoId())), Parallel(Func(self.suit.reparentTo, render), Func(self.suit.addActive), Func(mtrack.start, offset)), self.flippy.head.hprInterval(1, (-15, -10, 0), blendType='easeInOut'), Wait(1), self.alec.head.hprInterval(1, (-15, -5, 0), blendType='easeInOut'), Func(self.slappy.setChatAbsolute, 'I will ensure- Uhh...', CFSpeech | CFTimeout), Func(self.slappy.hideLaughMuzzle), Wait(2), Func(self.surleeR.sadEyes), Wait(3), Func(self.alec.setChatAbsolute, 'Wha- What is that...?', CFSpeech | CFTimeout), Wait(5), Func(self.slappy.setChatAbsolute, 'Err... Hey there, fella!', CFSpeech | CFTimeout), Func(self.slappy.loop, 'walk'), self.slappy.posHprInterval(1, (-4, 8.5, 3.03), (110, 0, 0)), Func(self.slappy.play, 'jump'), Wait(0.45), self.slappy.posInterval(0.2, (-7.5, 8.3, 3.5)), self.slappy.posHprInterval(0.4, (-13, 8, 0), (125, 0, 0)), Wait(0.8), Func(self.slappy.loop, 'neutral'), self.slappy.head.hprInterval(0.5, (-3, 5, 0)), Func(self.slappy.setChatAbsolute, 'My name is Slappy, the newly elected President of the Toon Council in this Toonerrific Town.', CFSpeech | CFTimeout), Wait(5), Func(self.suit.setChatAbsolute, 'President, you say? Just the Toon I need to speak with.', CFSpeech | CFTimeout, dialogue=self.speechStatementSfx), Wait(5), Func(self.slappy.setChatAbsolute, "Boy, that's some propeller you have there! You know, it looks a lot like the one on that TV.", CFSpeech | CFTimeout), Wait(5), Func(self.suit.setChatAbsolute, 'Yes. Now as I began to-', CFSpeech | CFTimeout, dialogue=self.speechQuestionSfx), Wait(1), Func(self.slappy.setChatAbsolute, "Ooh, and the suit too. Where did you come from, anyway? It can't be Loony Labs, they're off today.", CFSpeech | CFTimeout), Wait(5), Func(self.suit.setChatAbsolute, 'See here, Toon. I am-', CFSpeech | CFTimeout, dialogue=self.speechStatementSfx), Wait(1), Func(self.slappy.setChatAbsolute, "No, don't tell me. Let me guess. Errrr... Montana. Final answer. No, no, nevermind. They wouldn't have that fancy of a suit there. Hrmm...", CFSpeech | CFTimeout), Wait(1), ActorInterval(self.slappy, 'think', startFrame=0, endFrame=46), ActorInterval(self.slappy, 'think', startFrame=46, endFrame=0), Func(self.slappy.loop, 'neutral'), Wait(1), Func(self.suit.setChatAbsolute, 'STOP!', CFSpeech | CFTimeout, dialogue=self.speechGruntSfx), Wait(4), Func(self.suit.setChatAbsolute, 'I like your lingo, Toon. You know how to schmooze.', CFSpeech | CFTimeout, dialogue=self.speechMurmurSfx), Wait(6), Func(self.suit.setChatAbsolute, 'However, you seem to need a smear of Positive Reinforcement.', CFSpeech | CFTimeout, dialogue=self.speechStatementSfx), Wait(3), self.slappy.head.hprInterval(1, (0, 0, 0)), Func(self.slappy.sadEyes), Wait(1), Func(self.slappy.play, 'lose'), Wait(2), Func(base.playSfx, sfxSad, volume=0.6), Wait(1.8), Func(base.playMusic, musicSad, looping=0), Wait(0.5), Parallel(Func(self.slappyStandDie.start), Func(self.slappyStandDie.setT, offset)), Func(self.flippy.setChatAbsolute, 'Slappy, NO!', CFSpeech | CFTimeout), Wait(0.5), Func(self.alec.setChatAbsolute, 'Oh my goodness- he...', CFSpeech | CFTimeout), self.slappy.scaleInterval(1.5, VBase3(0.01, 0.01, 0.01), blendType='easeInOut'), Wait(2), Parallel(Func(self.alec.setChatAbsolute, "No. Nonono, no. This isn't happening.", CFSpeech | CFTimeout), Func(self.alec.loop, 'walk')), Parallel(self.alec.posInterval(2, (-1.5, -0.14, 3.13))), Func(self.alec.loop, 'neutral'), Parallel(Func(self.moveCamera, 2, 77, -23, 9, 398, 0), Func(base.cr.cameraManager.setMainCamera, self.cameras[2].getDoId())), Parallel(Func(self.flippy.setChatAbsolute, 'What have you done?!', CFSpeech | CFTimeout), Func(self.flippy.loop, 'run')), Wait(0.5), Parallel(self.flippy.posHprInterval(0.5, (-4.2, -9.5, 3.23), (70, 0, 0)), self.flippy.head.hprInterval(0.5, (0, 0, 0), blendType='easeInOut')), Wait(0.45), Func(self.flippy.play, 'jump'), Wait(0.45), self.flippy.posInterval(0.2, (-7.5, -9.2, 3.5)), self.flippy.posHprInterval(0.4, (-14, -9, 0), (50, 0, 0)), Wait(0.2), Func(self.flippy.loop, 'run'), Func(self.suit.loop, 'walk'), Parallel(self.suit.hprInterval(1, (180, 0, 0)), self.flippy.posHprInterval(1, (-15, -1, 0), (0, 0, 0))), Func(self.suit.loop, 'neutral'), Parallel(Func(self.flippy.setChatAbsolute, 'Where did you send him?! Where is he?!', CFSpeech | CFTimeout), Func(self.flippy.loop, 'neutral')), Wait(2.5), Func(self.alec.setChatAbsolute, 'Flippy, NO! Get away from it!', CFSpeech | CFTimeout), self.alec.head.hprInterval(1, (-5, -5, 0), blendType='easeInOut'), Wait(5), Func(self.flippy.setChatAbsolute, 'What... What are you?', CFSpeech | CFTimeout), Wait(4), Func(self.suit.setChatAbsolute, "I don't like your tone. Perhaps you need a drop of Positive Reinforcement as well.", CFSpeech | CFTimeout, dialogue=self.speechStatementSfx), Wait(3), Parallel(Func(self.flippy.setChatAbsolute, "No.. No, get away. I don't need your help.", CFSpeech | CFTimeout), ActorInterval(self.flippy, 'walk', loop=1, playRate=-1, duration=3), self.flippy.posInterval(3, (-15, -7, 0)), self.alec.head.hprInterval(1, (0, -5, 0), blendType='easeInOut')), Func(self.flippy.loop, 'neutral'), Wait(1.5), Func(self.suit.loop, 'walk'), Parallel(Func(self.suit.setChatAbsolute, "Let me confirm our meeting to discuss this. I won't take no for an answer.", CFSpeech | CFTimeout, dialogue=self.speechMurmurSfx), self.suit.posInterval(2, (65, -1, 4.0))), Func(self.suit.loop, 'neutral'), Parallel(Func(self.flippy.setChatAbsolute, "Stop it, this isn't fun!", CFSpeech | CFTimeout), self.alec.head.hprInterval(1, (10, -5, 0), blendType='easeInOut'), ActorInterval(self.flippy, 'walk', loop=1, playRate=-1, duration=2), self.flippy.posInterval(2, (-15, -12, 0))), Func(self.flippy.loop, 'neutral'), Func(self.suit.loop, 'walk'), Parallel(Func(self.suit.setChatAbsolute, 'Fun cannot exist without order.', CFSpeech | CFTimeout, dialogue=self.speechStatementSfx), self.suit.posInterval(2, (65, -5, 4.0))), Func(self.suit.loop, 'neutral'), Parallel(ActorInterval(self.flippy, 'throw', startFrame=0, endFrame=46), Func(self.flippy.setChatAbsolute, "I'm warning you, stay back. Please.", CFSpeech | CFTimeout), Func(self.pie.reparentTo, self.flippy.rightHand)), Wait(1), Func(self.suit.setChatAbsolute, "Don't worry, I haven't been wrong yet.", CFSpeech | CFTimeout, dialogue=self.speechStatementSfx), Wait(1.5), Parallel(Sequence(ActorInterval(self.flippy, 'throw', startFrame=47, endFrame=91), Func(self.flippy.loop, 'neutral')), Func(self.flippy.setChatAbsolute, 'Stay AWAY from me!', CFSpeech | CFTimeout), Func(self.surleeR.normalEyes), Sequence(Wait(0.6), Func(self.pie.wrtReparentTo, render), ProjectileInterval(self.pie, endPos=Point3(65, -5, 9.0), duration=0.1), Func(self.pie.removeNode), Parallel(Func(self.sendUpdate, 'setSuitDamage', [36, False]), Func(self.suit.hide), Func(self.suit.removeActive)))))
        self.cogSequence.start()
        self.cogSequence.setT(offset)

    def exitCogLanding(self):
        self.cogSequence.finish()

    def enterInvasion(self, offset):
        self.finishedPreShow = True
        self.finishedBegin = True
        self.finishedCogLanding = True
        self.catchUp()
        self.accept('enter' + self.pieCollision.node().getName(), self.handleWheelbarrowCollisionSphereEnter)
        self.surleeAnimation = Sequence(ActorInterval(self.surlee, 'scientistEmcee', startFrame=251, endFrame=314), ActorInterval(self.surlee, 'scientistEmcee', startFrame=314, endFrame=251))
        self.alecRunAway = Sequence(Func(self.alec.loop, 'walk'), self.alec.posInterval(1, (4.2, -0.25, 3.13)), self.alec.posHprInterval(3, (12.9, -3.3, 0), (0, 0, 0)), Func(self.alec.loop, 'neutral'), Wait(0.5), Func(self.alec.loop, 'run'), self.alec.posInterval(3, (18.0, 41.2, 0)), Func(self.alec.loop, 'walk'), self.alec.hprInterval(1.3, (-130, 0, 0)), Func(self.alec.loop, 'neutral'), Func(self.startInteractiveAlec))
        self.surleeIntroInterval = Sequence(Func(base.cr.cameraManager.setMainCamera, self.cameras[3].getDoId()), Func(self.moveCamera, 4, 10, -31, 7, 651, 0), Func(self.surleeR.loop, 'walk'), Func(self.surleeR.setChatAbsolute, "Everyone, listen. There's no time to explain!", CFSpeech | CFTimeout), self.surleeR.posHprInterval(1, (-32, -15, 0), (50, 0, 0)), Func(self.surleeR.loop, 'neutral'), Func(self.cameras[4].setState, 'Move', globalClockDelta.getRealNetworkTime(), 10, -24, 7, -263, 0, 0), Parallel(self.alec.head.hprInterval(1, (15, 0, 0), blendType='easeInOut')), self.flippy.head.hprInterval(1, (80, 0, 0), blendType='easeInOut'), Parallel(Func(self.flippy.loop, 'walk'), self.flippy.hprInterval(2, (95, 0, 0)), self.flippy.head.hprInterval(2, (0, 0, 0))), Func(self.flippy.loop, 'neutral'), Wait(2), Func(self.surleeR.setChatAbsolute, 'Grab the pies, they seem to be the weakness of these...', CFSpeech | CFTimeout), Wait(5), Func(self.surleeR.setChatAbsolute, '..."Cogs."', CFSpeech | CFTimeout), Wait(3), Func(self.surleeR.setChatAbsolute, "Now take up arms, there's more on the way!", CFSpeech | CFTimeout), Wait(3), Func(self.alecRunAway.start, offset), Wait(2), Func(self.surleeR.setChatAbsolute, 'Fight for our town. Fight for Slappy!', CFSpeech | CFTimeout), Wait(7), Func(base.cr.cameraManager.disableScreen), Wait(3), Parallel(Func(self.surlee.show), Func(self.surlee.addActive), Func(self.surleeR.hide), Func(self.surleeR.removeActive), Func(self.surleeAnimation.loop, offset)), Func(self.surlee.setChatAbsolute, "Flippy, I'm going to need you over here to help with the pies. Can you get cooking?", CFSpeech | CFTimeout), Wait(7), Func(base.cr.cameraManager.setMainCamera, self.cameras[4].getDoId()), Func(self.flippy.setChatAbsolute, 'I can certainly try.', CFSpeech | CFTimeout), Wait(1), Func(self.flippy.loop, 'run'), self.flippy.posHprInterval(3.5, (-38, -18.5, 0), (100, 0, 0)), Func(self.flippy.loop, 'walk'), self.flippy.posHprInterval(1.5, (-38, -18.5, 0), (75, 0, 0)), Func(self.flippy.loop, 'neutral'))
        self.surleeIntroInterval.start()
        self.surleeIntroInterval.setT(offset)

    def exitInvasion(self):
        self.surleeIntroInterval.finish()
        self.surleeAnimation.finish()

    def enterInvasionEnd(self, offset):
        self.finishedPreShow = True
        self.finishedBegin = True
        self.finishedCogLanding = True
        self.finishedInvasion = True
        self.catchUp()
        pie = BattleProps.globalPropPool.getProp('creampie')
        pie.setScale(0)
        cake = BattleProps.globalPropPool.getProp('birthday-cake')
        cake.setScale(0)
        weddingcake = BattleProps.globalPropPool.getProp('wedding-cake')
        weddingcake.setScale(0)
        sfxCake = loader.loadSfx('phase_5/audio/sfx/AA_throw_wedding_cake.ogg')
        sfxCakeSplat = loader.loadSfx('phase_5/audio/sfx/AA_throw_wedding_cake_cog.ogg')
        sfxPieSplat = loader.loadSfx('phase_3.5/audio/sfx/AA_tart_only.ogg')
        messenger.send('invasionEndSequence', [offset])
        cakeSeq = Sequence(Func(self.flippy.loop, 'walk'), self.flippy.hprInterval(2, (0, 0, 0)), Func(self.flippy.loop, 'neutral'), Func(self.flippy.setChatAbsolute, 'Here we go...', CFSpeech | CFTimeout), Wait(3), Func(self.flippy.loop, 'run'), Parallel(self.flippy.posHprInterval(2.5, (-14, -9, 0), (-90, 0, 0)), self.flippy.head.hprInterval(0.5, (-65, 0, 0), blendType='easeInOut')), Func(self.flippy.play, 'jump'), Wait(0.45), self.flippy.posInterval(0.2, (-7.5, -9.2, 3.5)), self.flippy.posInterval(0.4, (-4.2, -9.5, 3.23)), Func(self.flippy.loop, 'run'), Parallel(self.flippy.posHprInterval(1, (2, -10, 3.23), (75, 0, 0)), self.flippy.head.hprInterval(0.5, (-5, 0, 0), blendType='easeInOut')), Func(self.flippy.loop, 'neutral'), Wait(5.5), Parallel(ActorInterval(self.flippy, 'throw', startFrame=0, endFrame=46), Func(pie.reparentTo, self.flippy.rightHand), pie.scaleInterval(0.5, 1)), Parallel(Sequence(ActorInterval(self.flippy, 'throw', startFrame=47, endFrame=91), Func(self.flippy.loop, 'neutral')), Sequence(Wait(0.6), Func(self.flippy.setChatAbsolute, "That's for the election!", CFSpeech | CFTimeout), Func(pie.wrtReparentTo, render), ProjectileInterval(pie, endPos=Point3(36.5, -1.9, 11.0), duration=0.3), Func(base.playSfx, sfxPieSplat, volume=0.8), Func(self.sendUpdate, 'setSuitDamage', [36, False]), Func(pie.removeNode))), Wait(1), Parallel(ActorInterval(self.flippy, 'throw', startFrame=0, endFrame=46), Func(cake.reparentTo, self.flippy.rightHand), cake.scaleInterval(0.5, 1)), Parallel(Sequence(ActorInterval(self.flippy, 'throw', startFrame=47, endFrame=91), Func(self.flippy.loop, 'neutral')), Sequence(Wait(0.6), Func(self.flippy.setChatAbsolute, "THAT'S for Slappy!", CFSpeech | CFTimeout), Func(cake.wrtReparentTo, render), ProjectileInterval(cake, endPos=Point3(36.5, -1.9, 11.0), duration=0.3), Func(base.playSfx, sfxPieSplat, volume=1.0), Func(self.sendUpdate, 'setSuitDamage', [100, False]), Func(cake.removeNode))), Wait(1), Parallel(Func(base.playSfx, sfxCake, volume=0.9), ActorInterval(self.flippy, 'throw', startFrame=0, endFrame=46), Func(weddingcake.reparentTo, self.flippy.rightHand), weddingcake.scaleInterval(0.5, 1.4)), Parallel(Sequence(ActorInterval(self.flippy, 'throw', startFrame=47, endFrame=91), Func(self.flippy.loop, 'neutral')), Sequence(Wait(0.6), Func(self.flippy.setChatAbsolute, 'AND THIS IS FOR TOONTOWN!', CFSpeech | CFTimeout), Func(weddingcake.wrtReparentTo, render), ProjectileInterval(weddingcake, endPos=Point3(36.5, -1.9, 11.0), duration=0.3), Func(base.playSfx, sfxCakeSplat, volume=0.8), Func(self.sendUpdate, 'setSuitDamage', [200, True]), Func(weddingcake.removeNode))), Wait(10), Func(self.alec.loop, 'run'), Func(self.alec.setChatAbsolute, 'Flippy, you did it!', CFSpeech | CFTimeout), self.alec.posHprInterval(5, (12.9, -0.3, 0), (180, 0, 0)), Parallel(self.alec.posHprInterval(1, (4.2, -3.25, 3.13), (90, 0, 0)), Func(self.flippy.loop, 'walk'), self.flippy.hprInterval(1, (0, 0, 0)), self.flippy.head.hprInterval(1, (15, 0, 0))), Func(self.flippy.loop, 'neutral'), self.alec.posHprInterval(1, (3, -7, 3.23), (165, 0, 0)), Func(self.alec.loop, 'neutral'), Wait(4), Func(self.surleeR.setChatAbsolute, "Don't get too excited... We've only driven them back to the streets.", CFSpeech | CFTimeout), Wait(3), Func(self.flippy.loop, 'walk'), Parallel(self.flippy.hprInterval(1, (90, 0, 0)), self.flippy.head.hprInterval(1, (0, 0, 0))), Func(self.flippy.loop, 'neutral'), Wait(4), Func(self.surleeR.setChatAbsolute, "The Cogs will be back, but I doubt we'll be seeing them in the playgrounds again after this battle.", CFSpeech | CFTimeout), Wait(7), Func(self.surleeR.setChatAbsolute, "All of you here today are heros, you're survivors!", CFSpeech | CFTimeout), Wait(7), Func(self.surleeR.setChatAbsolute, "And I'm sure our new President is very grateful.", CFSpeech | CFTimeout), Wait(6), Func(self.flippy.setChatAbsolute, 'Surlee, I...', CFSpeech | CFTimeout), Wait(5), Func(self.alec.setChatAbsolute, "He's right, Flippy. You're a hero, and you're the only leader we have left.", CFSpeech | CFTimeout), Wait(7), Func(self.flippy.setChatAbsolute, 'With a heavy heart, I hereby accept the Toon Council Presidency.', CFSpeech | CFTimeout), Wait(7), Func(self.flippy.setChatAbsolute, 'Only until these Cogs are gone, though.', CFSpeech | CFTimeout), Wait(7), Func(self.flippy.setChatAbsolute, "If we're going to get rid of them, we have to stand together.", CFSpeech | CFTimeout), Wait(7))
        cakeSeq.start()
        cakeSeq.setT(offset)

    def enterWrapUp(self, offset):
        self.finishedPreShow = True
        self.finishedBegin = True
        self.finishedCogLanding = True
        self.finishedInvasion = True
        self.finishedInvasionEnding = True
        self.catchUp()
        self.stopInteractiveAlec()
        NodePath(base.marginManager).hide()
        base.cr.credits.setLocalToonDetails(base.localAvatar.getName(), base.localAvatar.style)
        musicCredits = base.loadMusic(ElectionGlobals.CreditsMusic)
        base.localAvatar.stopUpdateSmartCamera()
        base.camera.wrtReparentTo(render)
        self.logo = loader.loadModel('phase_3/models/gui/toontown-logo')
        self.logo.reparentTo(aspect2d)
        self.logo.setTransparency(1)
        self.logo.setScale(0.6)
        self.logo.setPos(0, 1, 0.3)
        self.logo.setColorScale(1, 1, 1, 0)
        self.portal = loader.loadModel('phase_3.5/models/props/portal-mod')
        self.portal.reparentTo(render)
        self.portal.setPosHprScale(93.1, 0.4, 4, 4, 355, 45, 0, 0, 0)
        from direct.gui.OnscreenText import OnscreenText
        from direct.gui.OnscreenImage import OnscreenImage
        from toontown.credits import AlphaCredits
        self.shockley = AlphaCredits.Shockley(True)
        self.shockley.load()
        self.laffMeter = base.localAvatar.laffMeter
        self.book = base.localAvatar.book.bookOpenButton
        self.book2 = base.localAvatar.book.bookCloseButton
        base.localAvatar.setPieType(0)
        base.localAvatar.setNumPies(0)
        base.localAvatar.disableAvatarControls()
        self.clearHudSeq = Sequence(Parallel(self.laffMeter.posInterval(10, (-0.5, 0.0, 0.13)), self.book.posInterval(10, (0.5, 0.0, 0.17)), self.book2.posInterval(10, (0.5, 0.0, 0.17))))
        self.wrapUpSequence = Sequence(Func(base.cr.cameraManager.tv.hide), Func(self.flippy.setChatAbsolute, 'Toons of the world...', CFSpeech | CFTimeout), Func(base.playMusic, musicCredits, looping=0, volume=0.8), Wait(4.5), Func(self.flippy.setChatAbsolute, 'UNITE!', CFSpeech | CFTimeout), Func(self.flippy.stopBlink), ActorInterval(self.flippy, 'victory', playRate=0.75, startFrame=0, endFrame=9), Func(base.camera.setPosHpr, 73, -9.5, 16, -90, -35, 0), Func(base.takeScreenShot), Wait(7.5), ActorInterval(self.flippy, 'victory', playRate=0.75, startFrame=9, endFrame=0), Wait(7.5), Parallel(self.shockley.title.colorScaleInterval(0.5, (1, 1, 1, 1)), self.shockley.description.colorScaleInterval(0.5, (1, 1, 1, 1)), self.shockley.image.colorScaleInterval(0.5, (1, 1, 1, 1))), Func(base.cr.loginFSM.request, 'credits'))
        self.cameraSequence = Sequence(base.camera.posHprInterval(10, (75, -9.5, 12), (-90, -10, 0), blendType='easeInOut'), Func(self.wrapUpSequence.start), Wait(12), Parallel(self.logo.posHprScaleInterval(6.5, (0, 0, 0.5), 0, 1, blendType='easeOut'), self.logo.colorScaleInterval(6.5, Vec4(1, 1, 1, 1), blendType='easeOut'), base.camera.posHprInterval(7.5, (70, 0.6, 42.2), (-90, 0, 0), blendType='easeInOut')), Parallel(self.logo.colorScaleInterval(0.3, Vec4(1, 1, 1, 0)), base.camera.posHprInterval(0.3, (85, 0, 42), (-90, -30, 0), blendType='easeIn')), Parallel(base.camera.posHprInterval(0.9, (95, 0.6, 6), (-90, -90, 0), blendType='easeOut'), self.portal.scaleInterval(0.5, 2)))
        self.clearHudSeq.start()
        self.clearHudSeq.setT(offset)
        self.cameraSequence.start()
        self.cameraSequence.setT(offset)

    def exitWrapUp(self):
        self.logo.removeNode()
        self.portal.removeNode()
        self.shockley.title.removeNode()
        self.shockley.description.removeNode()
        self.shockley.image.removeNode()
        self.wrapUpSequence.finish()
        self.clearHudSeq.finish()
        self.cameraSequence.finish()

    def startInteractiveAlec(self):
        cs = CollisionSphere(0, 0, 0, 3)
        self.alecNode = self.alec.attachNewNode(CollisionNode('cnode'))
        self.alecNode.node().addSolid(cs)
        self.accept('enter' + self.alecNode.node().getName(), self.handleAlecCollision)

    def handleAlecCollision(self, collEntry):
        self.cowardSequence = Sequence(Parallel(ActorInterval(self.alec, 'cringe'), Func(self.alec.setChatAbsolute, "Don't hurt me!! Oh, phew. It's only you.", CFSpeech | CFTimeout)))
        self.cowardSequence.start()

    def stopInteractiveAlec(self):
        if self.alecNode:
            self.ignore('enter' + self.alecNode.node().getName())

    def moveCamera(self, id, x, y, z, h, p):
        self.cameras[id].setState('Move', globalClockDelta.getRealNetworkTime(), x, y, z, h, p, 0)

    def saySurleePhrase(self, phrase, interrupt, broadcast):
        self.surlee.setChatAbsolute(phrase, CFSpeech | CFTimeout, interrupt=interrupt)
        if broadcast and Vec3(base.localAvatar.getPos(self.surleeR)).length() >= 15:
            base.localAvatar.setSystemMessage(0, self.surleeR.getName() + ': ' + phrase, WTEmote)

    def setState(self, state, timestamp):
        self.request(state, globalClockDelta.localElapsedTime(timestamp))
