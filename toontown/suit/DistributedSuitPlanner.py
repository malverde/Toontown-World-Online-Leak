import SuitPlannerBase
from direct.distributed import DistributedObject
from otp.ai.MagicWordGlobal import *
from pandac.PandaModules import *
from toontown.dna.DNAParser import DNASuitPoint
from toontown.toonbase import ToontownGlobals


class DistributedSuitPlanner(DistributedObject.DistributedObject, SuitPlannerBase.SuitPlannerBase):

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        SuitPlannerBase.SuitPlannerBase.__init__(self)
        self.suitList = []
        self.buildingList = [0, 0, 0, 0]
        self.pathViz = None
        self.debugText = {}

    def generate(self):
        self.notify.info('DistributedSuitPlanner %d: generating' % self.getDoId())
        DistributedObject.DistributedObject.generate(self)
        base.cr.currSuitPlanner = self

    def disable(self):
        self.notify.info('DistributedSuitPlanner %d: disabling' % self.getDoId())
        self.hidePaths()
        DistributedObject.DistributedObject.disable(self)
        base.cr.currSuitPlanner = None

    def d_suitListQuery(self):
        self.sendUpdate('suitListQuery')

    def suitListResponse(self, suitList):
        self.suitList = suitList
        messenger.send('suitListResponse')

    def d_buildingListQuery(self):
        self.sendUpdate('buildingListQuery')

    def buildingListResponse(self, buildingList):
        self.buildingList = buildingList
        messenger.send('buildingListResponse')

    def hidePaths(self):
        if self.pathViz:
            self.pathViz.detachNode()
            self.pathViz = None

    def showPaths(self):
        self.hidePaths()
        vizNode = GeomNode(self.uniqueName('PathViz'))
        lines = LineSegs()
        self.pathViz = render.attachNewNode(vizNode)
        points = self.frontdoorPointList + self.sidedoorPointList + self.cogHQDoorPointList + self.streetPointList
        while len(points) > 0:
            self.__doShowPoints(vizNode, lines, None, points)
        cnode = CollisionNode('battleCells')
        cnode.setCollideMask(BitMask32.allOff())
        for zoneId, cellPos in self.battlePosDict.items():
            cnode.addSolid(CollisionSphere(LPoint3f(cellPos), 9))
            text = '%s' % zoneId
            self.__makePathVizText(text, cellPos[0], cellPos[1], cellPos[2] + 9, (1, 1, 1, 1))
        self.pathViz.attachNewNode(cnode).show()

    def __doShowPoints(self, vizNode, lines, p, points):
        if p == None:
            pi = len(points) - 1
            if pi < 0:
                return
            p = points[pi]
            del points[pi]
        else:
            if p not in points:
                return
            pi = points.index(p)
            del points[pi]
        text = '%s' % p.getIndex()
        pos = p.getPos()
        if p.getPointType() == DNASuitPoint.FRONT_DOOR_POINT:
            color = (1, 0, 0, 1)
        elif p.getPointType() == DNASuitPoint.SIDE_DOOR_POINT:
            color = (0, 0, 1, 1)
        elif p.getPointType() == DNASuitPoint.COGHQ_IN_POINT:
            color = (0, 0, 0, 1)
        elif p.getPointType() == DNASuitPoint.COGHQ_OUT_POINT:
            color = (0.5, 0.5, 0.5, 1)
        else:
            color = (0, 1, 0, 1)
        self.__makePathVizText(text, pos[0], pos[1], pos[2], color, i=p.getIndex())
        cs = CollisionSphere(LPoint3f(pos), 3)
        cs.setTangible(0)
        triggerName = 'suitPoint-' + str(p.getIndex())
        cn = CollisionNode(triggerName)
        cn.addSolid(cs)
        cn.setIntoCollideMask(ToontownGlobals.WallBitmask)
        base.accept('enter' + triggerName, self.__showEdges, [p.getIndex()])
        base.accept('exit' + triggerName, self.__hideEdges, [p.getIndex()])
        self.pathViz.attachNewNode(cn)
        adjacent = self.dnaStore.getAdjacentPoints(p)
        numPoints = adjacent.getNumPoints()
        for i in xrange(numPoints):
            qi = adjacent.getPointIndex(i)
            q = self.dnaStore.getSuitPointWithIndex(qi)
            pp = p.getPos()
            qp = q.getPos()
            v = Vec3(qp - pp)
            v.normalize()
            c = v.cross(Vec3.up())
            p1a = pp + v * 2 + c * 0.5
            p1b = pp + v * 3
            p1c = pp + v * 2 - c * 0.5
            lines.reset()
            lines.moveTo(pp)
            lines.drawTo(qp)
            lines.moveTo(p1a)
            lines.drawTo(p1b)
            lines.drawTo(p1c)
            lines.create(vizNode, 0)
            self.__doShowPoints(vizNode, lines, q, points)

    def __makePathVizText(self, text, x, y, z, color, i=-1):
        if not hasattr(self, 'debugTextNode'):
            self.debugTextNode = TextNode('debugTextNode')
            self.debugTextNode.setAlign(TextNode.ACenter)
            self.debugTextNode.setFont(ToontownGlobals.getSignFont())
        self.debugTextNode.setTextColor(*color)
        self.debugTextNode.setText(text)
        np = self.pathViz.attachNewNode(self.debugTextNode.generate())
        np.setPos(x, y, z + 1)
        np.setScale(1.0)
        np.setBillboardPointEye(2)
        np.node().setAttrib(TransparencyAttrib.make(TransparencyAttrib.MDual), 2)
        if i >= 0:
            self.debugText[i] = np

    def __showEdges(self, i, collisionEntry):
        highlightedPoints = [i]
        if i in self.dnaStore.suitEdges:
            edges = self.dnaStore.suitEdges[i]
            for edge in edges:
                endPoint = edge.getEndPoint()
                highlightedPoints.append(endPoint.getIndex())
        for i in highlightedPoints:
            p = self.dnaStore.getSuitPointWithIndex(i)
            pos = p.getPos()
            self.debugText[i].removeNode()
            self.__makePathVizText(str(p.getIndex()), pos[0], pos[1], pos[2], (0.95, 1, 0, 1), i=p.getIndex())

    def __hideEdges(self, i, collisionEntry):
        highlightedPoints = [i]
        if i in self.dnaStore.suitEdges:
            edges = self.dnaStore.suitEdges[i]
            for edge in edges:
                endPoint = edge.getEndPoint()
                highlightedPoints.append(endPoint.getIndex())
        for i in highlightedPoints:
            p = self.dnaStore.getSuitPointWithIndex(i)
            pos = p.getPos()
            self.debugText[i].removeNode()
            if p.getPointType() == DNASuitPoint.FRONT_DOOR_POINT:
                color = (1, 0, 0, 1)
            elif p.getPointType() == DNASuitPoint.SIDE_DOOR_POINT:
                color = (0, 0, 1, 1)
            elif p.getPointType() == DNASuitPoint.COGHQ_IN_POINT:
                color = (0, 0, 0, 1)
            elif p.getPointType() == DNASuitPoint.COGHQ_OUT_POINT:
                color = (0.5, 0.5, 0.5, 1)
            else:
                color = (0, 1, 0, 1)
            self.__makePathVizText(str(p.getIndex()), pos[0], pos[1], pos[2], color, i=p.getIndex())


@magicWord(category=CATEGORY_COMMUNITY_MANAGER)
def suitPaths():
    response = "Couldn't toggle suit path visualization."
    for do in base.cr.doId2do.values():
        if not isinstance(do, DistributedSuitPlanner):
            continue
        if getattr(do, '_showPaths', False):
            do.hidePaths()
            do._showPaths = False
            response = 'Suit paths are not being visualized.'
        else:
            do.showPaths()
            do._showPaths = True
            response = 'Suit paths are being visualized.'
    return response
