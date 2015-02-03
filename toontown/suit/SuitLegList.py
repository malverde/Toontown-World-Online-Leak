from toontown.toonbase import ToontownGlobals
import SuitTimings
from toontown.dna import DNAStoreSuitPoint


class SuitLeg:
    TWalkFromStreet = 0
    TWalkToStreet = 1
    TWalk = 2
    TFromSky = 3
    TToSky = 4
    TFromSuitBuilding = 5
    TToSuitBuilding = 6
    TToToonBuilding = 7
    TFromCoghq = 8
    TToCoghq = 9
    TOff = 10
    TypeToName = {
      0 : 'WalkFromStreet',
      1 : 'WalkToStreet',
      2 : 'Walk',
      3 : 'FromSky',
      4 : 'ToSky',
      5 : 'FromSuitBuilding',
      6 : 'ToSuitBuilding',
      7 : 'ToToonBuilding',
      8 : 'FromCoghq',
      9 : 'ToCoghq',
      10 : 'Off'
    }
    def __init__(self, suitGraph, pointA, pointB, type):
        self.suitGraph = suitGraph
        self.pointA = pointA
        self.pointB = pointB
        self.posA = pointA.getPos()
        self.posB = pointB.getPos()
        self.type = type

    def getLegTime(self):
        if self.type in (SuitLeg.TWalk, SuitLeg.TWalkFromStreet,
                         SuitLeg.TWalkToStreet):
            return (self.posA-self.posB).length()/ToontownGlobals.SuitWalkSpeed
        elif self.type == SuitLeg.TFromSky:
            return SuitTimings.fromSky
        elif self.type == SuitLeg.TToSky:
            return SuitTimings.toSky
        elif self.type == SuitLeg.TFromSuitBuilding:
            return SuitTimings.fromSuitBuilding
        elif self.type == SuitLeg.TToSuitBuilding:
            return SuitTimings.toSuitBuilding
        elif self.type == SuitLeg.TToToonBuilding:
            return SuitTimings.toToonBuilding
        else:
            return SuitTimings.toToonBuilding

    def getPosA(self):
        return self.posA

    def getPosB(self):
        return self.posB

    def getPosAtTime(self, time):
        if self.type in (SuitLeg.TFromSky, SuitLeg.TFromSuitBuilding,
                         SuitLeg.TFromCoghq):
            return self.getPosA()
        elif self.type in (SuitLeg.TToSky, SuitLeg.TToSuitBuilding,
                           SuitLeg.TToToonBuilding, SuitLeg.TToCoghq,
                           SuitLeg.TOff):
            return self.getPosB()

        fraction = time/self.getLegTime()
        fraction = min(max(fraction, 0.0), 1.0)

        delta = self.getPosB()-self.getPosA()
        pos = self.getPosA() + delta*(time/self.getLegTime())

        return pos

    def getZone(self):
        return self.suitGraph.getEdgeZone(self.suitGraph.getConnectingEdge(self.pointA, self.pointB))

    def getBlockNumber(self):
        block = self.pointB.getLandmarkBuildingIndex()
        if block is not None:
            return block
        else:
            return self.pointA.getLandmarkBuildingIndex()

    @staticmethod
    def getTypeName(type):
        return SuitLeg.TypeToName[type]

    def getType(self):
        return self.type
