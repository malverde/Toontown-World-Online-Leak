from direct.distributed.DistributedObjectAI import DistributedObjectAI


class DistributedLibraryInteriorAI(DistributedObjectAI):
    def __init__(self, block, air, zoneId):
        DistributedObjectAI.__init__(self, air)

        self.block = block
        self.zoneId = zoneId

    def getZoneIdAndBlock(self):
        return (self.zoneId, self.block)
