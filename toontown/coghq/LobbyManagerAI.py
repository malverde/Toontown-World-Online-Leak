from direct.distributed import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import ToontownGlobals

class LobbyManagerAI(DistributedObjectAI.DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('LobbyManagerAI')

    def __init__(self, air, bossConstructor, brutalBossCtor):
        DistributedObjectAI.DistributedObjectAI.__init__(self, air)
        self.air = air
        self.bossConstructor = bossConstructor
        self.brutalBossCtor = brutalBossCtor

    def delete(self):
        self.ignoreAll()

        DistributedObjectAI.DistributedObjectAI.delete(self)

    def createBossOffice(self, avIdList, isBrutal=False):
        bossZone = self.air.allocateZone()
        self.notify.info('createBossOffice: %s' % bossZone)
        if isBrutal:
            bossCog = self.brutalBossCtor(self.air)
        else:
            bossCog = self.bossConstructor(self.air)
        bossCog.generateWithRequired(bossZone)
        self.acceptOnce(bossCog.uniqueName('BossDone'), self.destroyBossOffice, extraArgs=[bossCog])
        for avId in avIdList:
            if avId:
                bossCog.addToon(avId)

        bossCog.b_setState('WaitForToons')
        return bossZone

    def destroyBossOffice(self, bossCog):
        bossZone = bossCog.zoneId
        self.notify.info('destroyBossOffice: %s' % bossZone)
        bossCog.requestDelete()
        self.air.deallocateZone(bossZone)
