import random
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
import os
from direct.showbase import AppRunnerGlobal
from direct.directnotify import DirectNotifyGlobal
from pandac.PandaModules import *
import PetNameMasterEnglish

class PetNameGenerator:
    notify = DirectNotifyGlobal.directNotify.newCategory('PetNameGenerator')
    boyFirsts = []
    girlFirsts = []
    neutralFirsts = []

    def __init__(self):
        self.generateLists()

    def generateLists(self):
        self.boyFirsts = []
        self.girlFirsts = []
        self.neutralFirsts = []
        self.nameDictionary = {}
        contents = PetNameMasterEnglish.NAMES
        if not contents:
            self.notify.error('PetNameGenerator: Error opening name list text file.')        
        lines = contents.split('\n')
        for line in lines:
            if line is not None:
                if line.lstrip()[0:1] != '#':
                    a1 = line.find('*')
                    a2 = line.find('*', a1 + 1)
                    self.nameDictionary[int(line[0:a1])] = (int(line[a1 + 1:a2]), line[a2 + 1:len(line)].strip())

        masterList = [self.boyFirsts, self.girlFirsts, self.neutralFirsts]
        for tu in self.nameDictionary.values():
            masterList[tu[0]].append(tu[1])

        return 1

    def getName(self, uniqueID):
        try:
            return self.nameDictionary[uniqueID][1]
        except:
            return self.nameDictionary[0][1]

    def returnUniqueID(self, name):
        newtu = [(), (), ()]
        newtu[0] = (0, name)
        newtu[1] = (1, name)
        newtu[2] = (2, name)
        for tu in self.nameDictionary.items():
            for g in newtu:
                if tu[1] == g:
                    return tu[0]

        return -1

    def randomName(self, gender = None, seed = None):
        S = random.getstate()
        if seed is not None:
            random.seed(seed)
        if gender is None:
            gender = random.choice([0, 1])
        retString = ''
        firstList = self.neutralFirsts[:]
        if gender == 0:
            firstList += self.boyFirsts
        elif gender == 1:
            firstList += self.girlFirsts
        else:
            self.error('Must be boy or girl.')
        retString += random.choice(firstList)
        random.setstate(S)
        return retString