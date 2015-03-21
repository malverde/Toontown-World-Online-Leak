from toontown.building.DistributedCFOElevatorAI import DistributedCFOElevatorAI


class DistributedExtremlyHardCFOElevatorAI(DistributedCFOElevatorAI):
    notify = directNotify.newCategory('DistributedExtremlyHardCFOElevatorAI')

    def sendAvatarsToDestination(self, avIdList):
        if len(avIdList) > 0:
            bossZone = self.bldg.createBossOffice(avIdList, isBrutal=True)
            for avId in avIdList:
                if avId:
                    self.sendUpdateToAvatarId(avId, 'setBossOfficeZoneForce', [bossZone])