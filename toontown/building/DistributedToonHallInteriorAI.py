from DistributedToonInteriorAI import *
from toontown.toonbase import ToontownGlobals


class DistributedToonHallInteriorAI(DistributedToonInteriorAI):
    def __init__(self, block, air, zoneId, building):
        DistributedToonInteriorAI.__init__(self, block, air, zoneId, building)
        self.accept('ToonEnteredZone', self.logToonEntered)
        self.accept('ToonLeftZone', self.logToonLeft)

    def logToonEntered(self, avId, zoneId):
        result = self.getCurPhase()
        if result == -1:
            phase = 'not available'
        else:
            phase = str(result)
        self.air.writeServerEvent(avId, 'entered toonhall')

    def logToonLeft(self, avId, zoneId):
        self.air.writeServerEvent(avId, 'exited toonhall')

    def delete(self):
        self.ignoreAll()
        DistributedToonInteriorAI.delete(self)
