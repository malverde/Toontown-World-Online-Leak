from toontown.building.DistributedVPElevatorAI import DistributedVPElevatorAI


class DistributedBrutalVPElevatorAI(DistributedVPElevatorAI):
    notify = directNotify.newCategory('DistributedBrutalVPElevatorAI')

    def sendAvatarsToDestination(self, avIdList):
        if len(avIdList) > 0:
            bossZone = self.bldg.createBossOffice(avIdList, isBrutal=True)
            for avId in avIdList:
                if avId:
                    self.sendUpdateToAvatarId(avId, 'setBossOfficeZoneForce', [bossZone])
