from toontown.coghq import CogDisguiseGlobals

suitTrackIndex = {
's' : 3,
'm' : 2,
'l' : 1,
'c' : 0
}

class CogSuitManagerAI:
    def __init__(self, air):
        self.air = air

    def recoverPart(self, toon, factoryType, suitTrack, zoneId, toons):
        recoveredParts = [0, 0, 0, 0]
        parts = toon.getCogParts()
        suitTrack = suitTrackIndex[suitTrack]
        if CogDisguiseGlobals.isSuitComplete(parts, suitTrack):
            return recoveredParts
        recoveredParts[suitTrack] = toon.giveGenericCogPart(factoryType, suitTrack)
        return recoveredParts

    def removeParts(self, toon, suitDept):
        parts = toon.getCogParts()
        if CogDisguiseGlobals.isSuitComplete(parts, suitDept):
            toon.loseCogParts(suitDept)
