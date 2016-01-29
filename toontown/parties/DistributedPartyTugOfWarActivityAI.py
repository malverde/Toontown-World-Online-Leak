

from direct.directnotify import DirectNotifyGlobal

from DistributedPartyTeamActivityAI import DistributedPartyTeamActivityAI
from toontown.toonbase import TTLocalizer
import PartyGlobals

'''
dclass DistributedPartyTugOfWarActivity : DistributedPartyTeamActivity {
  reportKeyRateForce(uint32, int16/100) airecv clsend;
  reportFallIn(uint8) airecv clsend;
  setToonsPlaying(uint32 [0-4], uint32 [0-4]) required broadcast ram;
  updateToonKeyRate(uint32, uint32) broadcast;
  updateToonPositions(int16/1000) broadcast;
};
'''

scoreRef = {'tie': (PartyGlobals.TugOfWarTieReward, PartyGlobals.TugOfWarTieReward),
            0: (PartyGlobals.TugOfWarWinReward, PartyGlobals.TugOfWarLossReward),
            1: (PartyGlobals.TugOfWarLossReward, PartyGlobals.TugOfWarWinReward),
            10:(PartyGlobals.TugOfWarFallInWinReward, PartyGlobals.TugOfWarFallInLossReward),
            11: (PartyGlobals.TugOfWarFallInLossReward, PartyGlobals.TugOfWarFallInWinReward),
           }

class DistributedPartyTugOfWarActivityAI(DistributedPartyTeamActivityAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedPartyTugOfWarActivityAI")
    forbidTeamChanges = True
    startDelay = PartyGlobals.TugOfWarStartDelay

    def getDuration(self):
        return PartyGlobals.TugOfWarDuration

    def reportKeyRateForce(self, keyRate, force):
        # Basic sanity check
        av = self._getCaller()
        if not av:
            return

        avId = av.doId

        if not (avId in self.toonIds[0] or avId in self.toonIds[1]):
            self.air.writeServerEvent('suspicious', avId, 'sent DistributedPartyTugOfWarActivityAI.reportKeyRateForce, but not playing')
            return

        self.forces[avId] = force
        self.sendUpdate('updateToonKeyRate', [avId, keyRate])
        self.d_updateToonPositions()

    def d_updateToonPositions(self):
        _getTeamForce = lambda team: sum(self.forces.get(avId, 0) for avId in self.toonIds[team])

        f0 = _getTeamForce(0)
        f1 = _getTeamForce(1)
        fr = f0 + f1

        if fr != 0:
            delta = (f0 - f1) / fr
            self.pos += -delta * PartyGlobals.TugOfWarMovementFactor * 2

            self.sendUpdate('updateToonPositions', [self.pos])

    def reportFallIn(self, losingTeam):
        if self.fsm.state != 'Active' or self._hasFall:
            return

        # Basic sanity check
        av = self._getCaller()
        if not av:
            return

        avId = av.doId

        if not (avId in self.toonIds[0] or avId in self.toonIds[1]):
            self.air.writeServerEvent('suspicious', avId, 'sent DistributedPartyTugOfWarActivityAI.reportFallIn, but not playing')
            return

        losers = int(self.pos < 0)
        if losers != losingTeam:
            self.air.writeServerEvent('suspicious', avId, 'called DistributedPartyTugOfWarActivityAI.reportFallIn with incorrect losingTeam')

        self._hasFall = 1

        def _advance(task):
            self.calcReward()
            return task.done

        taskMgr.doMethodLater(1, _advance, self.taskName('fallIn-advance'))
        taskMgr.remove(self.taskName('finish')) # Mitigate races

    def calcReward(self):
        nobodyWins = abs(self.pos) <= 2
        if nobodyWins:
            self._winnerTeam = 3
            self._teamScores = scoreRef['tie']

        else:
            self._winnerTeam = int(self.pos < 0)
            self._teamScores = scoreRef[self._winnerTeam + self._hasFall * 10]

        self.b_setState('Conclusion', self._winnerTeam)

    def startActive(self, data):
        self.forces = {}
        self.pos = 0
        self._hasFall = 0
        DistributedPartyTeamActivityAI.startActive(self, data)

    def startConclusion(self, data):
        taskMgr.doMethodLater(1, self.__exitConclusion, self.taskName('exitconc'))

    def finishConclusion(self):
        taskMgr.remove(self.taskName('exitconc'))

    def __exitConclusion(self, task):
        def _sendReward(team):
            jb = self._teamScores[team]
            msg = TTLocalizer.PartyTeamActivityRewardMessage % jb

            for avId in self.toonIds[team]:
                av = self.air.doId2do.get(avId)
                if av:
                    self.sendUpdateToAvatarId(avId, 'showJellybeanReward', [jb, av.getMoney(), msg])
                    av.addMoney(jb)

        _sendReward(0)
        _sendReward(1)

        self.toonsPlaying = []
        self.toonIds = ([], [])

        self.updateToonsPlaying()

        self.b_setState('WaitForEnough')
        return task.done

