from toontown.hood import HoodAI
from toontown.toonbase import ToontownGlobals
from toontown.distributed.DistributedTimerAI import DistributedTimerAI
from toontown.classicchars import DistributedChipAI
from toontown.classicchars import DistributedDaleAI
from toontown.dna.DNAParser import DNAGroup, DNAVisGroup
from toontown.safezone.DistributedPicnicBasketAI import DistributedPicnicBasketAI
from toontown.safezone import DistributedGameTableAI
from toontown.hood import ZoneUtil


class OZHoodAI(HoodAI.HoodAI):
    def __init__(self, air):
        HoodAI.HoodAI.__init__(self, air,
                               ToontownGlobals.OutdoorZone,
                               ToontownGlobals.OutdoorZone)

        self.timer = None
        self.classicCharChip = None
        self.classicCharDale = None
        self.picnicTables = []
        self.gameTables = []

        self.startup()

    def startup(self):
        HoodAI.HoodAI.startup(self)

        self.createTimer()
        if simbase.config.GetBool('want-classic-chars', True):
            if simbase.config.GetBool('want-chip-and-dale', True):
                self.createClassicChars()
        self.createPicnicTables()
        if simbase.config.GetBool('want-game-tables', True):
            self.createGameTables()

    def createTimer(self):
        self.timer = DistributedTimerAI(self.air)
        self.timer.generateWithRequired(self.zoneId)

    def createClassicChars(self):
        self.classicCharChip = DistributedChipAI.DistributedChipAI(self.air)
        self.classicCharChip.generateWithRequired(self.zoneId)
        self.classicCharChip.start()
        self.classicCharDale = DistributedDaleAI.DistributedDaleAI(self.air, self.classicCharChip.doId)
        self.classicCharDale.generateWithRequired(self.zoneId)
        self.classicCharDale.start()
        self.classicCharChip.setDaleId(self.classicCharDale.doId)

    def findPicnicTables(self, dnaGroup, zoneId, area, overrideDNAZone=False):
        picnicTables = []
        if isinstance(dnaGroup, DNAGroup) and ('picnic_table' in dnaGroup.getName()):
            nameInfo = dnaGroup.getName().split('_')
            for i in xrange(dnaGroup.getNumChildren()):
                childDnaGroup = dnaGroup.at(i)
                if 'picnic_table' in childDnaGroup.getName():
                    pos = childDnaGroup.getPos()
                    hpr = childDnaGroup.getHpr()
                    picnicTable = DistributedPicnicBasketAI(
                        simbase.air, nameInfo[2],
                        pos[0], pos[1], pos[2], hpr[0], hpr[1], hpr[2])
                    picnicTable.generateWithRequired(zoneId)
                    picnicTables.append(picnicTable)
        elif isinstance(dnaGroup, DNAVisGroup) and (not overrideDNAZone):
            zoneId = ZoneUtil.getTrueZoneId(int(dnaGroup.getName().split(':')[0]), zoneId)
        for i in xrange(dnaGroup.getNumChildren()):
            foundPicnicTables = self.findPicnicTables(
                dnaGroup.at(i), zoneId, area, overrideDNAZone=overrideDNAZone)
            picnicTables.extend(foundPicnicTables)
        return picnicTables

    def createPicnicTables(self):
        self.picnicTables = []
        for zoneId in self.getZoneTable():
            dnaData = self.air.dnaDataMap.get(zoneId, None)
            zoneId = ZoneUtil.getTrueZoneId(zoneId, self.zoneId)
            if dnaData.getName() == 'root':
                area = ZoneUtil.getCanonicalZoneId(zoneId)
                foundPicnicTables = self.findPicnicTables(
                    dnaData, zoneId, area, overrideDNAZone=True)
                self.picnicTables.extend(foundPicnicTables)
        for picnicTable in self.picnicTables:
            picnicTable.start()

    def findGameTables(self, dnaGroup, zoneId, area, overrideDNAZone=False):
        gameTables = []
        if isinstance(dnaGroup, DNAGroup) and ('game_table' in dnaGroup.getName()):
            for i in xrange(dnaGroup.getNumChildren()):
                childDnaGroup = dnaGroup.at(i)
                if 'game_table' in childDnaGroup.getName():
                    pos = childDnaGroup.getPos()
                    hpr = childDnaGroup.getHpr()
                    gameTable = DistributedGameTableAI.DistributedGameTableAI(simbase.air)
                    gameTable.setPosHpr(pos[0], pos[1], pos[2], hpr[0], hpr[1], hpr[2])
                    gameTable.generateWithRequired(zoneId)
        elif isinstance(dnaGroup, DNAVisGroup) and (not overrideDNAZone):
            zoneId = ZoneUtil.getTrueZoneId(int(dnaGroup.getName().split(':')[0]), zoneId)
        for i in xrange(dnaGroup.getNumChildren()):
            foundGameTables = self.findGameTables(
                dnaGroup.at(i), zoneId, area, overrideDNAZone=overrideDNAZone)
            gameTables.extend(foundGameTables)
        return gameTables

    def createGameTables(self):
        self.gameTables = []
        for zoneId in self.getZoneTable():
            dnaData = self.air.dnaDataMap.get(zoneId, None)
            zoneId = ZoneUtil.getTrueZoneId(zoneId, self.zoneId)
            if dnaData.getName() == 'root':
                area = ZoneUtil.getCanonicalZoneId(zoneId)
                foundGameTables = self.findGameTables(
                    dnaData, zoneId, area, overrideDNAZone=True)
                self.gameTables.extend(foundGameTables)
