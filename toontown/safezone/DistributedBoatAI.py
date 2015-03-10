from direct.distributed import DistributedObjectAI
from direct.distributed.ClockDelta import *
from direct.fsm import ClassicFSM, State
from otp.ai.AIBase import *
from toontown.toonbase.ToontownGlobals import *


class DistributedBoatAI(DistributedObjectAI.DistributedObjectAI):

    def __init__(self, air):
        DistributedObjectAI.DistributedObjectAI.__init__(self, air)
        self.fsm = ClassicFSM.ClassicFSM(
            'DistributedBoatAI',
            [
                State.State('off', self.enterOff, self.exitOff,
                            ['DockedEast']),
                State.State('DockedEast', self.enterDockedEast, self.exitDockedEast,
                            ['SailingWest']),
                State.State('SailingWest', self.enterSailingWest, self.exitSailingWest,
                            ['DockedWest']),
                State.State('DockedWest', self.enterDockedWest, self.exitDockedWest,
                            ['SailingEast']),
                State.State('SailingEast', self.enterSailingEast, self.exitSailingEast,
                            ['DockedEast'])
            ], 'off', 'off')
        self.fsm.enterInitialState()

    def delete(self):
        self.fsm.request('off')
        DistributedObjectAI.DistributedObjectAI.delete(self)

    def b_setState(self, state):
        self.sendUpdate('setState', [state, globalClockDelta.getRealNetworkTime()])
        self.fsm.request(state)

    def getState(self):
        return [self.fsm.getCurrentState().getName(), globalClockDelta.getRealNetworkTime()]

    def start(self):
        self.b_setState('DockedEast')

    def enterOff(self):
        pass

    def exitOff(self):
        pass

    def enterDockedEast(self):
        taskMgr.doMethodLater(10.0, self.__departEast, 'depart-east')

    def exitDockedEast(self):
        taskMgr.remove('depart-east')

    def __departEast(self, task):
        self.b_setState('SailingWest')
        return Task.done

    def enterSailingWest(self):
        taskMgr.doMethodLater(20.0, self.__dockWest, 'dock-west')

    def exitSailingWest(self):
        taskMgr.remove('dock-west')

    def __dockWest(self, task):
        self.b_setState('DockedWest')
        return Task.done

    def enterDockedWest(self):
        taskMgr.doMethodLater(10.0, self.__departWest, 'depart-west')

    def exitDockedWest(self):
        taskMgr.remove('depart-west')

    def __departWest(self, task):
        self.b_setState('SailingEast')
        return Task.done

    def enterSailingEast(self):
        taskMgr.doMethodLater(20.0, self.__dockEast, 'dock-east')

    def exitSailingEast(self):
        taskMgr.remove('dock-east')

    def __dockEast(self, task):
        self.b_setState('DockedEast')
        return Task.done
