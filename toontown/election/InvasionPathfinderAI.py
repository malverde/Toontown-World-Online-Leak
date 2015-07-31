#Embedded file name: toontown.election.InvasionPathfinderAI
import bisect
import math
from pandac.PandaModules import *

class InvasionPathfinderAI:
    VERTEX_EXTRUSION = 0.15

    def __init__(self, polygons = None):
        self.borders = []
        self.vertices = []
        if polygons:
            for polygon in polygons:
                self.addPolygon(polygon)

            self.buildNeighbors()

    def addPolygon(self, points):
        newVertices = []
        for i, point in enumerate(points):
            prevPoint = points[i - 1]
            x, y = point
            x2, y2 = prevPoint
            self.borders.append((x2,
             y2,
             x,
             y))
            vertex = AStarVertex(Point2(x, y))
            self.vertices.append(vertex)
            newVertices.append(vertex)

        for i, vertex in enumerate(newVertices):
            prevVertex = newVertices[i - 1]
            nextVertex = newVertices[(i + 1) % len(newVertices)]
            vertex.setPolygonalNeighbors(prevVertex, nextVertex)
            vertex.extrudeVertex(self.VERTEX_EXTRUSION)
            if vertex.interiorAngle > 180:
                self.vertices.remove(vertex)

    def buildNeighbors(self):
        for vertex in self.vertices:
            vertex.resetNeighbors()

        for i, v1 in enumerate(self.vertices):
            for v2 in self.vertices[i + 1:]:
                self._considerLink(v1, v2)

    def planPath(self, fromPoint, toPoint, closeEnough = 0):
        x1, y1 = fromPoint
        x2, y2 = toPoint
        if not self._testLineIntersections((x1,
         y1,
         x2,
         y2), self.borders):
            return [toPoint]
        fromVertex = AStarVertex(Point2(x1, y1))
        toVertex = AStarVertex(Point2(x2, y2))
        for vertex in self.vertices:
            self._considerLink(vertex, fromVertex)
            self._considerLink(vertex, toVertex)

        tempVertices = [fromVertex, toVertex]
        isApproximate = False
        try:
            if not toVertex.getNeighbors():
                if closeEnough is 0:
                    return
                isApproximate = True
                closeEnoughSquared = closeEnough * closeEnough
                for border in self.borders:
                    projected = self._projectPointToLine(toVertex.pos, border)
                    if projected is None:
                        continue
                    if (projected - toVertex.pos).lengthSquared() > closeEnoughSquared:
                        continue
                    projectionDirection = projected - toVertex.pos
                    projectionDirection.normalize()
                    projected += projectionDirection * self.VERTEX_EXTRUSION
                    projectedVertex = AStarVertex(projected)
                    projectedVertex.link(toVertex)
                    self._considerLink(fromVertex, projectedVertex)
                    for vertex in self.vertices:
                        self._considerLink(vertex, projectedVertex, False)

                    tempVertices.append(projectedVertex)

            astar = AStarSearch()
            result = astar.search(fromVertex, toVertex)
            if result:
                if isApproximate:
                    result.pop(-1)
                return [ vertex.pos for vertex in result ]
            return
        finally:
            for tempVertex in tempVertices:
                tempVertex.unlinkAll()

    def _considerLink(self, v1, v2, testAngles = True):
        if v1.isVertexPolygonalNeighbor(v2):
            v1.link(v2)
            return
        if testAngles:
            if v1.isVertexInsideAngle(v2) or v2.isVertexInsideAngle(v1):
                return
            if v1.isVertexInsideOpposite(v2) or v2.isVertexInsideOpposite(v1):
                return
        x1, y1 = v1.pos
        x2, y2 = v2.pos
        if self._testLineIntersections((x1,
         y1,
         x2,
         y2), self.borders):
            return
        v1.link(v2)

    def _makeLineMat(self, x1, y1, x2, y2):
        mat = Mat3(y2 - y1, x1 - x2, 0, x2 - x1, y2 - y1, 0, x1, y1, 1)
        if not mat.invertInPlace():
            return None
        return mat

    def _testLineIntersections(self, incident, lines):
        x1, y1, x2, y2 = incident
        mat = self._makeLineMat(x1, y1, x2, y2)
        if not mat:
            return False
        for x1, y1, x2, y2 in lines:
            x1, y1, _ = mat.xform(Point3(x1, y1, 1))
            x2, y2, _ = mat.xform(Point3(x2, y2, 1))
            if not (x1 < 0 and x2 > 0 or x1 > 0 and x2 < 0):
                continue
            m = (y2 - y1) / (x2 - x1)
            b = m * -x1 + y1
            epsilon = 0.001
            if 0.0 + epsilon < b < 1.0 - epsilon:
                return True

        return False

    def _projectPointToLine(self, point, line):
        x1, y1, x2, y2 = line
        x, y = point
        origin = Point2(x1, y1)
        vecLine = Point2(x2, y2) - origin
        vecPoint = Point2(x, y) - origin
        projectedPoint = vecPoint.project(vecLine)
        if projectedPoint.lengthSquared() > vecLine.lengthSquared():
            return None
        if projectedPoint.dot(vecLine) < 0:
            return None
        return origin + projectedPoint


class AStarVertex:

    def __init__(self, pos):
        self.pos = pos
        self.neighbors = []
        self.prevPolyNeighbor = None
        self.nextPolyNeighbor = None
        self.interiorAngle = None
        self.extrudeVector = None

    def link(self, neighbor):
        self.__addNeighbor(neighbor)
        neighbor.__addNeighbor(self)

    def unlink(self, neighbor):
        self.__removeNeighbor(neighbor)
        neighbor.__removeNeighbor(self)

    def unlinkAll(self):
        neighbors = list(self.neighbors)
        for neighbor in neighbors:
            self.unlink(neighbor)

    def resetNeighbors(self):
        self.neighbors = []

    def __addNeighbor(self, neighbor):
        if neighbor not in self.neighbors:
            self.neighbors.append(neighbor)

    def __removeNeighbor(self, neighbor):
        if neighbor in self.neighbors:
            self.neighbors.remove(neighbor)

    def setPolygonalNeighbors(self, prev, next):
        vecToPrev = prev.pos - self.pos
        vecToNext = next.pos - self.pos
        angle = vecToPrev.signedAngleDeg(vecToNext)
        angle %= 360
        self.prevPolyNeighbor = prev
        self.nextPolyNeighbor = next
        self.interiorAngle = angle
        prevAngle = Vec2(1, 0).signedAngleDeg(vecToPrev)
        extrudeAngle = prevAngle + self.interiorAngle / 2.0 + 180
        extrudeAngle *= math.pi / 180
        self.extrudeVector = Vec2(math.cos(extrudeAngle), math.sin(extrudeAngle))

    def isVertexInsideAngle(self, other):
        if self.prevPolyNeighbor is None or self.interiorAngle is None:
            return False
        vecToPrev = self.prevPolyNeighbor.pos - self.pos
        vecToOther = other.pos - self.pos
        angle = vecToPrev.signedAngleDeg(vecToOther)
        angle %= 360
        return angle < self.interiorAngle

    def isVertexInsideOpposite(self, other):
        if self.prevPolyNeighbor is None or self.interiorAngle is None:
            return False
        vecToPrev = self.prevPolyNeighbor.pos - self.pos
        vecToOther = other.pos - self.pos
        angle = vecToPrev.signedAngleDeg(vecToOther)
        angle -= 180
        angle %= 360
        return angle < self.interiorAngle

    def extrudeVertex(self, distance):
        if self.extrudeVector is None:
            return
        self.pos += self.extrudeVector * distance

    def isVertexPolygonalNeighbor(self, other):
        return other in (self.prevPolyNeighbor, self.nextPolyNeighbor)

    def getNeighbors(self):
        return self.neighbors

    def getHeuristicTo(self, other):
        return (self.pos - other.pos).length()

    def getCostTo(self, other):
        return (self.pos - other.pos).length()


class AStarSearch:

    def __init__(self):
        self.openList = []
        self.closed = set()
        self.paths = {}
        self._toVertex = None

    def search(self, fromVertex, toVertex):
        self.openList = [AStarPath(None, fromVertex, 0, 0)]
        self.closed = set()
        self.paths = {}
        self._toVertex = toVertex
        while self.openList and toVertex not in self.paths:
            self.__doIteration()

        path = self.paths.get(toVertex)
        if not path:
            return
        return self.__getVerticesToPath(path)

    def __doIteration(self):
        path = self.openList.pop(0)
        vertex = path.vertex
        self.closed.add(vertex)
        neighbors = vertex.getNeighbors()
        for neighbor in neighbors:
            if neighbor in self.closed:
                continue
            cost = vertex.getCostTo(neighbor) + path.totalCost
            if neighbor in self.paths:
                neighborPath = self.paths[neighbor]
                if cost < neighborPath.totalCost:
                    self.openList.remove(neighborPath)
                    del self.paths[neighbor]
                else:
                    continue
            newPath = AStarPath(path, neighbor, cost, neighbor.getHeuristicTo(self._toVertex))
            self.paths[neighbor] = newPath
            bisect.insort(self.openList, newPath)

    def __getVerticesToPath(self, path):
        result = []
        while path is not None:
            result.insert(0, path.vertex)
            path = path.parent

        return result


class AStarPath:

    def __init__(self, parent, vertex, cost, heuristic):
        self.parent = parent
        self.vertex = vertex
        self.heuristic = heuristic
        self.totalCost = cost

    def __cmp__(self, other):
        return cmp(self.totalCost + self.heuristic, other.totalCost + other.heuristic)
