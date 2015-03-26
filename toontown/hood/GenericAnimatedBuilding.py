from toontown.hood import GenericAnimatedProp

class GenericAnimatedBuilding(GenericAnimatedProp.GenericAnimatedProp):

    def __init__(self, node):
        GenericAnimatedProp.GenericAnimatedProp.__init__(self, node)
        parent = node.getParent()
        self.building = Actor.Actor(node, copy=0)
        self.building.reparentTo(parent)
        self.building.loadAnims({'dance': 'phase_5/models/char/tt_a_ara_ttc_B2_dance'})
        self.building.pose('dance', 0)
        self.node = self.building        

    def enter(self):
        if base.config.GetBool('buildings-animate', True):
            GenericAnimatedProp.GenericAnimatedProp.enter(self)
            self.building.loop('dance') # Dancing buildings? Why the fuck not?

    def delete(self):
        GenericAnimatedProp.GenericAnimatedProp.delete(self)
        self.building.cleanup()
        del self.building

    def exit(self):
        GenericAnimatedProp.GenericAnimatedProp.exit(self)
        self.building.stop()
