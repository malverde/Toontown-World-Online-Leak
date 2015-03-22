from pandac.PandaModules import *
from toontown.dna.DNAParser import DNAGroup, DNAVisGroup
from toontown.hood import HoodAI
from toontown.hood import ZoneUtil
from toontown.safezone.DistributedGolfKartAI import DistributedGolfKartAI
from toontown.toonbase import ToontownGlobals


class GZHoodAI(HoodAI.HoodAI):
    def __init__(self, air):
        HoodAI.HoodAI.__init__(self, air,
                               ToontownGlobals.GolfZone,
                               ToontownGlobals.GolfZone)

        self.golfKarts = []

        self.startup()

    def startup(self):
        HoodAI.HoodAI.startup(self)

        self.createGolfKarts()

    def findGolfKarts(self, dnaGroup, zoneId, area, overrideDNAZone=False):
        golfKarts = []
        if isinstance(dnaGroup, DNAGroup) and ('golf_kart' in dnaGroup.getName()):
            nameInfo = dnaGroup.getName().split('_')
            golfCourse = int(nameInfo[2])
            for i in xrange(dnaGroup.getNumChildren()):
                childDnaGroup = dnaGroup.at(i)
                if 'starting_block' in childDnaGroup.getName():
                    pos = childDnaGroup.getPos()
                    hpr = childDnaGroup.getHpr()
                    golfKart = DistributedGolfKartAI(
                        self.air, golfCourse,
                        pos[0], pos[1], pos[2], hpr[0], hpr[1], hpr[2])
                    golfKart.generateWithRequired(zoneId)
                    golfKarts.append(golfKart)
        elif isinstance(dnaGroup, DNAVisGroup) and (not overrideDNAZone):
            zoneId = ZoneUtil.getTrueZoneId(int(dnaGroup.getName().split(':')[0]), zoneId)
        for i in xrange(dnaGroup.getNumChildren()):
            foundGolfKarts = self.findGolfKarts(dnaGroup.at(i), zoneId, area, overrideDNAZone=overrideDNAZone)
            golfKarts.extend(foundGolfKarts)
        return golfKarts

    def createGolfKarts(self):
        self.golfKarts = []
        for zoneId in self.getZoneTable():
            dnaData = self.air.dnaDataMap.get(zoneId, None)
            zoneId = ZoneUtil.getTrueZoneId(zoneId, self.zoneId)
            if dnaData.getName() == 'root':
                area = ZoneUtil.getCanonicalZoneId(zoneId)
                foundGolfKarts = self.findGolfKarts(dnaData, zoneId, area, overrideDNAZone=True)
                self.golfKarts.extend(foundGolfKarts)
        for golfKart in self.golfKarts:
            golfKart.start()
