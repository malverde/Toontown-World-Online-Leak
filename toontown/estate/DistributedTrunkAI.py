from direct.directnotify import DirectNotifyGlobal
from toontown.estate.DistributedClosetAI import DistributedClosetAI
from toontown.toon import ToonDNA
from ClosetGlobals import *

N_A = 0
class DistributedTrunkAI(DistributedClosetAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedTrunkAI")
    
    def enterAvatar(self):
        avId = self.air.getAvatarIdFromSender()
        if self.inUse:
            self.sendUpdate('freeAvatar')
            return
            
        ownerAv = self.air.doId2do.get(self.ownerId)
        if not ownerAv:
            return
                
        av = self.air.doId2do.get(avId)
        if av:
            self.oldDnaStr = av.dna.makeNetString()
            self.d_setState(OPEN, avId, av.getStyle().getGender(), ownerAv.getHatList() + [0, 0, 0],
                            ownerAv.getGlassesList() + [0, 0, 0], ownerAv.getBackpackList() + [0, 0, 0],
                            ownerAv.getShoesList() + [0, 0, 0])
            self.setInUse(avId)
            self.resetTimeout()
            
    def d_setState(self, mode, avId, gender = '', hatList = [], glassesList = [], backpackList = [], shoesList = []):
        self.sendUpdate('setState', [mode, avId, self.ownerId, gender, hatList, glassesList, backpackList, shoesList])

    def removeItem(self, geom, texture, color, which):
        self.resetTimeout()
        currAv = self.air.doId2do.get(self.currAvId)
        if currAv:
            c2b = {1:(currAv.b_setHatList,currAv.getHatList),2:(currAv.b_setGlassesList,currAv.getGlassesList),4:(currAv.b_setBackpackList,currAv.getBackpackList),8:(currAv.b_setShoesList,currAv.getShoesList)}
            if currAv.removeItemInAccessoriesList(which, geom, texture, color) == 1:
                c2b[which][0](c2b[which][1]())
            

    def setDNA(self, hatIdx, hatTexture, hatColor,
               glassesIdx, glassesTexture, glassesColor,
               backpackIdx, backpackTexture, backpackColor,
               shoesIdx, shoesTexture, shoesColor,
               finished, which):      
        self.resetTimeout()
        currAv = self.air.doId2do.get(self.currAvId)
        if currAv:
            dna = currAv.getStyle()
            if finished == 2 and which > 0:
                # changed
                if which & ToonDNA.HAT:
                    item = dna.hat
                    if currAv.replaceItemInAccessoriesList(ToonDNA.HAT, hatIdx, hatTexture, hatColor, item[0], item[1], item[2]) == 1:
                        currAv.b_setHatList(currAv.getHatList())
                        self.__update(currAv, ToonDNA.HAT, (hatIdx, hatTexture, hatColor))
                        
                elif which & ToonDNA.GLASSES:
                    item = dna.glasses
                    if currAv.replaceItemInAccessoriesList(ToonDNA.GLASSES, glassesIdx, glassesTexture, glassesColor, item[0], item[1], item[2]) == 1:
                        currAv.b_setGlassesList(currAv.getGlassesList())
                        self.__update(currAv, ToonDNA.GLASSES, (glassesIdx, glassesTexture, glassesColor))
                        
                elif which & ToonDNA.BACKPACK:
                    item = dna.backpack
                    if currAv.replaceItemInAccessoriesList(ToonDNA.BACKPACK, backpackIdx, backpackTexture, backpackColor, item[0], item[1], item[2]) == 1:
                        currAv.b_setBackpackList(currAv.getBackpackList())
                        self.__update(currAv, ToonDNA.BACKPACK, (backpackIdx, backpackTexture, backpackColor))
                        
                elif which & ToonDNA.SHOES:
                    item = dna.shoes
                    if currAv.replaceItemInAccessoriesList(ToonDNA.SHOES, shoesIdx, shoesTexture, shoesColor, item[0], item[1], item[2]) == 1:
                        currAv.b_setShoesList(currAv.getShoesList())
                        self.__update(currAv, ToonDNA.SHOES, (shoesIdx, shoesTexture, shoesColor))
                        
                self.d_setMovie(CLOSET_MOVIE_COMPLETE, self.currAvId)
                self.d_setState(CLOSED, self.currAvId)
                self.setFree()
                self.timer.stop()
                
            elif finished == 1:
                # canceled
                currAv.b_setDNAString(self.oldDnaStr)
                
                self.d_setMovie(CLOSET_MOVIE_COMPLETE, self.currAvId)
                self.d_setState(CLOSED, self.currAvId)
                self.setFree()
                self.timer.stop()
                
            else:
                # swapping
                if which == ToonDNA.HAT:
                    li = (hatIdx, hatTexture, hatColor)
                    self.sendUpdate('setCustomerDNA', [self.currAvId, li[0],li[1],li[2],N_A,N_A,N_A,N_A,N_A,N_A,N_A,N_A,N_A,ToonDNA.HAT])
                    
                elif which == ToonDNA.GLASSES:
                    li = (glassesIdx, glassesTexture, glassesColor)
                    self.sendUpdate('setCustomerDNA', [self.currAvId, N_A,N_A,N_A,li[0],li[1],li[2],N_A,N_A,N_A,N_A,N_A,N_A,ToonDNA.GLASSES])
                    
                elif which == ToonDNA.BACKPACK:
                    li = (backpackIdx, backpackTexture, backpackColor)
                    self.sendUpdate('setCustomerDNA', [self.currAvId, N_A,N_A,N_A,N_A,N_A,N_A,li[0],li[1],li[2],N_A,N_A,N_A,ToonDNA.BACKPACK])
                    
                elif which == ToonDNA.SHOES:
                    li = (shoesIdx, shoesTexture, shoesColor)
                    self.sendUpdate('setCustomerDNA', [self.currAvId, N_A,N_A,N_A,N_A,N_A,N_A,N_A,N_A,N_A,li[0],li[1],li[2],ToonDNA.SHOES])
                        
    def __update(self, currAv, mode, args):
        dna = currAv.getStyle()
        
        if mode == ToonDNA.HAT:
            dna.hat = args
            
        elif mode == ToonDNA.GLASSES:
            dna.glasses = args
            
        elif mode == ToonDNA.BACKPACK:
            dna.backpack = args
        
        elif mode == ToonDNA.SHOES:
            dna.backpack = shoes

        currAv.b_setDNAString(dna.makeNetString())
        