from panda3d.core import LVector4f
import DNANode
import DNAFlatBuilding
import DNAError
import DNAUtil

class DNAWall(DNANode.DNANode):
    COMPONENT_CODE = 10

    def __init__(self, name):
        DNANode.DNANode.__init__(self, name)
        self.code = ''
        self.height = 10
        self.color = LVector4f(1, 1, 1, 1)

    def setCode(self, code):
        self.code = code

    def getCode(self):
        return self.code

    def setColor(self, color):
        self.color = color

    def getColor(self):
        return self.color

    def setHeight(self, height):
        self.height = height

    def getHeight(self):
        return self.height

    def makeFromDGI(self, dgi):
        DNANode.DNANode.makeFromDGI(self, dgi)
        self.code = DNAUtil.dgiExtractString8(dgi)
        self.height = dgi.getInt16() / 100.0
        self.color = DNAUtil.dgiExtractColor(dgi)

    def traverse(self, nodePath, dnaStorage):
        node = dnaStorage.findNode(self.code)
        if node is None:
            raise DNAError.DNAError('DNAWall code ' + self.code + ' not found in DNAStorage')
        node = node.copyTo(nodePath, 0)
        self.pos.setZ(DNAFlatBuilding.DNAFlatBuilding.currentWallHeight)
        self.scale.setZ(self.height)
        node.setPosHprScale(self.pos, self.hpr, self.scale)
        node.setColor(self.color)
        for child in self.children:
            child.traverse(node, dnaStorage)
        node.flattenStrong()
        DNAFlatBuilding.DNAFlatBuilding.currentWallHeight += self.height