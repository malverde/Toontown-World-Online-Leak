from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase.ToontownGlobals import *
from toontown.safezone import RegenTreasurePlannerAI
from toontown.safezone import TreasureGlobals

class TagTreasurePlannerAI(RegenTreasurePlannerAI.RegenTreasurePlannerAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('TagTreasurePlannerAI')

    def __init__(self, zoneId, game, callback):
        self.numPlayers = 0
        self.game = game
        RegenTreasurePlannerAI.RegenTreasurePlannerAI.__init__(self, zoneId, TreasureGlobals.TreasureTT, 'TagTreasurePlanner-' + str(zoneId), 3, 4, callback)
        return None

    def initSpawnPoints(self):
        self.spawnPoints = [(1.513, 92.867, 0.025),
         (16.182, 110.657, 0.025),
         (5.546, 129.393, 0.025),
         (-13.570, 123.593, 0.025),
         (-36.960, 102.175, 0.025),
         (-54.228, 97.105, 0.025),
         (-58.487, 120.859, 0.025),
         (-40.125, 130.528, 0.025),
         (-22.243, 138.216, 0.025),
         (-5.929, 147.418, 0.025),
         (10.651, 145.624, 0.025),
         (6.184, 166.947, 0.025),
         (-24.769, 160.486, 0.025),
         (32.721, 128.607, 0.025),
         (45.624, 115.085, 0.025),
         (39.829, 96.130, 0.025),
         (-62.112, 97.018, 0.025)]
        return self.spawnPoints

    def validAvatar(self, treasure, av):
        return av.doId != self.game.itAvId
