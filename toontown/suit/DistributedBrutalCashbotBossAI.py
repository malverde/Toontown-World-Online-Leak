from toontown.suit.DistributedCashbotBossAI import DistributedCashbotBossAI
from toontown.toonbase import ToontownGlobals
from toontown.chat import ResistanceChat

import random


class DistributedBrutalCashbotBossAI(DistributedCashbotBossAI):
    notify = directNotify.newCategory('DistributedBrutalCashbotBoss')

    DEPT = 'c'
    WANT_SAFES = False

    def __init__(self, air):
        DistributedCashbotBossAI.__init__(self, air)

        self.rewardId = ResistanceChat.getRandomBrutalId()
        self.bossMaxDamage = ToontownGlobals.BrutalCashbotBossMaxDamage

    def generateSuits(self, battleNumber):
        return self.invokeSuitPlanner(20, 0)

    def recordHit(self, damage):
        avId = self.air.getAvatarIdFromSender()

        if not self.validate(avId, avId in self.involvedToons, 'recordHit from unknown avatar'):
            return

        if self.state != 'BattleThree':
            return

        self.b_setBossDamage(self.bossDamage + damage)

        if self.bossDamage >= self.bossMaxDamage:
            self.b_setState('Victory')

        self.b_setAttackCode(ToontownGlobals.BossCogNoAttack)

    def waitForNextHelmet(self):
        pass

    def applyReward(self):
        avId = self.air.getAvatarIdFromSender()
        if avId in self.involvedToons and avId not in self.rewardedToons:
            self.rewardedToons.append(avId)

            toon = self.air.doId2do.get(avId)
            if toon:
                for _ in xrange(4):
                    toon.doResistanceEffect(self.rewardId)

            if simbase.config.GetBool('cfo-staff-event', False):

                withStaff = False
                for avId in self.involvedToons:
                    av = self.air.doId2do.get(avId)
                    if av:
                        if av.adminAccess > 100:
                            withStaff = True

                if withStaff:
                    participants = simbase.backups.load('cfo-staff-event', ('participants',), default={'doIds': []})
                    if avId not in participants['doIds']:
                        participants['doIds'].append(toon.doId)
                    simbase.backups.save('cfo-staff-event', ('participants',), participants)

    def removeToon(self, avId):
        av = self.air.doId2do.get(avId)

        if self.cranes is not None:
            for crane in self.cranes:
                crane.removeToon(avId)

        if self.safes is not None:
            for safe in self.safes:
                safe.removeToon(avId)

        if self.goons is not None:
            for goon in self.goons:
                goon.removeToon(avId)

        if avId in self.looseToons:
            self.looseToons.remove(avId)

        if avId in self.involvedToons:
            self.involvedToons.remove(avId)

        if avId in self.toonsA:
            self.toonsA.remove(avId)

        if avId in self.toonsB:
            self.toonsB.remove(avId)

        if avId in self.nearToons:
            self.nearToons.remove(avId)

        event = self.air.getAvatarExitEvent(avId)
        self.ignore(event)
        if not self.hasToons():
            taskMgr.doMethodLater(10, self.getBossDoneFunc(), self.uniqueName('BossDone'))

    def progressValue(self, fromValue, toValue):
        t0 = float(self.bossDamage) / float(self.bossMaxDamage)
        elapsed = globalClock.getFrameTime() - self.battleThreeStart
        t1 = elapsed / float(self.battleThreeDuration)
        t = max(t0, t1)
        return fromValue + (toValue - fromValue) * min(t, 1) * 1.5

    def progressRandomValue(self, fromValue, toValue, radius = 0.2):
        t = self.progressValue(0, 1)
        radius = radius * (1.0 - abs(t - 0.5) * 2.0)
        t += radius * random.uniform(-1, 1)
        t = max(min(t, 1.0), 0.0)
        return fromValue + (toValue - fromValue) * t * 1.5