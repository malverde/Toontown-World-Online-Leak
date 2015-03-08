from panda3d.core import BamFile, NodePath, StringStream, decompressString
import DNANode

class DNASignBaseline(DNANode.DNANode):
    COMPONENT_CODE = 6

    def __init__(self):
        DNANode.DNANode.__init__(self, '')
        self.data = ''

    def makeFromDGI(self, dgi):
        DNANode.DNANode.makeFromDGI(self, dgi)
        self.data = dgi.getString()
        if len(self.data):
            self.data = decompressString(self.data)

    def traverse(self, nodePath, dnaStorage):
        node = nodePath.attachNewNode('baseline', 0)
        node.setPosHpr(self.pos, self.hpr)
        node.setPos(node, 0, -0.1, 0)
        if self.data:
            bf = BamFile()
            ss = StringStream()
            ss.setData(self.data)
            bf.openRead(ss)
            signText = NodePath(bf.readNode())
            signText.reparentTo(node)
        node.flattenStrong()
        for child in self.children:
            child.traverse(nodePath, dnaStorage)