from direct.showbase.PythonUtil import invertDict
from toontown.coghq import LabotOfficeFloor_01a_Cogs
from toontown.coghq import LabotOfficeFloor_01b_Cogs
from toontown.coghq import NullCogs
from toontown.toonbase import ToontownGlobals


def getLawOfficeFloorSpecModule(floorId):
    return LawbotOfficeSpecModules[floorId]


def getCogSpecModule(floorId):
    floor = LawbotOfficeFloorId2FloorName[roomId]
    return CogSpecModules.get(floorId, NullCogs)


def getNumBattles(floorId):
    return floorId2numBattles[floorId]

LawbotOfficeFloorId2FloorName = {
    0: 'LabotOfficeFloor_01_a',
    1: 'LabotOfficeFloor_01_b' }
LawbotOfficeFloorName2FloorId = invertDict(LawbotOfficeFloorId2FloorName)
LawbotOfficeEntranceIDs = (0, 1)
LawbotOfficeFloorIDs = (0, 1)
LawbotOfficeSpecModules = {}
for roomName, roomId in LawbotOfficeFloorName2FloorId.items():
    LawbotOfficeSpecModules[roomId] = __import__('toontown.coghq.' + roomName)

CogSpecModules = {
    'CashbotMintBoilerRoom_Battle00': LabotOfficeFloor_01a_Cogs,
    'CashbotMintBoilerRoom_Battle01': LabotOfficeFloor_01b_Cogs }
floorId2numBattles = { }
for (roomName, roomId) in LawbotOfficeFloorName2FloorId.items():
    if roomName not in CogSpecModules:
        floorId2numBattles[roomId] = 0
        continue
    cogSpecModule = CogSpecModules[roomName]
    floorId2numBattles[roomId] = len(cogSpecModule.BattleCells)

