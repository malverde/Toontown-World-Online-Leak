from otp.level import DistributedEntity
from direct.directnotify import DirectNotifyGlobal
from pandac.PandaModules import NodePath
from otp.level import BasicEntities

class DistributedCrushableEntity(DistributedEntity.DistributedEntity, NodePath, BasicEntities.NodePathATTWibs):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedCrushableEntity')

    def __init__(self, cr):
        DistributedEntity.DistributedEntity.__init__(self, cr)
        node = hidden.attachNewNode('DistributedNodePathEntity')

    def initNodePath(self):
        node = hidden.attachNewNode('DistributedNodePathEntity')
        NodePath.__init__(self, node)

    def announceGenerate(self):
        DistributedEntity.DistributedEntity.announceGenerate(self)
        BasicEntities.NodePathATTWibs.initNodePathATTWibs(self)

    def disable(self):
        self.reparentTo(hidden)
        BasicEntities.NodePathATTWibs.destroy(self)
        DistributedEntity.DistributedEntity.disable(self)

    def delete(self):
        self.removeNode()
        DistributedEntity.DistributedEntity.delete(self)

    def setPosition(self, x, y, z):
        self.setPos(x, y, z)

    def setCrushed(self, crusherId, axis):
        self.playCrushMovie(crusherId, axis)

    def playCrushMovie(self, crusherId, axis):
        pass
