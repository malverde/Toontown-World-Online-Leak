from direct.distributed.ClockDelta import *
from direct.directnotify import DirectNotifyGlobal
import DistributedSwitchBase
from direct.task import Task
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from otp.level import DistributedEntityAI

class DistributedSwitchAI(DistributedSwitchBase.DistributedSwitchBase, DistributedEntityAI.DistributedEntityAI):

    def __init__(self, level, entId, zoneId = None):
        DistributedEntityAI.DistributedEntityAI.__init__(self, level, entId)
        self.fsm = ClassicFSM.ClassicFSM('DistributedSwitch', [State.State('off', self.enterOff, self.exitOff, ['playing']), State.State('aTTWact', self.enterATTWact, self.exitATTWact, ['playing']), State.State('playing', self.enterPlaying, self.exitPlaying, ['aTTWact'])], 'off', 'off')
        self.fsm.enterInitialState()
        self.avatarId = 0
        self.doLaterTask = None
        if zoneId is not None:
            self.generateWithRequired(zoneId)
        return

    def setup(self):
        pass

    def takedown(self):
        pass

    setScale = DistributedSwitchBase.stubFunction

    def delete(self):
        if self.doLaterTask:
            self.doLaterTask.remove()
            self.doLaterTask = None
        del self.fsm
        DistributedEntityAI.DistributedEntityAI.delete(self)
        return

    def getAvatarInteract(self):
        return self.avatarId

    def getState(self):
        r = [self.fsm.getCurrentState().getName(), globalClockDelta.getRealNetworkTime()]
        return r

    def sendState(self):
        self.sendUpdate('setState', self.getState())

    def setIsOn(self, isOn):
        if self.isOn != isOn:
            self.isOn = isOn
            stateName = self.fsm.getCurrentState().getName()
            if isOn:
                if stateName != 'playing':
                    self.fsm.request('playing')
            elif stateName != 'aTTWact':
                self.fsm.request('aTTWact')
            messenger.send(self.getOutputEventName(), [isOn])

    def getIsOn(self):
        return self.isOn

    def getName(self):
        return 'switch-%s' % (self.entId,)

    def switchOffTask(self, task):
        self.setIsOn(0)
        self.fsm.request('aTTWact')
        return Task.done

    def requestInteract(self):
        avatarId = self.air.getAvatarIdFromSender()
        stateName = self.fsm.getCurrentState().getName()
        if stateName != 'playing':
            self.sendUpdate('setAvatarInteract', [avatarId])
            self.avatarId = avatarId
            self.fsm.request('playing')
        else:
            self.sendUpdateToAvatarId(avatarId, 'rejectInteract', [])

    def requestExit(self):
        avatarId = self.air.getAvatarIdFromSender()
        if self.avatarId and avatarId == self.avatarId:
            stateName = self.fsm.getCurrentState().getName()
            if stateName == 'playing':
                self.sendUpdate('avatarExit', [avatarId])
                self.avatarId = None
                if self.isOn and self.secondsOn != -1.0 and self.secondsOn >= 0.0:
                    self.doLaterTask = taskMgr.doMethodLater(self.secondsOn, self.switchOffTask, self.uniqueName('switch-timer'))
        return

    def enterOff(self):
        pass

    def exitOff(self):
        pass

    def enterATTWact(self):
        self.sendState()

    def exitATTWact(self):
        pass

    def enterPlaying(self):
        self.sendState()
        self.setIsOn(1)

    def exitPlaying(self):
        if self.doLaterTask:
            self.doLaterTask.remove()
            self.doLaterTask = None
        return

    if __dev__:

        def aTTWibChanged(self, aTTWib, value):
            self.takedown()
            self.setup()
