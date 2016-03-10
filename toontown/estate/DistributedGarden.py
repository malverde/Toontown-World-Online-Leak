from direct.distributed.DistributedObject import DistributedObject

from toontown.estate import HouseGlobals


class DistributedGarden(DistributedObject):
    notify = directNotify.newCategory('DistributedGarden')

    PROPS = {
        HouseGlobals.PROP_ICECUBE: 'phase_8/models/props/icecube.bam',
        HouseGlobals.PROP_FLOWER: 'phase_8/models/props/flower_treasure.bam',
        HouseGlobals.PROP_SNOWFLAKE: 'phase_8/models/props/snowflake_treasure.bam'
    }

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)

        self.lt = base.localAvatar
        self.props = []
        self.pos = None
        self.radius = 0
        self.gridCells = 20
        self.propTable = [None] * self.gridCells

        for i in xrange(len(self.propTable)):
            self.propTable[i] = [None] * self.gridCells

        self.dx = 1.0 / self.gridCells
        self.occupied = []

    def delete(self):
        for prop in self.props:
            prop[0].removeNode()

        self.props = []

    def sendNewProp(self, prop, x, y, z):
        path = self.PROPS.get(prop)
        if path is None:
            self.notify.warning('Unknown prop: %s' % prop)
            return

        model = loader.loadModel(path)
        model.setPos(x, y, z)
        model.setScale(0.2)
        model.setBillboardPointEye()
        model.reparentTo(render)

        self.props.append([model, x, y, z])

    def getPropPos(self, i, j):
        return [self.pos[0] - self.radius + 2 * self.radius * i,
                self.pos[1] - self.radius + 2 * self.radius * j,
                self.pos[2]]

    def loadProp(self, prop, i, j):
        pos = self.getPropPos(i, j)
        path = self.PROPS.get(prop)
        if path is None:
            self.notify.warning('Unknown prop: %s' % prop)
            return

        model = loader.loadModel(path)
        model.setPos(pos[0], pos[1], pos[2])
        model.setScale(0.2)
        model.setBillboardPointEye()
        model.reparentTo(render)

    def setAddProp(self, prop, i, j):
        self.props.append([prop, i, j])
        self.loadProp(prop, i, j)
        self.b_setProps(self, self.props)

    def b_setProps(self, props):
        self.setProps(props)
        self.d_setProps(props)

    def d_setProps(self, props):
        self.sendUpdate('setProps', [props])

    def setProps(self, props):
        self.props = props

        for prop in self.props:
            pInd, i, j = prop
            self.propTable[i, j] = pInd
