import DNAProp
from DNAUtil import *

class DNAAnimProp(DNAProp.DNAProp):
    COMPONENT_CODE = 14

    def __init__(self, name):
        DNAProp.DNAProp.__init__(self, name)
        self.animName = ''

    def setAnim(self, anim):
        self.animName = anim

    def getAnim(self):
        return self.animName

    def makeFromDGI(self, dgi):
        DNAProp.DNAProp.makeFromDGI(self, dgi)
        self.animName = dgiExtractString8(dgi)

    def traverse(self, nodePath, dnaStorage):
        node = None
        if self.getCode() == 'DCS':
            node = ModelNode(self.getName())
            node.setPreserveTransform(ModelNode.PTNet)
            node = nodePath.attachNewNode(node, 0)
        else:
            node = dnaStorage.findNode(self.getCode())
            node = node.copyTo(nodePath, 0)
            node.setName(self.getName())
        node.setTag('DNAAnim', self.getAnim())
        node.setPosHprScale(self.getPos(), self.getHpr(), self.getScale())
        node.setColorScale(self.getColor(), 0)
        node.flattenStrong()
        for child in self.children:
            child.traverse(node, dnaStorage)