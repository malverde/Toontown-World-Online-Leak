#from toontown.election.DistributedElectionEventAI import DistributedElectionEventAI
from toontown.hood import HoodAI
from toontown.safezone import ButterflyGlobals
from toontown.safezone import DistributedButterflyAI
from toontown.safezone import DistributedTrolleyAI
from toontown.toon import NPCToons
from toontown.toonbase import TTLocalizer
from toontown.toonbase import ToontownGlobals
from toontown.ai import DistributedTrickOrTreatTargetAI
from toontown.ai import DistributedWinterCarolingTargetAI


class TTHoodAI(HoodAI.HoodAI):
    def __init__(self, air):
        HoodAI.HoodAI.__init__(self, air,
                               ToontownGlobals.ToontownCentral,
                               ToontownGlobals.ToontownCentral)

        self.trolley = None

        self.startup()

    def startup(self):
        HoodAI.HoodAI.startup(self)

        if simbase.config.GetBool('want-minigames', True):
            self.createTrolley()
        if simbase.config.GetBool('want-butterflies', True):
            self.createButterflies()
        if self.air.config.GetBool('want-doomsday', False):
            self.spawnElection()
            
                
        if simbase.air.wantHalloween:
            self.TrickOrTreatTargetManager = DistributedTrickOrTreatTargetAI.DistributedTrickOrTreatTargetAI(self.air)
            self.TrickOrTreatTargetManager.generateWithRequired(2649)
        
        if simbase.air.wantChristmas:
            self.WinterCarolingTargetManager = DistributedWinterCarolingTargetAI.DistributedWinterCarolingTargetAI(self.air)
            self.WinterCarolingTargetManager.generateWithRequired(2659)

    def shutdown(self):
        HoodAI.HoodAI.shutdown(self)

        ButterflyGlobals.clearIndexes(self.zoneId)
        
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
                taskMgr.doMethodLater(10, election.b_setState, 'election-start-delay', extraArgs=['Event'])
        if not election:
            # Create a new election object.
            election = DistributedElectionEventAI(self.air)
            election.generateWithRequired(self.HOOD)
            election.b_setState('Idle')
            # Start the election after a 10 second delay.
            taskMgr.doMethodLater(10, election.b_setState, 'election-start-delay', extraArgs=['Event'])
        return task.again

    def createTrolley(self):
        self.trolley = DistributedTrolleyAI.DistributedTrolleyAI(self.air)
        self.trolley.generateWithRequired(self.zoneId)
        self.trolley.start()

    def createButterflies(self):
        playground = ButterflyGlobals.TTC
        for area in range(ButterflyGlobals.NUM_BUTTERFLY_AREAS[playground]):
            for b in range(ButterflyGlobals.NUM_BUTTERFLIES[playground]):
                butterfly = DistributedButterflyAI.DistributedButterflyAI(self.air)
                butterfly.setArea(playground, area)
                butterfly.setState(0, 0, 0, 1, 1)
                butterfly.generateWithRequired(self.zoneId)
                self.butterflies.append(butterfly)
