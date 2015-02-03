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
class SuitLegList:
    def __init__(self, path, dnaStore):
        self.path = path
        self.dnaStore = dnaStore

        self.legs = []

        # First, add the initial SuitLeg:
        self.add(self.path.getPoint(0), self.path.getPoint(1), self.getFirstLegType())

        # Next, connect each of the points in our path through SuitLegs:
        for i in xrange(self.path.getNumPoints() - 1):
            pointA = self.path.getPoint(i)
            pointB = self.path.getPoint(i + 1)
            pointTypeA = pointA.getPointType()
            pointTypeB = pointB.getPointType()
            legType = self.getLegType(pointTypeA, pointTypeB)

            if pointTypeA == DNASuitPoint.COGHQ_OUT_POINT:
                # We're going out of a door, so we'll need to insert a door
                # leg before the move:
                self.add(pointA, pointB, SuitLeg.TFromCogHQ)

            self.add(pointA, pointB, legType)

            if pointTypeB == DNASuitPoint.COGHQ_IN_POINT:
                # We're going into a door, so we'll need to insert a door leg
                # after the move:
                self.add(pointA, pointB, SuitLeg.TToCogHQ)

        # Add the last SuitLeg:
        numPoints = self.path.getNumPoints()
        pointA = self.path.getPoint(numPoints - 2)
        pointB = self.path.getPoint(numPoints - 1)
        self.add(pointA, pointB, self.getLastLegType())

        # Finally, take down the suit:
        self.add(pointA, pointB, SuitLeg.TOff)

    def add(self, pointA, pointB, legType):
        zoneId = self.dnaStore.getSuitEdgeZone(pointA.getIndex(), pointB.getIndex())
        landmarkBuildingIndex = pointB.getLandmarkBuildingIndex()
        if landmarkBuildingIndex == -1:
            landmarkBuildingIndex = pointA.getLandmarkBuildingIndex()
        startTime = 0.0
        if len(self.legs) > 0:
            startTime = self.legs[-1].getEndTime()
        leg = SuitLeg(startTime, zoneId, landmarkBuildingIndex, pointA, pointB, legType)
        self.legs.append(leg)

    def getFirstLegType(self):
        if self.path.getPoint(0).getPointType() == DNASuitPoint.SIDE_DOOR_POINT:
            return SuitLeg.TFromSuitBuilding
        else:
            return SuitLeg.TFromSky

    def getLegType(self, pointTypeA, pointTypeB):
        if pointTypeA in (DNASuitPoint.FRONT_DOOR_POINT,
                          DNASuitPoint.SIDE_DOOR_POINT):
            return SuitLeg.TWalkToStreet
        if pointTypeB in (DNASuitPoint.FRONT_DOOR_POINT,
                          DNASuitPoint.SIDE_DOOR_POINT):
            return SuitLeg.TWalkFromStreet
        return SuitLeg.TWalk

    def getLastLegType(self):
        endPoint = self.path.getPoint(self.path.getNumPoints() - 1)
        endPointType = endPoint.getPointType()
        if endPointType == DNASuitPoint.FRONT_DOOR_POINT:
            return SuitLeg.TToToonBuilding
        if endPointType == DNASuitPoint.SIDE_DOOR_POINT:
            return SuitLeg.TToSuitBuilding
        return SuitLeg.TToSky

    def getNumLegs(self):
        return len(self.legs)

    def getLeg(self, index):
        return self.legs[index]

    def getType(self, index):
        return self.legs[index].getType()

    def getLegTime(self, index):
        return self.legs[index].getLegTime()

    def getZoneId(self, index):
        return self.legs[index].getZoneId()

    def getBlockNumber(self, index):
        return self.legs[index].getBlockNumber()

    def getPointA(self, index):
        return self.legs[index].getPointA()

    def getPointB(self, index):
        return self.legs[index].getPointB()

    def getStartTime(self, index):
        return self.legs[index].getStartTime()

    def getLegIndexAtTime(self, time, startLegIndex):
        for i, leg in enumerate(self.legs):
            if leg.getEndTime() > time:
                break
        return i

    def isPointInRange(self, point, lowTime, highTime):
        legIndex = self.getLegIndexAtTime(lowTime, 0)
        while legIndex < self.getNumLegs():
            leg = self.legs[legIndex]
            if leg.getEndTime() > highTime:
                break
            if (leg.pointA == point) or (leg.pointB == point):
                return True
            legIndex += 1
        return False
