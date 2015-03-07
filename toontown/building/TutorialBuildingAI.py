from toontown.building import DistributedDoorAI
from toontown.building import DoorTypes
from toontown.building.DistributedTutorialInteriorAI import DistributedTutorialInteriorAI


class TutorialBuildingAI:
    def __init__(self, air, exteriorZone, interiorZone, blockNumber, tutorialNpcId):
        self.air = air
        self.exteriorZone = exteriorZone
        self.interiorZone = interiorZone
        self.blockNumber = blockNumber
        self.tutorialNpcId = tutorialNpcId

        self.interior = DistributedTutorialInteriorAI(
            self.air, self.blockNumber, self.interiorZone, self.tutorialNpcId)
        self.interior.generateWithRequired(self.interiorZone)

        self.door = DistributedDoorAI.DistributedDoorAI(
            self.air, blockNumber, DoorTypes.EXT_STANDARD)
        self.insideDoor = DistributedDoorAI.DistributedDoorAI(
            self.air, blockNumber, DoorTypes.INT_STANDARD)
        self.door.setOtherDoor(self.insideDoor)
        self.insideDoor.setOtherDoor(self.door)
        self.door.zoneId = self.exteriorZone
        self.insideDoor.zoneId = self.interiorZone
        self.door.generateWithRequired(self.exteriorZone)
        self.insideDoor.generateWithRequired(self.interiorZone)

    def cleanup(self):
        self.door.requestDelete()
        del self.door
        self.insideDoor.requestDelete()
        del self.insideDoor
        self.interior.requestDelete()
        del self.interior
