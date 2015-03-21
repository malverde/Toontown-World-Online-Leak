from toontown.building.DistributedVPElevatorAI import DistributedVPElevatorAI


class DistributedExtremlyHardVPElevatorAI(DistributedVPElevatorAI):
    notify = directNotify.newCategory('DistributedExtremlyHardVPElevatorAI')

    def sendAvatarsToDestination(self, avIdList):
        if len(avIdList) > 0:
            bossZone = self.bldg.createBossOffice(avIdList, isBrutal=True)
            for avId in avIdList:
                if avId:
                    self.sendUpdateToAvatarId(avId, 'setBossOfficeZoneForce', [bossZone])
