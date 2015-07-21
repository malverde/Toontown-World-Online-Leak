from direct.directnotify import DirectNotifyGlobal
from toontown.parties.DistributedPartyActivityAI import DistributedPartyActivityAI
from toontown.toonbase import TTLocalizer
import PartyGlobals

class DistributedPartyCannonActivityAI(DistributedPartyActivityAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedPartyCannonActivityAI")
    
    def __init__(self, air, parent, activityTuple):
        DistributedPartyActivityAI.__init__(self, air, parent, activityTuple)
        self.cloudColors = {}
        self.cloudsHit = {}

    def setMovie(self, mode, toonId):
        self.notify.debug('%s setMovie(%s, %s)' % (self.doId, toonId, mode))
        if toonId != base.localAvatar.doId:
            return
        if mode == PartyGlobals.CANNON_MOVIE_CLEAR:
            self.landToon(toonId)
        elif mode == PartyGlobals.CANNON_MOVIE_LANDED:
            self.landToon(toonId)
        elif mode == PartyGlobals.CANNON_MOVIE_FORCE_EXIT:
            self.landToon(toonId)
    def setLanded(self, toonId):
        avId = self.air.getAvatarIdFromSender()
        if avId != toonId:
            self.air.writeServerEvent('suspicious',avId,'Toon tried to land someone else!')
            return
        if not avId in self.toonsPlaying:
            self.air.writeServerEvent('suspicious',avId,'Toon tried to land while not playing the cannon activity!')
            return
        self.toonsPlaying.remove(avId)
        reward = self.cloudsHit[avId] * PartyGlobals.CannonJellyBeanReward
        if reward > PartyGlobals.CannonMaxTotalReward:
            reward = PartyGlobals.CannonMaxTotalReward
        av = self.air.doId2do.get(avId, None)
        if not av:
            self.air.writeServerEvent('suspicious',avId,'Toon tried to award beans while not in district!')
            return
        # TODO: Pass a msgId(?) to the client so the client can use whatever localizer it chooses.
        # Ideally, we shouldn't even be passing strings that *should* be localized.
        self.sendUpdateToAvatarId(avId, 'showJellybeanReward', [reward, av.getMoney(), TTLocalizer.PartyCannonResults % (reward, self.cloudsHit[avId])])
        av.addMoney(reward)
        self.sendUpdate('setMovie', [PartyGlobals.CANNON_MOVIE_LANDED, avId])
        del self.cloudsHit[avId]

    def b_setCannonWillFire(self, cannonId, rot, angle, toonId):
        self.toonsPlaying.append(toonId)
        self.cloudsHit[toonId] = 0
        self.sendUpdate('setCannonWillFire', [cannonId, rot, angle])

    def cloudsColorRequest(self):
        avId = self.air.getAvatarIdFromSender()
        self.sendUpdateToAvatarId(avId, 'cloudsColorResponse', [self.cloudColors.values()])

    def requestCloudHit(self, cloudId, r, g, b):
        avId = self.air.getAvatarIdFromSender()
        if not avId in self.toonsPlaying:
            self.air.writeServerEvent('suspicious',avId,'Toon tried to hit cloud in cannon activity they\'re not using!')
            return
        self.cloudColors[cloudId] = [cloudId, r, g, b]
        self.sendUpdate('setCloudHit', [cloudId, r, g, b])
        self.cloudsHit[avId] += 1

    def setToonTrajectoryAi(self, launchTime, x, y, z, h, p, r, vx, vy, vz):
        self.sendUpdate('setToonTrajectory', [self.air.getAvatarIdFromSender(), launchTime, x, y, z, h, p, r, vx, vy, vz])

    def setToonTrajectory(self, avId, launchTime, x, y, z, h, p, r, vx, vy, vz):
        if avId == localAvatar.doId:
            return
        startPos = Vec3(x, y, z)
        startHpr = Vec3(h, p, r)
        startVel = Vec3(vx, vy, vz)
        startT = globalClockDelta.networkToLocalTime(launchTime, bits=31) + 0.2
        trajectory = Trajectory.Trajectory(0.0, startPos, startVel)
        self._avId2trajectoryInfo[avId] = ScratchPad(startPos=startPos, startHpr=startHpr, startVel=startVel, startT=startT, trajectory=trajectory)
   
    def updateToonTrajectoryStartVelAi(self, vx, vy, vz):
        avId = self.air.getAvatarIdFromSender()
        self.sendUpdate('updateToonTrajectoryStartVel', [avId, vx, vy, vz])

    def updateToonTrajectoryStartVel(self, avId, vx, vy, vz):
        if avId == localAvatar.doId:
            return
        if avId in self._avId2trajectoryInfo:
            self._avId2trajectoryInfo[avId].trajectory.setStartVel(Vec3(vx, vy, vz))