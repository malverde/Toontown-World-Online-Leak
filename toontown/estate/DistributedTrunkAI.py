from toontown.estate.DistributedClosetAI import DistributedClosetAI
from toontown.toon.ToonDNA import ToonDNA, HAT, GLASSES, BACKPACK, SHOES
from toontown.estate import ClosetGlobals

from direct.distributed.ClockDelta import globalClockDelta


class DistributedTrunkAI(DistributedClosetAI):
    notify = directNotify.newCategory('DistributedTrunkAI')

    def __init__(self, air, furnitureMgr, itemType):
        DistributedClosetAI.__init__(self, air, furnitureMgr, itemType)

        self.hatList = []
        self.glassesList = []
        self.backpackList = []
        self.shoesList = []

        self.removedHats = []
        self.removedGlasses = []
        self.removedBackpacks = []
        self.removedShoes = []

    def generate(self):
        if self.furnitureMgr.ownerId:
            owner = self.air.doId2do.get(self.furnitureMgr.ownerId)

            if owner:
                self.hatList = owner.hatList
                self.glassesList = owner.glassesList
                self.backpackList = owner.backpackList
                self.shoesList = owner.shoesList
                self.gender = owner.dna.gender
            else:
                self.air.dbInterface.queryObject(self.air.dbId, self.furnitureMgr.ownerId, self.__gotOwner)

    def __gotOwner(self, dclass, fields):
        if dclass != self.air.dclassesByName['DistributedToonAI']:
            self.notify.warning('Got object of wrong type!')
            return

        self.hatList = fields['setHatList'][0]
        self.glassesList = fields['setGlassesList'][0]
        self.backpackList = fields['setBackpackList'][0]
        self.shoesList = fields['setShoesList'][0]
        dna = ToonDNA(str=fields['setDNAString'][0])
        self.gender = dna.gender

    def __verifyAvatarInMyZone(self, av):
        return av.getLocation() == self.getLocation()

    def setState(self, mode, avId, ownerId, gender, hatList, glassesList, backpackList, shoesList):
        self.sendUpdate('setState', [mode, avId, ownerId, gender, hatList, glassesList, backpackList, shoesList])

    def removeItem(self, itemIdx, textureIdx, colorIdx, which):
        avId = self.air.getAvatarIdFromSender()

        if avId != self.furnitureMgr.ownerId:
            self.air.writeServerEvent('suspicious', avId=avId,
                                      issue='Tried to remove item from someone else\'s closet!')
            return

        if not self.verifyCustomer(avId):
            self.air.writeServerEvent('suspicious', avId=avId,
                                      issue='Tried to remove item while not interacting with closet!')
            return

        av = self.air.doId2do.get(avId)

        if not av:
            self.air.writeServerEvent('suspicious', avId=avId,
                                      issue='Tried to interact with a closet from another shard!')
            return

        if which == HAT:
            self.removedHats.append((itemIdx, textureIdx, colorIdx))
        elif which == GLASSES:
            self.removedGlasses.append((itemIdx, textureIdx, colorIdx))
        elif which == BACKPACK:
            self.removedBackpacks.append((itemIdx, textureIdx, colorIdx))
        elif which == SHOES:
            self.removedShoes.append((itemIdx, textureIdx, colorIdx))

    def setDNA(self, hatIdx, hatTexture, hatColor, glassesIdx, glassesTexture, glassesColor, backpackIdx,
               backpackTexture, backpackColor, shoesIdx, shoesTexture, shoesColor, finished, which):
        avId = self.air.getAvatarIdFromSender()

        if not self.verifyCustomer(avId):
            self.air.writeServerEvent('suspicious', avId, 'Tried to set DNA from closet while not using it!')
            return

        av = self.air.doId2do.get(avId)

        if not av:
            self.air.writeServerEvent('suspicious', avId, 'Interacted with a closet from another shard!')
            return

        if not self.__verifyAvatarInMyZone(av):
            self.air.writeServerEvent('suspicious', avId, 'Tried to setDNA while in another zone!')
            return

        if not finished:
            # They changed one of their accessories.
            if which == HAT:
                av.b_setHat(hatIdx, hatTexture, hatColor)
            if which == GLASSES:
                av.b_setGlasses(glassesIdx, glassesTexture, glassesColor)
            if which == BACKPACK:
                av.b_setBackpack(backpackIdx, backpackTexture, backpackColor)
            if which == SHOES:
                av.b_setShoes(shoesIdx, shoesTexture, shoesColor)
        elif finished == 1:
            # The user pressed the cancel button. All we need to do is free him.
            # Reset the removed items and our user.
            av.b_setHat(hatIdx, hatTexture, hatColor)
            av.b_setGlasses(glassesIdx, glassesTexture, glassesColor)
            av.b_setBackpack(backpackIdx, backpackTexture, backpackColor)
            av.b_setShoes(shoesIdx, shoesTexture, shoesColor)

            self.removedHats = []
            self.removedGlasses = []
            self.removedBackpacks = []
            self.removedShoes = []
            self.avId = None
            # Free the user.
            self.d_setMovie(ClosetGlobals.CLOSET_MOVIE_COMPLETE, avId, globalClockDelta.getRealNetworkTime())
            self.resetMovie()
            self.setState(ClosetGlobals.CLOSED, 0, self.furnitureMgr.ownerId, self.gender, self.hatList,
                          self.glassesList, self.backpackList, self.shoesList)
        elif finished == 2:
            # They are done using the trunk. Update their removed items.
            # Is the user actually the owner?
            if avId != self.furnitureMgr.ownerId:
                self.air.writeServerEvent('suspicious', avId,
                                          'Tried to set their clothes from somebody else\'s closet!')
                return

            # Put on the accessories they want...
            if which & HAT:
                av.b_setHat(hatIdx, hatTexture, hatColor)
            if which & GLASSES:
                av.b_setGlasses(glassesIdx, glassesTexture, glassesColor)
            if which & BACKPACK:
                av.b_setBackpack(backpackIdx, backpackTexture, backpackColor)
            if which & SHOES:
                av.b_setShoes(shoesIdx, shoesTexture, shoesColor)

            # Delete all their items they want to be deleted...
            for hat in self.removedHats:
                id, texture, color = hat
                av.removeItemInAccessoriesList(HAT, id, texture, color)
            for glasses in self.removedGlasses:
                id, texture, color = glasses
                av.removeItemInAccessoriesList(GLASSES, id, texture, color)
            for backpack in self.removedBackpacks:
                id, texture, color = backpack
                av.removeItemInAccessoriesList(BACKPACK, id, texture, color)
            for shoe in self.removedShoes:
                id, texture, color = shoe
                av.removeItemInAccessoriesList(SHOES, id, texture, color)

            # Regenerate the available accessories...
            self.removedHats = []
            self.removedGlasses = []
            self.removedBackpacks = []
            self.removedShoes = []
            self.generate()

            # Release the customer
            self.releaseCustomer()

            # We are done, free the user!
            self.d_setMovie(ClosetGlobals.CLOSET_MOVIE_COMPLETE, avId, globalClockDelta.getRealNetworkTime())
            self.resetMovie()
            self.setState(ClosetGlobals.CLOSED, 0, self.furnitureMgr.ownerId, self.gender, self.hatList,
                          self.glassesList, self.backpackList, self.shoesList)

    def enterAvatar(self):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)

        if not av:
            self.air.writeServerEvent('suspicious', avId=avId, issue='Not in same shard as closet!')
            return

        if not self.__verifyAvatarInMyZone(av):
            self.air.writeServerEvent('suspicious', avId=avId, issue='Not in same zone as closet!')
            return

        if not self.occupy(avId):
            self.sendUpdateToAvatarId(avId, 'freeAvatar', [])
            return

        self.setState(ClosetGlobals.OPEN, avId, self.furnitureMgr.ownerId, self.gender, self.hatList, self.glassesList,
                      self.backpackList, self.shoesList)
