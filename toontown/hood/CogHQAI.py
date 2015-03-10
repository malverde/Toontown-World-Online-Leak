from toontown.building import DoorTypes
from toontown.building.DistributedBoardingPartyAI import DistributedBoardingPartyAI
from toontown.coghq import DistributedCogHQDoorAI
from toontown.coghq import LobbyManagerAI
from toontown.toonbase import TTLocalizer
from toontown.toonbase import ToontownGlobals


class CogHQAI:
    notify = directNotify.newCategory('CogHQAI')
    notify.setInfo(True)

    def __init__(
            self, air, zoneId, lobbyZoneId, lobbyFADoorCode,
            lobbyElevatorCtor, bossCtor):
        self.air = air
        self.zoneId = zoneId
        self.lobbyZoneId = lobbyZoneId
        self.lobbyFADoorCode = lobbyFADoorCode
        self.lobbyElevatorCtor = lobbyElevatorCtor
        self.bossCtor = bossCtor

        self.lobbyMgr = None
        self.lobbyElevator = None
        self.boardingParty = None

        self.notify.info('Creating objects... ' + self.getLocationName(zoneId))

    def getLocationName(self, zoneId):
        lookupTable = ToontownGlobals.hoodNameMap
        if (zoneId % 1000) != 0:
            lookupTable = TTLocalizer.GlobalStreetNames
        name = lookupTable.get(zoneId, '')
        if isinstance(name, str):
            return name
        return name[2]

    def startup(self):
        self.createLobbyManager()
        self.createLobbyElevator()
        self.extDoor = self.makeCogHQDoor(self.lobbyZoneId, 0, 0, self.lobbyFADoorCode)
        if simbase.config.GetBool('want-boarding-groups', True):
            self.createBoardingParty()

    def createLobbyManager(self):
        self.lobbyMgr = LobbyManagerAI.LobbyManagerAI(self.air, self.bossCtor)
        self.lobbyMgr.generateWithRequired(self.lobbyZoneId)

    def createLobbyElevator(self):
        self.lobbyElevator = self.lobbyElevatorCtor(
            self.air, self.lobbyMgr, self.lobbyZoneId, antiShuffle=1)
        self.lobbyElevator.generateWithRequired(self.lobbyZoneId)

    def makeCogHQDoor(self, destinationZone, intDoorIndex, extDoorIndex, lock=0):
        intDoor = DistributedCogHQDoorAI.DistributedCogHQDoorAI(
            self.air, 0, DoorTypes.INT_COGHQ, self.zoneId,
            doorIndex=intDoorIndex, lockValue=lock)
        intDoor.zoneId = destinationZone

        extDoor = DistributedCogHQDoorAI.DistributedCogHQDoorAI(
            self.air, 0, DoorTypes.EXT_COGHQ, destinationZone,
            doorIndex=extDoorIndex, lockValue=lock)

        extDoor.setOtherDoor(intDoor)
        intDoor.setOtherDoor(extDoor)

        intDoor.generateWithRequired(destinationZone)
        intDoor.sendUpdate('setDoorIndex', [intDoor.getDoorIndex()])

        extDoor.generateWithRequired(self.zoneId)
        extDoor.sendUpdate('setDoorIndex', [extDoor.getDoorIndex()])

        return extDoor

    def createBoardingParty(self):
        self.boardingParty = DistributedBoardingPartyAI(self.air, [self.lobbyElevator.doId], 8)
        self.boardingParty.generateWithRequired(self.lobbyZoneId)
