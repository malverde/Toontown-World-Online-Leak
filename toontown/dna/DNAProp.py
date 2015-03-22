from panda3d.core import LVector4f, ModelNode
import DNANode
import DNAUtil

class DNAProp(DNANode.DNANode):
    COMPONENT_CODE = 4

    def __init__(self, name):
        DNANode.DNANode.__init__(self, name)
        self.code = ''
        self.color = LVector4f(1, 1, 1, 1)

    def getCode(self):
        return self.code

    def setCode(self, code):
        self.code = code

    def getColor(self):
        return self.color

    def setColor(self, color):
        self.color = color

    def smartFlatten(self, node):
        if 'trolley' in self.name:
            return
        elif self.children:
            node.flattenMedium()
        elif 'HQTelescopeAnimatedProp' in self.name:
            node.flattenMedium()
        elif node.find('**/water1*').isEmpty():
            node.flattenStrong()
        elif not node.find('**/water').isEmpty():
            water = node.find('**/water')
            water.setTransparency(1)
            water.setColor(1, 1, 1, 0.8)
            node.flattenStrong()
        elif not node.find('**/water1*').isEmpty():
            water = node.find('**/water1*')
            water.setTransparency(1)
            water.setColorScale(1.0, 1.0, 1.0, 1.0)
            water.setBin('water', 51, 1)
            node.flattenStrong()

    def makeFromDGI(self, dgi):
        DNANode.DNANode.makeFromDGI(self, dgi)
        self.code = DNAUtil.dgiExtractString8(dgi)
        self.color = DNAUtil.dgiExtractColor(dgi)

    def traverse(self, nodePath, dnaStorage):
        if self.code == 'DCS':
            node = ModelNode(self.name)
            node.setPreserveTransform(ModelNode.PTNet)
            node = nodePath.attachNewNode(node)
        else:
            node = dnaStorage.findNode(self.code)
            if node is None:
                return
            node = node.copyTo(nodePath, 0)
        node.setPosHprScale(self.pos, self.hpr, self.scale)
        node.setName(self.name)
        node.setColorScale(self.color, 0)
        #self.smartFlatten(node)
        for child in self.children:
            child.traverse(node, dnaStorage)
