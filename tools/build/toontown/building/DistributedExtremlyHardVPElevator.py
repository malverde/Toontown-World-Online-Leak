from toontown.building.DistributedVPElevator import DistributedVPElevator
from toontown.toonbase import TTLocalizer


class DistributedExtremlyHardVPElevator(DistributedVPElevator):
    notify = directNotify.newCategory('DistributedExtremlyHardVPElevator')

    def setupElevator(self):
        pass

    def getDestName(self):
        return TTLocalizer.ElevatorBrutalSellBotBoss
