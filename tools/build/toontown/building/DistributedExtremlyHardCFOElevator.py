from toontown.building.DistributedCFOElevator import DistributedCFOElevator
from toontown.toonbase import TTLocalizer


class DistributedExtremlyHardCFOElevator(DistributedCFOElevator):
    notify = directNotify.newCategory('DistributedExtremlyHardCFOElevator')

    def setupElevator(self):
        pass

    def getDestName(self):
        return TTLocalizer.ElevatorBrutalCashBotBoss