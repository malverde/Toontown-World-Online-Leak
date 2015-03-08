from panda3d.core import LVector3f, PandaNode
import DNAGroup

class DNANode(DNAGroup.DNAGroup):
    COMPONENT_CODE = 3

    def __init__(self, name):
        DNAGroup.DNAGroup.__init__(self, name)
        self.pos = LVector3f()
        self.hpr = LVector3f()
        self.scale = LVector3f(1, 1, 1)

    def getPos(self):
        return self.pos

    def setPos(self, pos):
        self.pos = pos

    def getHpr(self):
        return self.hpr

    def setHpr(self, hpr):
        self.hpr = hpr

    def getScale(self):
        return self.scale

    def setScale(self, scale):
        self.scale = scale

    def makeFromDGI(self, dgi):
        DNAGroup.DNAGroup.makeFromDGI(self, dgi)

        x = dgi.getInt32() / 100.0
        y = dgi.getInt32() / 100.0
        z = dgi.getInt32() / 100.0
        self.pos = LVector3f(x, y, z)

        h = dgi.getInt32() / 100.0
        p = dgi.getInt32() / 100.0
        r = dgi.getInt32() / 100.0
        self.hpr = LVector3f(h, p, r)

        sx = dgi.getInt16() / 100.0
        sy = dgi.getInt16() / 100.0
        sz = dgi.getInt16() / 100.0
        self.scale = LVector3f(sx, sy, sz)

    def traverse(self, nodePath, dnaStorage):
        node = PandaNode(self.name)
        node = nodePath.attachNewNode(node, 0)
        node.setPosHprScale(self.pos, self.hpr, self.scale)
        for child in self.children:
            child.traverse(node, dnaStorage)
        node.flattenMedium()