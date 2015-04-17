import random


class PetManagerAI:
    def __init__(self, air):
        self.air = air

    def getAvailablePets(self, numPets=5):
        return random.sample(xrange(256), numPets)

    def createNewPetFromSeed(self, avId, petSeeds, nameIndex, gender, safeZoneId):
        pass # TODO
