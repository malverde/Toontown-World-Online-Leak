

from direct.directnotify import DirectNotifyGlobal
from direct.distributed.ClockDelta import globalClockDelta

from DistributedPartyActivityAI import DistributedPartyActivityAI
from activityFSMs import TeamActivityAIFSM
import PartyGlobals

'''
dclass DistributedPartyTeamActivity : DistributedPartyActivity {
  toonJoinRequest(uint8(0-1)) airecv clsend;
  toonExitRequest(uint8(0-1)) airecv clsend;
  toonSwitchTeamRequest() airecv clsend;
  setPlayersPerTeam(uint8, uint8) broadcast required;
  setDuration(uint8) broadcast required;
  setCanSwitchTeams(bool) broadcast required;
  setState(string, int16, uint32) broadcast ram;
  setToonsPlaying(uint32 [0-8], uint32 [0-8]) required broadcast ram;
  setAdvantage(uint16/100);
  switchTeamRequestDenied(uint8);
};
'''

'''self.defaultTransitions = {'WaitForEnough': ['WaitToStart'],
         'WaitToStart': ['WaitForEnough', 'WaitClientsReady'],
         'WaitClientsReady': ['WaitForEnough', 'Active'],
         'Active': ['WaitForEnough', 'Conclusion'],
         'Conclusion': ['WaitForEnough']}'''

class DistributedPartyTeamActivityAI(DistributedPartyActivityAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedPartyTeamActivityAI")
    forbidTeamChanges = False
    startDelay = PartyGlobals.TeamActivityStartDelay

    def __init__(self, air, parent, activityTuple):
        self.toonIds = ([], [])
        self.responses = set()
        self.fsm = TeamActivityAIFSM(self)

        DistributedPartyActivityAI.__init__(self, air, parent, activityTuple)

    def announceGenerate(self):
        self.b_setState('WaitForEnough')
        DistributedPartyActivityAI.announceGenerate(self)

    def toonJoinRequest(self, team):
        av = self._getCaller()
        if not av:
            return

        if not self.fsm.state in ('WaitForEnough', 'WaitToStart'):
            self.sendUpdateToAvatarId(av.doId, 'joinTeamRequestDenied', [PartyGlobals.DenialReasons.Default])
            return

        if len(self.toonIds[team]) >= self.getPlayersPerTeam()[1]:
            self.sendUpdateToAvatarId(av.doId, 'joinTeamRequestDenied', [PartyGlobals.DenialReasons.Full])
            return

        if av.doId in self.toonsPlaying:
            self.air.writeServerEvent('suspicious', av.doId, 'tried to join party team activity again!')
            self.sendUpdateToAvatarId(av.doId, 'joinTeamRequestDenied', [PartyGlobals.DenialReasons.Default])
            return

        # idgaf if they exit unexpectedly in this case
        self.toonIds[team].append(av.doId)
        DistributedPartyActivityAI.toonJoinRequest(self)
        self.__update()

    def toonExitRequest(self, team):
        av = self._getCaller()
        if not av:
            return

        if not self.fsm.state in ('WaitForEnough', 'WaitToStart'):
            self.sendUpdateToAvatarId(av.doId, 'exitRequestDenied', [PartyGlobals.DenialReasons.Default])
            return

        if not (av.doId in self.toonIds[0] or av.doId in self.toonIds[1]):
            self.air.writeServerEvent('suspicious', avId, 'tried to switch DistributedPartyActivityAI team, but not in one')
            self.sendUpdateToAvatarId(av.doId, 'exitRequestDenied', [PartyGlobals.DenialReasons.Default])
            return

        currentTeam = (1, 0)[av.doId in self.toonIds[0]]
        self.toonIds[currentTeam].remove(av.doId)

        DistributedPartyActivityAI.toonExitRequest(self)
        self.__update()

    def toonSwitchTeamRequest(self):
        av = self._getCaller()
        if not av:
            return

        if not self.getCanSwitchTeams():
            self.air.writeServerEvent('suspicious', avId, 'tried to switch DistributedPartyActivityAI team in bad time')
            self.sendUpdateToAvatarId(av.doId, 'switchTeamRequestDenied', [PartyGlobals.DenialReasons.Default])
            return

        if not (av.doId in self.toonIds[0] or av.doId in self.toonIds[1]):
            self.air.writeServerEvent('suspicious', avId, 'tried to switch DistributedPartyActivityAI team, but not in one')
            self.sendUpdateToAvatarId(av.doId, 'switchTeamRequestDenied', [PartyGlobals.DenialReasons.Default])
            return

        currentTeam = (1, 0)[av.doId in self.toonIds[0]]
        otherTeam = (1, 0)[currentTeam]

        if len(self.toonIds[otherTeam]) >= self.getPlayersPerTeam()[1]:
            self.sendUpdateToAvatarId(av.doId, 'switchTeamRequestDenied', [PartyGlobals.DenialReasons.Full])
            return

        self.toonIds[currentTeam].remove(av.doId)
        self.toonIds[otherTeam].append(av.doId)

        self.__update()

    def getPlayersPerTeam(self):
        return (PartyGlobals.CogActivityMinPlayersPerTeam,
                PartyGlobals.CogActivityMaxPlayersPerTeam)

    def __areTeamsCorrect(self):
        minPlayers = self.getPlayersPerTeam()[0]
        return all(len(self.toonIds[i]) >= minPlayers for i in xrange(2))

    def getDuration(self):
        raise NotImplementedError('getDuration() -- pure virtual')

    def getCanSwitchTeams(self):
        return self.fsm.state in ('Off', 'WaitForEnough', 'WaitToStart') and not self.forbidTeamChanges

    def updateToonsPlaying(self):
        self.sendUpdate('setToonsPlaying', self.getToonsPlaying())

    def getToonsPlaying(self):
        return self.toonIds

    def setAdvantage(self, todo0):
        pass

    def b_setState(self, state, data=0):
        self.fsm.request(state, data)
        self.d_setState(state, data)

    def d_setState(self, state, data=0):
        self.sendUpdate('setState', [state, globalClockDelta.getRealNetworkTime(), data])

    def _getCaller(self):
        avId = self.air.getAvatarIdFromSender()
        if avId not in self.air.doId2do:
            self.air.writeServerEvent('suspicious', avId, 'called some DistributedPartyActivityAI method outside shard')
            return None

        return self.air.doId2do[avId]

    def __update(self):
        self.updateToonsPlaying()

        if self.fsm.state == 'WaitForEnough':
            if self.__areTeamsCorrect():
                self.b_setState('WaitToStart')

        elif self.fsm.state == 'WaitToStart':
            if not self.__areTeamsCorrect():
                self.b_setState('WaitForEnough')

    def startWaitForEnough(self, data):
        pass

    def finishWaitForEnough(self):
        pass

    def startWaitToStart(self, data):
        def advance(task):
            self.fsm.request('WaitClientsReady')
            self.d_setState('Rules')
            return task.done

        taskMgr.doMethodLater(self.startDelay, advance, self.taskName('dostart'))

    def finishWaitToStart(self):
        taskMgr.remove(self.taskName('dostart'))

    def __doStart(self, task = None):
        self.b_setState('Active')
        if task: return task.done

    def startWaitClientsReady(self):
        self.responses = set()
        taskMgr.doMethodLater(15, self.__doStart, self.taskName('clientready'))

    def finishWaitClientsReady(self):
        taskMgr.remove(self.taskName('clientready'))

    def toonReady(self):
        self.responses.add(self.air.getAvatarIdFromSender())
        if self.responses == set(self.toonsPlaying):
            self.__doStart()

    def startActive(self, data):
        taskMgr.doMethodLater(self.getDuration(), self.__finish, self.taskName('finish'))

    def finishActive(self):
        taskMgr.remove(self.taskName('finish'))

    def __finish(self, task):
        self.calcReward()
        self.b_setState('Conclusion')
        return task.done

    def calcReward(self):
        raise NotImplementedError('calcReward() -- pure virtual')

    def startConclusion(self, data):
        raise NotImplementedError('startConclusion() -- pure virtual')

    def finishConclusion(self):
        raise NotImplementedError('finishConclusion() -- pure virtual')

