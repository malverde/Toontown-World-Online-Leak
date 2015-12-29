from toontown.toonbase import ToontownGlobals
from SZHoodAI import SZHoodAI
from toontown.safezone import ButterflyGlobals
from toontown.safezone.DistributedButterflyAI import DistributedButterflyAI
from toontown.toon import NPCToons
#from toontown.election.DistributedElectionEventAI import DistributedElectionEventAI
from direct.task import Task
import time
from toontown.ai import DistributedTrickOrTreatTargetAI
from toontown.ai import DistributedWinterCarolingTargetAI
import datetime


class TTHoodAI(SZHoodAI):
    HOOD = ToontownGlobals.ToontownCentral

    def createZone(self):
        SZHoodAI.createZone(self)
        self.spawnObjects()
        self.butterflies = []
        self.createButterflies()

        if self.air.config.GetBool('want-doomsday', False):
            self.spawnElection()
		day = str(datetime.datetime.now().strftime("%d"))
		
        if str(datetime.datetime.now().strftime("%m")) == "12" and day == "14" or day == "15" or day == "16" or day == "17" or day == "18" or day == "19" or day == "20" or day == "21" or day == "22" or day == "23" or day == "24" or day == "25" or day == "26" or day == "27" or "28" or day == "29" or day == "30" or day == "31":
            self.WinterCarolingTargetManager = DistributedWinterCarolingTargetAI.DistributedWinterCarolingTargetAI(self.air)
            self.WinterCarolingTargetManager.generateWithRequired(2659)
            
        elif str(datetime.datetime.now().strftime("%m")) == "1" and day == "2" or day == "3" or day == "4":
            self.WinterCarolingTargetManager = DistributedWinterCarolingTargetAI.DistributedWinterCarolingTargetAI(self.air)
            self.WinterCarolingTargetManager.generateWithRequired(2659)
            
        elif str(datetime.datetime.now().strftime("%m")) == "10" and day ==  "21" or day == "22" or day == "23" or day == "25" or day == "26" or day == "27" or day == "28" or day == "29" or day == "30" or day == "31":
            self.TrickOrTreatTargetManager = DistributedTrickOrTreatTargetAI.DistributedTrickOrTreatTargetAI(self.air)
            self.TrickOrTreatTargetManager.generateWithRequired(2649)
            
        elif str(datetime.datetime.now().strftime("%m")) == "11" and day ==  "1":
            self.TrickOrTreatTargetManager = DistributedTrickOrTreatTargetAI.DistributedTrickOrTreatTargetAI(self.air)
            self.TrickOrTreatTargetManager.generateWithRequired(2649)

    def spawnElection(self):
        election = self.air.doFind('ElectionEvent')
        if election is None:
            election = DistributedElectionEventAI(self.air)
            election.generateWithRequired(self.HOOD)
        election.b_setState('Idle')
        if self.air.config.GetBool('want-hourly-doomsday', False):
            self.__startElectionTick()

    def __startElectionTick(self):
        # Check seconds until next hour.
        ts = time.time()
        nextHour = 3600 - (ts % 3600)
        taskMgr.doMethodLater(nextHour, self.__electionTick, 'election-hourly')

    def __electionTick(self, task):
        # The next tick will occur in exactly an hour.
        task.delayTime = 3600
        # Check if we have toons in TTC...
        toons = self.air.doFindAll('DistributedToon')
        if not toons:
            # There are no toons online, just wait for the next hour.
            return task.again
        # Is there an invasion currently running?
        election = self.air.doFind('ElectionEvent')
        if election:
            state = election.getState()
            if state[0] == 'Idle':
                # There's already an Idle invasion, start it!
                taskMgr.doMethodLater(
                    10,
                    election.b_setState,
                    'election-start-delay',
                    extraArgs=['Event'])
        if not election:
            # Create a new election object.
            election = DistributedElectionEventAI(self.air)
            election.generateWithRequired(self.HOOD)
            election.b_setState('Idle')
            # Start the election after a 10 second delay.
            taskMgr.doMethodLater(
                10,
                election.b_setState,
                'election-start-delay',
                extraArgs=['Event'])
        return task.again

    def createButterflies(self):
        playground = ButterflyGlobals.TTC
        for area in range(ButterflyGlobals.NUM_BUTTERFLY_AREAS[playground]):
            for b in range(ButterflyGlobals.NUM_BUTTERFLIES[playground]):
                butterfly = DistributedButterflyAI(self.air)
                butterfly.setArea(playground, area)
                butterfly.setState(0, 0, 0, 1, 1)
                butterfly.generateWithRequired(self.HOOD)
                self.butterflies.append(butterfly)
