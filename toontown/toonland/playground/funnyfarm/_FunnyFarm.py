########################## THE TOON LAND PROJECT ##########################
# Filename: _FunnyFarm.py
# Created by: Mark/Doctor Leroy (February 2nd, 2013)
####
# Description:
#
# The Funny Farm added Python implementation.
####

from pandac.PandaModules import *
from random import randint
from otp.otpbase import OTPGlobals

def loadPicnicTable(objectId, tn, seed, *posHpr):
    from toontown.toon.LocalToon import globalClockDelta
    picnicTable = DistributedPicnicBasket.DistributedPicnicBasket(base.cr)
    picnicTable.objectId = objectId
    picnicTable.doId = picnicTable.objectId
    picnicTable.generateInit()
    picnicTable.generate()
    picnicTable.setTableNumber(tn)
    picnicTable.setPosHpr(*posHpr)
    picnicTable.announceGenerate()
    if picnicTable.activeState != 6:
        picnicTable.activeState = 6
    ts = globalClockDelta.getFrameNetworkTime()
    picnicTable.setState('waitEmpty', seed, ts)
    TTSendBuffer.TTSendBuffer.networking_objects[objectId] = picnicTable
    TTSendBuffer.TTSendBuffer.temporary_objects.append(objectId)

def loadCabinHouse(objectId, houseIndex, houseName, nameText, *scale):
    from toontown.estate import DistributedHouse
    from toontown.estate import HouseGlobals
    houseObject = DistributedHouse.DistributedHouse(base.cr)
    houseObject.objectId = objectId
    houseObject.doId = houseObject.objectId
    houseObject.generateInit()
    houseObject.generate()
    houseObject.setHousePos(houseIndex)
    houseObject.setHouseType(0)
    houseObject.setAvatarId(base.localAvatar.doId)
    houseObject.setName(houseName)
    houseObject.setColor((len(HouseGlobals.houseColors) - 3) + houseIndex)
    houseObject.announceGenerate()
    if houseObject.activeState != 6:
        houseObject.activeState = 6
    houseObject.load()
    houseObject.nameText.setText(nameText)
    houseObject.house.setScale(*scale)
    TTSendBuffer.TTSendBuffer.networking_objects[objectId] = houseObject
    TTSendBuffer.TTSendBuffer.temporary_objects.append(objectId)

def loadBuildingDoor(objectId, nodePath, doorModelName, color, scale):
    from libtoontown import DNADoor
    dnaStore = base.cr.playGame.dnaStore
    if doorModelName[-1:] == 'r':
        doorModelName = doorModelName[:-1] + 'l'
    else:
        doorModelName = doorModelName[:-1] + 'r'
    door = dnaStore.findNode(doorModelName)
    door_origin = nodePath.find('**/*door_origin')
    door_origin.setPos(door_origin, 0, -0.01, 0)
    door_origin.setScale(scale)
    doorNP = door.copyTo(door_origin)
    DNADoor.setupDoor(doorNP, door_origin, door_origin,
     dnaStore, str(objectId), color)

safe_zone = render.find('**/%d:safe_zone' % PlaygroundGlobals.FUNNY_FARM)
tunnelNp = render.find('**/linktunnel_ff_19201_DNARoot')
tunnelNp.find('**/sign').hide()
tunnelNp.find('**/chip_dale').hide()
tunnelOrigin = tunnelNp.find('**/tunnel_origin')
_POS = tunnelOrigin.getPos(safe_zone)
_HPR = tunnelOrigin.getHpr(safe_zone)
birdNp = safe_zone.attachNewNode('linktunnel_ff_19201_DNARoot_bird')
birdNp.setPosHpr((_POS[0] + 5), (_POS[1] - 5), _POS[2], (_HPR[0] - 180), _HPR[1], _HPR[2])
birdNp.setScale(350)
birdNp.setZ(45)
loader.loadModel('phase_5/models/props/bird').reparentTo(birdNp)

collisionBlocker = safe_zone.attachNewNode('collision_blocker_1')
collisionBlocker.setPos(113.921, 82.753, 10.026)
cs = CollisionSphere(0.0, 0.0, 3.0, 8.0)
cn = CollisionNode('collision_blocker_1')
cn.addSolid(cs)
cn.setIntoCollideMask(OTPGlobals.WallBitmask)
collisionBlocker.attachNewNode(cn)
collisionBlocker = safe_zone.attachNewNode('collision_blocker_2')
collisionBlocker.setPos(64.083, 120.748, 10.026)
cs = CollisionSphere(0.0, 0.0, 3.0, 17.0)
cn = CollisionNode('collision_blocker_2')
cn.addSolid(cs)
cn.setIntoCollideMask(OTPGlobals.WallBitmask)
collisionBlocker.attachNewNode(cn)
collisionBlocker = safe_zone.attachNewNode('collision_blocker_3')
collisionBlocker.setPos(49.946, 132.416, 10.026)
cs = CollisionSphere(0.0, 0.0, 3.0, 10.0)
cn = CollisionNode('collision_blocker_3')
cn.addSolid(cs)
cn.setIntoCollideMask(OTPGlobals.WallBitmask)
collisionBlocker.attachNewNode(cn)

loadCabinHouse(4, 0, 'Doctor Leroy', 'Doctor Leroy\'s\nLabratory', 1.1)
loadCabinHouse(5, 1, 'Fluffy', 'Fluffy\'s Dog\nHouse', 1)
loadCabinHouse(6, 2, 'Evil Blinky', 'Evil Blinky\'s\nDen', 1)

trashCan = DistributedTrashCan.DistributedTrashCan(base.cr, 3, parent=safe_zone)
trashCan.setPosHpr(72, 30, 10.025, -812, 0, 0)
trashCan.setScale(1.1)
TTSendBuffer.TTSendBuffer.networking_objects[trashCan.objectId] = trashCan
TTSendBuffer.TTSendBuffer.temporary_objects.append(trashCan.objectId)

dgaFountain = DistributedFountain.DistributedFountain(base.cr, 7)
dgaFountain.reparentTo(safe_zone)
dgaFountain.setPosHpr(41, 12, 10.026, 0, 0, 0)
dgaFountain.setScale(1.2)
dgaFountain.generate()
TTSendBuffer.TTSendBuffer.networking_objects[dgaFountain.objectId] = dgaFountain
TTSendBuffer.TTSendBuffer.temporary_objects.append(dgaFountain.objectId)
base.cr.doId2do[7] = dgaFountain

nodePath = render.find('**/prop_quest_landmark_1_DNARoot')
loadBuildingDoor(8, nodePath, 'door_double_curved_ur', Vec4(0.88, 0.45, 0.38, 1), 1)
nodePath = render.find('**/prop_quest_landmark_2_DNARoot')
loadBuildingDoor(9, nodePath, 'door_double_curved_ul', Vec4(1, 0.63, 0.38, 1), 1)
door_types  = ['door_double_curved_u', 'door_double_square_u', 'door_double_square_u']
door_colors = [(1, 0.87, 0.38, 1), (1, 0.63, 0.38, 1), (0.88, 0.45, 0.38, 1)]
buildingNodeNum = 0
for buildingNode in safe_zone.findAllMatches('**/prop_landmark_FF_DNARoot'):
    typeIndex  = buildingNodeNum % len(door_types)
    colorIndex = buildingNodeNum % len(door_colors)
    objectId = buildingNodeNum + 10
    R, G, B, A = door_colors[colorIndex]
    doorType = door_types[typeIndex] + choice(randint(0, 1), 'r', 'l')
    loadBuildingDoor(objectId, buildingNode, doorType, Vec4(R, G, B, A), 1)
    buildingNodeNum += 1

device = loader.loadModel('phase_4/models/props/tt_m_prp_acs_sillyReader')
device.reparentTo(safe_zone)
device.setPos(-81.5, 61.4, 17.8)
device.setScale(2.1)
device.hprInterval(8.0, Vec3(0, 270, 0), Vec3(360, 270, 0)).loop()
device.find('**/sillyReader').setX(1.4)
device = loader.loadModel('phase_4/models/props/tt_m_prp_acs_sillyReader')
device.reparentTo(safe_zone)
device.setPos(-68, 70, 17.8)
device.setScale(2.1)
device.hprInterval(8.0, Vec3(0, 270, 0), Vec3(360, 270, 0)).loop()
device.find('**/sillyReader').setX(1.4)

toonHall = loader.loadModel('phase_3.5/models/modules/tt_m_ara_int_toonhall.bam')
tallSpaceLamp = toonHall.find('**/prop_tallLamp_space').copyTo(safe_zone)
spaceLamp = toonHall.find('**/prop_lamp_space').copyTo(safe_zone)
for nodePath in (tallSpaceLamp.findAllMatches('**/tallLamp') + tallSpaceLamp.findAllMatches('**/collision')):
    nodePath.setPos(76, -22, 0)
for nodePath in (spaceLamp.findAllMatches('**/lamp') + spaceLamp.findAllMatches('**/collision')):
    nodePath.setPos(76.6, -36, -2.45)
tallSpaceLamp.setPos(-75, 74, 12)
tallSpaceLamp.setScale(1.2)
spaceLamp.setPos(-86.5, 67.5, 15.8)
spaceLamp.setH(180)

collisionBlocker = safe_zone.attachNewNode('collision_blocker_1')
collisionBlocker.setPos(-90, 62, 10)
cs = CollisionSphere(0.0, 0.0, 3.0, 5.0)
cn = CollisionNode('collision_blocker_1')
cn.addSolid(cs)
cn.setIntoCollideMask(OTPGlobals.WallBitmask)
collisionBlocker.attachNewNode(cn)

toonHq = render.find('**/sz20:toon_landmark_hqFF_DNARoot')
for doorFrameHole in toonHq.findAllMatches('**/doorFrameHole*'):
    doorFrameHole.hide()

posHpr = [(81, 7, 0.026, 0, 0, 0), (52, 46, 0.026, 40, 0, 0), (45, -8, 0.026, 60, 0, 0)]
for tn in range(3):
    X, Y, Z, H, P, R = posHpr[tn]
    loadPicnicTable(tn, (tn + 1), tn, X, Y, Z, H, P, R)

safe_zone.find('**/*statue*').removeNode()

filepath = '%s/toonland/playground/funnyfarm/maps' % __filebase__
tunnelAheadSign = loader.loadTexture('%s/tt_t_ara_gen_tunnelAheadSign.jpg' % filepath)
safe_zone.find('**/prop_tunnel_ahead_FF_DNARoot').setTexture(tunnelAheadSign, 1)