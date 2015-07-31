#Embedded file name: toontown.election.DistributedElectionEventAI
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
from direct.fsm.FSM import FSM
from otp.ai.MagicWordGlobal import *
from toontown.election.DistributedHotAirBalloonAI import DistributedHotAirBalloonAI
from DistributedElectionCameraManagerAI import DistributedElectionCameraManagerAI
from DistributedSafezoneInvasionAI import DistributedSafezoneInvasionAI
from DistributedInvasionSuitAI import DistributedInvasionSuitAI
from InvasionMasterAI import InvasionMasterAI
from toontown.toonbase import ToontownGlobals
import SafezoneInvasionGlobals
import ElectionGlobals
import random
from otp.distributed.OtpDoGlobals import *
from direct.task import Task

class DistributedElectionEventAI(DistributedObjectAI, FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedElectionEventAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        FSM.__init__(self, 'ElectionFSM')
        self.air = air
        self.stateTime = globalClockDelta.getRealNetworkTime()
        self.pieTypeAmount = [4, 20, 1]
        self.balloon = None
        self.cogDead = False
        self.master = InvasionMasterAI(self)
        self.toons = []
        self.suits = []

    def enterOff(self):
        self.balloon.requestDelete()
        self.requestDelete()

    def enterIdle(self):
        if self.balloon is None:
            self.balloon = DistributedHotAirBalloonAI(self.air)
            self.balloon.generateWithRequired(self.zoneId)
        if config.GetBool('want-doomsday', False):
            self.balloon.b_setState('ElectionIdle')
            if not hasattr(simbase.air, 'cameraManager'):
                camMgr = DistributedElectionCameraManagerAI(simbase.air)
                camMgr.spawnManager()
        else:
            self.balloon.b_setState('Waiting')

    def phraseSaidToFlippy(self, phraseId):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId, None)
        if not av:
            self.air.writeServerEvent('suspicious', avId=avId, issue="Someone tried to talk to Flippy while they aren't on the district!")
            return
        self.sendUpdate('flippySpeech', [avId, phraseId])

    def wheelbarrowAvatarEnter(self):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId, None)
        if not av:
            self.air.writeServerEvent('suspicious', avId=avId, issue="Got a request for pies from a toon that isn't on the district!")
            return
        if av.hp > 0:
            av.b_setPieType(self.pieTypeAmount[0])
            av.b_setNumPies(self.pieTypeAmount[1])
            av.b_setPieThrowType(self.pieTypeAmount[2])
        self.sendUpdate('flippySpeech', [avId, 1])

    def setPieTypeAmount(self, type, num):
        self.pieTypeAmount = [type, num]

    def slappyAvatarEnter(self):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId, None)
        if not av:
            self.air.writeServerEvent('suspicious', avId=avId, issue="Got a request for Slappy's Cheesy Effect from a toon that isn't on the district!")
            return
        av.b_setCheesyEffect(15, 0, 0)

    def enterEvent(self):
        event = simbase.air.doFind('ElectionEvent')
        if event is None:
            event = DistributedElectionEventAI(simbase.air)
            event.generateWithRequired(2000)
        if self.balloon is None:
            self.balloon = DistributedHotAirBalloonAI(self.air)
            self.balloon.generateWithRequired(self.zoneId)
        self.eventSequence = Sequence(Func(event.b_setState, 'PreShow'), Wait(34), Func(event.b_setState, 'Begin'), Wait(10), Func(event.b_setState, 'AlecSpeech'), Wait(128), Func(event.b_setState, 'VoteBuildup'), Wait(44), Func(event.b_setState, 'WinnerAnnounce'), Wait(12), Func(event.b_setState, 'CogLanding'), Wait(117), Func(event.b_setState, 'Invasion'))
        self.eventSequence.start()

    def enterPreShow(self):
        self.showAnnounceInterval = Sequence(Func(self.sendGlobalUpdate, 'TOON HQ: The Toon Council Presidential Elections will be starting any second!'), Wait(5), Func(self.sendGlobalUpdate, 'TOON HQ: Please silence your Shtickerbooks and keep any Oinks, Squeaks, and Owooos to a low rustle.'))
        self.showAnnounceInterval.start()

    def exitPreShow(self):
        self.showAnnounceInterval.finish()

    def enterBegin(self):
        pass

    def enterAlecSpeech(self):
        pass

    def enterVoteBuildup(self):
        pass

    def enterWinnerAnnounce(self):
        pass

    def enterCogLanding(self):
        self.landingSequence = Sequence(Wait(65), Func(self.balloon.b_setState, 'ElectionCrashing'))
        self.landingSequence.start()

    def exitCogLanding(self):
        self.landingSequence.finish()

    def enterInvasion(self):
        self.surleePhraseLoop = Sequence(Wait(30), Func(self.saySurleePhrase))
        self.invasionSequence = Sequence(Wait(15), Func(self.spawnInvasion), Func(self.surleePhraseLoop.loop))
        self.invasionSequence.start()

    def exitInvasion(self):
        self.invasionSequence.finish()
        self.surleePhraseLoop.finish()

    def enterInvasionEnd(self):
        self.cogDead = False

    def enterWrapUp(self):
        taskMgr.doMethodLater(60, self.b_setState, self.uniqueName('restart-election'), extraArgs=['Off'])

    def spawnInvasion(self):
        invasion = simbase.air.doFind('SafezoneInvasion')
        if invasion is None:
            invasion = DistributedSafezoneInvasionAI(simbase.air, self)
            invasion.generateWithRequired(2000)

    def setSuitDamage(self, hp, kill = False):
        if self.state == 'InvasionEnd':
            invasion = simbase.air.doFind('SafezoneInvasion')
            if invasion:
                invasion.setFinaleSuitStunned(hp, kill)
        elif not self.cogDead:
            self.cogDead = True
            self.suit = DistributedInvasionSuitAI(self.air, self)
            self.suit.dna.newSuit('ym')
            self.suit.setSpawnPoint(99)
            self.suit.setLevel(0)
            self.suit.generateWithRequired(ToontownGlobals.ToontownCentral)
            self.suit.takeDamage(hp)

    def saySurleePhrase(self, phrase = None, interrupt = 0, broadcast = False):
        if not phrase:
            phrase = random.choice(ElectionGlobals.SurleeTips)
        self.sendUpdate('saySurleePhrase', [phrase, interrupt, broadcast])

    def sendGlobalUpdate(self, text):
        for doId in simbase.air.doId2do:
            if str(doId)[:2] == '10':
                do = simbase.air.doId2do.get(doId)
                do.d_setSystemMessage(0, text)

    def setState(self, state):
        self.demand(state)

    def d_setState(self, state):
        self.stateTime = globalClockDelta.getRealNetworkTime()
        self.sendUpdate('setState', [state, self.stateTime])

    def b_setState(self, state):
        self.setState(state)
        self.d_setState(state)

    def getState(self):
        return (self.state, self.stateTime)


@magicWord(category=CATEGORY_MODERATION, types=[str])
def election(state):
    event = simbase.air.doFind('ElectionEvent')
    if event is None:
        event = DistributedElectionEventAI(simbase.air)
        event.generateWithRequired(2000)
    if not hasattr(event, 'enter' + state):
        return 'Invalid state'
    if not config.GetBool('want-doomsday', False):
        if not state == 'Idle':
            return 'These states will crash the game when Elections are disabled!'
    event.b_setState(state)
    return 'Election event now in %r state' % state
