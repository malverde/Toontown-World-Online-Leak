import Entity
import DistributedEntity
from pandac.PandaModules import NodePath

class NodePathEntityBase:

    def initNodePathATTWibs(self, doReparent = 1):
        self.callSetters('pos', 'x', 'y', 'z', 'hpr', 'h', 'p', 'r', 'scale', 'sx', 'sy', 'sz')
        if doReparent:
            self.callSetters('parentEntId')
        self.getNodePath().setName('%s-%s' % (self.__class__.__name__, self.entId))
        if __dev__:
            self.getNodePath().setTag('entity', '1')

    def setParentEntId(self, parentEntId):
        self.parentEntId = parentEntId
        self.level.requestReparent(self, self.parentEntId)

    def destroy(self):
        if __dev__:
            self.getNodePath().clearTag('entity')


class NodePathATTWibs(NodePathEntityBase):

    def initNodePathATTWibs(self, doReparent = 1):
        NodePathEntityBase.initNodePathATTWibs(self, doReparent)

    def destroy(self):
        NodePathEntityBase.destroy(self)

    def getNodePath(self):
        return self


class NodePathAndATTWibs(NodePathEntityBase, NodePath):

    def __init__(self):
        node = hidden.attachNewNode('EntityNodePath')
        NodePath.__init__(self, node)

    def initNodePathATTWibs(self, doReparent = 1):
        NodePathEntityBase.initNodePathATTWibs(self, doReparent)

    def destroy(self):
        NodePathEntityBase.destroy(self)
        self.removeNode()

    def getNodePath(self):
        return self


class NodePathATTWibsProxy(NodePathEntityBase):

    def initNodePathATTWibs(self, doReparent = 1):
        NodePathEntityBase.initNodePathATTWibs(self, doReparent)

    def destroy(self):
        NodePathEntityBase.destroy(self)

    def setPos(self, *args):
        self.getNodePath().setPos(*args)

    def setX(self, *args):
        self.getNodePath().setX(*args)

    def setY(self, *args):
        self.getNodePath().setY(*args)

    def setZ(self, *args):
        self.getNodePath().setZ(*args)

    def setHpr(self, *args):
        self.getNodePath().setHpr(*args)

    def setH(self, *args):
        self.getNodePath().setH(*args)

    def setP(self, *args):
        self.getNodePath().setP(*args)

    def setR(self, *args):
        self.getNodePath().setR(*args)

    def setScale(self, *args):
        self.getNodePath().setScale(*args)

    def setSx(self, *args):
        self.getNodePath().setSx(*args)

    def setSy(self, *args):
        self.getNodePath().setSy(*args)

    def setSz(self, *args):
        self.getNodePath().setSz(*args)

    def reparentTo(self, *args):
        self.getNodePath().reparentTo(*args)


class NodePathEntity(Entity.Entity, NodePath, NodePathATTWibs):

    def __init__(self, level, entId):
        node = hidden.attachNewNode('NodePathEntity')
        NodePath.__init__(self, node)
        Entity.Entity.__init__(self, level, entId)
        self.initNodePathATTWibs(self)

    def destroy(self):
        NodePathATTWibs.destroy(self)
        Entity.Entity.destroy(self)
        self.removeNode()


class DistributedNodePathEntity(DistributedEntity.DistributedEntity, NodePath, NodePathATTWibs):

    def __init__(self, cr):
        DistributedEntity.DistributedEntity.__init__(self, cr)

    def generateInit(self):
        DistributedEntity.DistributedEntity.generateInit(self)
        node = hidden.attachNewNode('DistributedNodePathEntity')
        NodePath.__init__(self, node)

    def announceGenerate(self):
        DistributedEntity.DistributedEntity.announceGenerate(self)
        self.initNodePathATTWibs(self)

    def delete(self):
        self.removeNode()
        DistributedEntity.DistributedEntity.delete(self)
