from direct.directnotify import DirectNotifyGlobal
from direct.fsm.FSM import FSM
import PetUtil, PetDNA, PetNameGenerator
from toontown.hood import ZoneUtil
from toontown.building import PetshopBuildingAI
from toontown.toonbase import ToontownGlobals
import random
import cPickle, time, random, os

MINUTE = 60
HOUR = 60 * MINUTE
DAY = 24 * HOUR

def getDayId():
    return int(time.time() // DAY)
    
class PetManagerAI:
    NUM_DAILY_PETS = 5 
    cachePath = config.GetString('air-pet-cache', 'astron/databases/air_cache/')
    def __init__(self, air):
        self.air = air
        self.cacheFile = '%spets_%d.pets' % (self.cachePath, self.air.districtId)
        if os.path.isfile(self.cacheFile):
            with open(self.cacheFile, 'rb') as f:
                data = f.read()
                
            self.seeds = cPickle.loads(data)
            if self.seeds.get('day', -1) != getDayId() or len(self.seeds.get(ToontownGlobals.ToontownCentral, [])) != self.NUM_DAILY_PETS:
                self.generateSeeds()
            
        else:
            self.generateSeeds()
            
        self.nameGen = PetNameGenerator.PetNameGenerator()        
        
    def generateSeeds(self):
        seeds = range(0, 255)
        random.shuffle(seeds)
        
        self.seeds = {}
        for hood in (ToontownGlobals.ToontownCentral, ToontownGlobals.DonaldsDock, ToontownGlobals.DaisyGardens,
                     ToontownGlobals.MinniesMelodyland, ToontownGlobals.TheBrrrgh, ToontownGlobals.DonaldsDreamland,
                     ToontownGlobals.FunnyFarm):
            self.seeds[hood] = [seeds.pop() for _ in xrange(self.NUM_DAILY_PETS)]
            
        self.seeds['day'] = getDayId()
            
        with open(self.cacheFile, 'wb') as f:
             f.write(cPickle.dumps(self.seeds))

        
    def getAvailablePets(self, seed, safezoneId):
        if self.seeds.get('day', -1) != getDayId():
            self.generateSeeds()
            
        return self.seeds.get(safezoneId, [seed])

    def createNewPetFromSeed(self, avId, seed, nameIndex, gender, safeZoneId):
        av = self.air.doId2do[avId]
        
        name = self.nameGen.getName(nameIndex)
        _, dna, traitSeed = PetUtil.getPetInfoFromSeed(seed, safeZoneId)
        head, ears, nose, tail, body, color, cs, eye, _ = dna
        numGenders = len(PetDNA.PetGenders)
        gender %= numGenders
                
        fields = {'setOwnerId' : avId, 'setPetName' : name, 'setTraitSeed' : traitSeed, 'setSafeZone' : safeZoneId,
                  'setHead' : head, 'setEars' : ears, 'setNose' : nose, 'setTail' : tail, 'setBodyTexture' : body,
                  'setColor' : color, 'setColorScale' : cs, 'setEyeColor' : eye, 'setGender' : gender}
                  
        def response(doId):
            if not doId:
                self.air.notify.warning("Cannot create pet for %s!" % avId)
                return
                
            self.air.writeServerEvent('bought-pet', avId, doId)
            av.b_setPetId(doId)
            
        self.air.dbInterface.createObject(self.air.dbId, self.air.dclassesByName['DistributedPetAI'],
                                          {k: (v,) for k,v in fields.items()}, response)
        
    def deleteToonsPet(self, avId):
        av = self.air.doId2do[avId]
        pet = av.getPetId()
        if pet:
            if pet in self.air.doId2do:
                self.air.doId2do[pet].requestDelete()
                
        av.b_setPetId(0)