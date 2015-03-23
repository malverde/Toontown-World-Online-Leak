from pandac.PandaModules import *

class ShadowPlacer(NodePath):
    def __init__(self, shadowNode):
        NodePath.__init__(self, hidden.attachNewNode('ShadowPlacer'))
        self.shadowNodePath = shadowNode
        self.shadowNodePath.reparentTo(self)

    def on(self):
        self.reparentTo(render)

    def off(self):
        self.reparentTo(hidden)

    def delete(self):
        self.removeNode()
