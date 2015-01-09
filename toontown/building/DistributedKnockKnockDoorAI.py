from otp.ai.AIBaseGlobal import *
from direct.distributed.ClockDelta import *
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import ClassicFSM
import DistributedAnimatedPropAI
from direct.task.Task import Task
from direct.fsm import State

class DistributedKnockKnockDoorAI(DistributedAnimatedPropAI.DistributedAnimatedPropAI):

    def __init__(self, air, propId):
        DistributedAnimatedPropAI.DistributedAnimatedPropAI.__init__(self, air, propId)
        self.fsm.setName('DistributedKnockKnockDoor')
        self.propId = propId
        self.doLaterTask = None
        return

    def delete(self):
        DistributedAnimatedPropAI.DistributedAnimatedPropAI.delete(self)

    def enterOff(self):
        DistributedAnimatedPropAI.DistributedAnimatedPropAI.enterOff(self)

    def exitOff(self):
        DistributedAnimatedPropAI.DistributedAnimatedPropAI.exitOff(self)

    def aTTWactTask(self, task):
        self.fsm.request('aTTWact')
        return Task.done

    def enterATTWact(self):
        DistributedAnimatedPropAI.DistributedAnimatedPropAI.enterATTWact(self)

    def exitATTWact(self):
        DistributedAnimatedPropAI.DistributedAnimatedPropAI.exitATTWact(self)

    def enterPlaying(self):
        DistributedAnimatedPropAI.DistributedAnimatedPropAI.enterPlaying(self)
        self.doLaterTask = taskMgr.doMethodLater(9, self.aTTWactTask, self.uniqueName('knockKnock-timer'))

    def exitPlaying(self):
        DistributedAnimatedPropAI.DistributedAnimatedPropAI.exitPlaying(self)
        taskMgr.remove(self.doLaterTask)
        self.doLaterTask = None
        return
