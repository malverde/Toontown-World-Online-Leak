from otp.ai.AIBaseGlobal import *
from direct.directnotify import DirectNotifyGlobal
import random
from toontown.suit import SuitDNA
import CogDisguiseGlobals

class CogSuitManagerAI:
    notify = DirectNotifyGlobal.directNotify.newCategory('CogSuitManagerAI')

    def __init__(self, air):
        self.air = air

    def recoverPart(self, av, factoryType, suiTTWack, zoneId, avList):
        partsRecovered = [0,
         0,
         0,
         0]
        part = av.giveGenericCogPart(factoryType, suiTTWack)
        if part:
            partsRecovered[CogDisguiseGlobals.dept2deptIndex(suiTTWack)] = part
            self.air.questManager.toonRecoveredCogSuitPart(av, zoneId, avList)
        return partsRecovered
