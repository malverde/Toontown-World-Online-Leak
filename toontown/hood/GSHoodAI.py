from toontown.classicchars import DistributedGoofySpeedwayAI
from toontown.dna.DNAParser import DNAGroup, DNAVisGroup
from toontown.hood import HoodAI
from toontown.hood import ZoneUtil
from toontown.racing import RaceGlobals
from toontown.racing.DistributedRacePadAI import DistributedRacePadAI
from toontown.racing.DistributedStartingBlockAI import DistributedStartingBlockAI
from toontown.racing.DistributedViewPadAI import DistributedViewPadAI
from toontown.racing.DistributedStartingBlockAI import DistributedViewingBlockAI
from toontown.toonbase import ToontownGlobals


class GSHoodAI(HoodAI.HoodAI):
    def __init__(self, air):
        HoodAI.HoodAI.__init__(self, air,
                               ToontownGlobals.GoofySpeedway,
                               ToontownGlobals.GoofySpeedway)

        self.racingPads = []
        self.viewingPads = []
        self.viewingBlocks = []
        self.startingBlocks = []
        self.leaderBoards = []
        self.classicChar = None
        self.zoneId = None

        self.startup()

    def startup(self):
        HoodAI.HoodAI.startup(self)

        self.createStartingBlocks()
        self.createLeaderBoards()
        self.cycleLeaderBoards()
        if simbase.config.GetBool('want-goofy', True):
            self.createClassicChar()

    def shutdown(self):
        HoodAI.HoodAI.shutdown(self)

        taskMgr.removeTasksMatching('leaderBoardSwitch')
        for board in self.leaderBoards:
            board.delete()
        del self.leaderBoards

    def findRacingPads(self, dnaGroup, zoneId, area, padType='racing_pad'):
        racingPads = []
        racingPadGroups = []
        if isinstance(dnaGroup, DNAGroup) and (padType in dnaGroup.getName()):
            racingPadGroups.append(dnaGroup)

            if padType == 'racing_pad':
                nameInfo = dnaGroup.getName().split('_')
                racingPad = DistributedRacePadAI(simbase.air)
                racingPad.setArea(zoneId)
                racingPad.nameType = nameInfo[3]
                racingPad.index = int(nameInfo[2])
                nextRaceInfo = RaceGlobals.getNextRaceInfo(-1, racingPad.nameType, racingPad.index)
                racingPad.setTrackInfo([nextRaceInfo[0], nextRaceInfo[1]])
                racingPad.generateWithRequired(zoneId)
            elif padType == 'viewing_pad':
                racingPad = DistributedViewPadAI(simbase.air)
                racingPad.setArea(zoneId)
                racingPad.generateWithRequired(zoneId)
            else:
                self.notify.error('Invalid racing pad type: ' + padType)

            racingPads.append(racingPad)
        elif isinstance(dnaGroup, DNAVisGroup):
            zoneId = ZoneUtil.getTrueZoneId(int(dnaGroup.getName().split(':')[0]), zoneId)
        for i in xrange(dnaGroup.getNumChildren()):
            (foundRacingPads, foundRacingPadGroups) = self.findRacingPads(dnaGroup.at(i), zoneId, area, padType=padType)
            racingPads.extend(foundRacingPads)
            racingPadGroups.extend(foundRacingPadGroups)
        return (racingPads, racingPadGroups)

    def findStartingBlocks(self, dnaGroup, racePad):
        startingBlocks = []
        if isinstance(dnaGroup, DNAGroup) and ('starting_block' in dnaGroup.getName()):
            x, y, z = dnaGroup.getPos()
            h, p, r = dnaGroup.getHpr()
            if isinstance(racePad, DistributedRacePadAI):
                startingBlock = DistributedStartingBlockAI(simbase.air)
            elif isinstance(racePad, DistributedViewPadAI):
                startingBlock = DistributedViewingBlockAI(simbase.air)
            else:
                self.notify.error('Unknown starting block type.')
            startingBlock.setPosHpr(x, y, z, h, p, r)
            startingBlock.setPadDoId(racePad.doId)
            startingBlock.setPadLocationId(getattr(racePad, 'index', 0))
            startingBlock.generateWithRequired(racePad.zoneId)

            startingBlocks.append(startingBlock)
        for i in xrange(dnaGroup.getNumChildren()):
            foundStartingBlocks = self.findStartingBlocks(dnaGroup.at(i), racePad)
            startingBlocks.extend(foundStartingBlocks)
        return startingBlocks

    def createStartingBlocks(self):
        self.racingPads = []
        self.viewingPads = []
        racingPadGroups = []
        viewingPadGroups = []
        for zoneId in self.getZoneTable():
            dnaData = self.air.dnaDataMap.get(zoneId, None)
            zoneId = ZoneUtil.getTrueZoneId(zoneId, self.zoneId)
            if dnaData.getName() == 'root':
                area = ZoneUtil.getCanonicalZoneId(zoneId)
                (foundRacingPads, foundRacingPadGroups) = self.findRacingPads(dnaData, zoneId, area, padType='racing_pad')
                (foundViewingPads, foundViewingPadGroups) = self.findRacingPads(dnaData, zoneId, area, padType='viewing_pad')
                self.racingPads.extend(foundRacingPads)
                racingPadGroups.extend(foundRacingPadGroups)
                self.viewingPads.extend(foundViewingPads)
                viewingPadGroups.extend(foundViewingPadGroups)
        self.startingBlocks = []
        for (dnaGroup, racePad) in zip(racingPadGroups, self.racingPads):
            foundStartingBlocks = self.findStartingBlocks(dnaGroup, racePad)
            self.startingBlocks.extend(foundStartingBlocks)
            for startingBlock in foundStartingBlocks:
                racePad.addStartingBlock(startingBlock)
        self.viewingBlocks = []
        for (dnaGroup, viewPad) in zip(viewingPadGroups, self.viewingPads):
            foundViewingBlocks = self.findStartingBlocks(dnaGroup, viewPad)
            self.viewingBlocks.extend(foundViewingBlocks)
            for viewingBlock in foundViewingBlocks:
                viewPad.addStartingBlock(viewingBlock)

    def findLeaderBoards(self, dnaData, zoneId):
        return []  # TODO

    def createLeaderBoards(self):
        self.leaderBoards = []
        dnaData = self.air.dnaDataMap[self.zoneId]
        if dnaData.getName() == 'root':
            self.leaderBoards = self.findLeaderBoards(dnaData, self.zoneId)
        for leaderBoard in self.leaderBoards:
            if not leaderBoard:
                continue
            if 'city' in leaderBoard.getName():
                leaderBoardType = 'city'
            elif 'stadium' in leaderBoard.getName():
                leaderBoardType = 'stadium'
            elif 'country' in leaderBoard.getName():
                leaderBoardType = 'country'
            for subscription in RaceGlobals.LBSubscription[leaderBoardType]:
                leaderBoard.subscribeTo(subscription)

    def cycleLeaderBoards(self, task=None):
        messenger.send('leaderBoardSwap-' + str(self.zoneId))
        taskMgr.doMethodLater(10, self.cycleLeaderBoards, 'leaderBoardSwitch')

    def createClassicChar(self):
        self.classicChar = DistributedGoofySpeedwayAI.DistributedGoofySpeedwayAI(self.air)
        self.classicChar.generateWithRequired(self.zoneId)
        self.classicChar.start()
