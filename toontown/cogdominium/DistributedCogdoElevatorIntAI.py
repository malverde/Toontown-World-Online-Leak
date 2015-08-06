#Embedded file name: toontown.cogdominium.DistributedCogdoElevatorIntAI
from direct.directnotify.DirectNotifyGlobal import directNotify
from toontown.building.DistributedElevatorIntAI import DistributedElevatorIntAI

class DistributedCogdoElevatorIntAI(DistributedElevatorIntAI):
    notify = directNotify.newCategory('DistributedCogdoElevatorIntAI')
