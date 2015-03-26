from direct.directnotify.DirectNotifyGlobal import *
from pandac.PandaModules import *

from toontown.suit import SuitDNA
from toontown.suit import SuitDialog
from toontown.suit.DistributedSuitBaseAI import DistributedSuitBaseAI
from toontown.tutorial.DistributedBattleTutorialAI import DistributedBattleTutorialAI


class FakeBattleManager:
    def __init__(self, avId):
        self.avId = avId

    def destroy(self, battle):
        if battle.suitsKilledThisBattle:
            if self.avId in simbase.air.tutorialManager.avId2fsm:
                simbase.air.tutorialManager.avId2fsm[self.avId].demand('HQ')
        battle.requestDelete()


class DistributedTutorialSuitAI(DistributedSuitBaseAI):
    notify = directNotify.newCategory('DistributedTutorialSuitAI')

    def __init__(self, air):
        DistributedSuitBaseAI.__init__(self, air, None)

        suitDNA = SuitDNA.SuitDNA()
        suitDNA.newSuit('f')
        self.dna = suitDNA
        self.setLevel(1)

    def destroy(self):
        del self.dna

    def requestBattle(self, x, y, z, h, p, r):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)
        if av is None:
            return

        self.confrontPos = Point3(x, y, z)
        self.confrontHpr = Vec3(h, p, r)

        if av.getBattleId() > 0:
            self.notify.warning('Avatar %d tried to request a battle, but is already in one.' % avId)
            self.b_setBrushOff(SuitDialog.getBrushOffIndex(self.getStyleName()))
            self.d_denyBattle(avId)
            return

        battle = DistributedBattleTutorialAI(
            self.air, FakeBattleManager(avId), Point3(35, 20, -0.5), self,
            avId, 20001)
        battle.generateWithRequired(self.zoneId)
        battle.battleCellId = 0

    def getConfrontPosHpr(self):
        return (self.confrontPos, self.confrontHpr)
