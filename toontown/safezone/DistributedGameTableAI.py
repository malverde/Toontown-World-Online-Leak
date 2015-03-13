from direct.distributed import DistributedObjectAI


class DistributedGameTableAI(DistributedObjectAI.DistributedObjectAI):
    def __init__(self, air):
        DistributedObjectAI.DistributedObjectAI.__init__(self, air)

        self.posHpr = (0, 0, 0, 0, 0, 0)

    # Required Fields:

    def setPosHpr(self, x, y, z, h, p, r):
        self.posHpr = (x, y, z, h, p, r)

    def getPosHpr(self):
        return self.posHpr

    # Receive Fields:

    def requestJoin(self, seatIndex):
        avId = self.air.getAvatarIdFromSender()
        self.sendUpdateToAvatarId(avId, 'rejectJoin', [])

    def requestExit(self):
        pass
