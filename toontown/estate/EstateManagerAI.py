#Embedded file name: toontown.estate.EstateManagerAI
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.fsm.FSM import FSM
from toontown.estate.DistributedEstateAI import DistributedEstateAI
from toontown.estate.DistributedHouseAI import DistributedHouseAI
from toontown.toon.ToonDNA import ToonDNA
import HouseGlobals
import functools

class LoadHouseFSM(FSM):

    def __init__(self, mgr, estate, houseIndex, toon, callback):
        FSM.__init__(self, 'LoadHouseFSM')
        self.mgr = mgr
        self.estate = estate
        self.houseIndex = houseIndex
        self.toon = toon
        self.callback = callback
        self.done = False

    def start(self):
        if self.toon is None:
            taskMgr.doMethodLater(0.0, self.demand, 'makeBlankHouse-%s' % id(self), extraArgs=['MakeBlankHouse'])
            return
        self.houseId = self.toon.get('setHouseId', [0])[0]
        if self.houseId == 0:
            self.demand('CreateHouse')
        else:
            self.demand('LoadHouse')

    def enterMakeBlankHouse(self):
        self.house = DistributedHouseAI(self.mgr.air)
        self.house.setHousePos(self.houseIndex)
        self.house.setColor(self.houseIndex)
        self.house.generateWithRequired(self.estate.zoneId)
        self.estate.houses[self.houseIndex] = self.house
        self.demand('Off')

    def enterCreateHouse(self):
        self.mgr.air.dbInterface.createObject(self.mgr.air.dbId, self.mgr.air.dclassesByName['DistributedHouseAI'], {'setName': [self.toon['setName'][0]],
         'setAvatarId': [self.toon['ID']]}, self.__handleCreate)

    def __handleCreate(self, doId):
        if self.state != 'CreateHouse':
            return
        av = self.mgr.air.doId2do.get(self.toon['ID'])
        if av:
            av.b_setHouseId(doId)
        else:
            self.mgr.air.dbInterface.updateObject(self.mgr.air.dbId, self.toon['ID'], self.mgr.air.dclassesByName['DistributedToonAI'], {'setHouseId': [doId]})
        self.houseId = doId
        self.demand('LoadHouse')

    def enterLoadHouse(self):
        dna = ToonDNA()
        dna.makeFromNetString(self.toon['setDNAString'][0])
        gender = 1 if dna.getGender() == 'm' else 0
        self.mgr.air.sendActivate(self.houseId, self.mgr.air.districtId, self.estate.zoneId, self.mgr.air.dclassesByName['DistributedHouseAI'], {'setHousePos': [self.houseIndex],
         'setColor': [self.houseIndex],
         'setName': [self.toon['setName'][0]],
         'setAvatarId': [self.toon['ID']],
         'setGender': [gender]})
        self.acceptOnce('generate-%d' % self.houseId, self.__gotHouse)

    def __gotHouse(self, house):
        self.house = house
        self.estate.houses[self.houseIndex] = self.house
        self.demand('Off')

    def exitLoadHouse(self):
        self.ignore('generate-%d' % self.houseId)

    def enterOff(self):
        self.done = True
        self.callback(self.house)


class LoadPetFSM(FSM):

    def __init__(self, mgr, estate, toon, callback):
        FSM.__init__(self, 'LoadPetFSM')
        self.mgr = mgr
        self.estate = estate
        self.toon = toon
        self.callback = callback
        self.done = False

    def start(self):
        self.petId = self.toon['setPetId'][0]
        if self.petId not in self.mgr.air.doId2do:
            self.mgr.air.sendActivate(self.petId, self.mgr.air.districtId, self.estate.zoneId)
            self.acceptOnce('generate-%d' % self.petId, self.__generated)
        else:
            self.__generated(self.mgr.air.doId2do[self.petId])

    def __generated(self, pet):
        self.pet = pet
        self.estate.pets.append(pet)
        self.demand('Off')

    def enterOff(self):
        self.done = True
        self.callback(self.pet)


class LoadEstateFSM(FSM):

    def __init__(self, mgr, callback):
        FSM.__init__(self, 'LoadEstateFSM')
        self.mgr = mgr
        self.callback = callback
        self.estate = None

    def start(self, accountId, zoneId):
        self.accountId = accountId
        self.zoneId = zoneId
        self.demand('QueryAccount')

    def enterQueryAccount(self):
        self.mgr.air.dbInterface.queryObject(self.mgr.air.dbId, self.accountId, self.__gotAccount)

    def __gotAccount(self, dclass, fields):
        if self.state != 'QueryAccount':
            return
        if dclass != self.mgr.air.dclassesByName['AccountAI']:
            self.mgr.notify.warning('Account %d has non-account dclass %d!' % (self.accountId, dclass))
            self.demand('Failure')
            return
        self.accountFields = fields
        self.estateId = fields.get('ESTATE_ID', 0)
        self.demand('QueryToons')

    def enterQueryToons(self):
        self.toonIds = self.accountFields.get('ACCOUNT_AV_SET', [0] * 6)
        self.toons = {}
        for index, toonId in enumerate(self.toonIds):
            if toonId == 0:
                self.toons[index] = None
                continue
            self.mgr.air.dbInterface.queryObject(self.mgr.air.dbId, toonId, functools.partial(self.__gotToon, index=index))

    def __gotToon(self, dclass, fields, index):
        if self.state != 'QueryToons':
            return
        if dclass != self.mgr.air.dclassesByName['DistributedToonAI']:
            self.mgr.notify.warning('Account %d has avatar %d with non-Toon dclass %d!' % (self.accountId, self.toonIds[index], dclass))
            self.demand('Failure')
            return
        fields['ID'] = self.toonIds[index]
        self.toons[index] = fields
        if len(self.toons) == 6:
            self.__gotAllToons()

    def __gotAllToons(self):
        if self.estateId:
            self.demand('LoadEstate')
        else:
            self.demand('CreateEstate')

    def enterCreateEstate(self):
        self.mgr.air.dbInterface.createObject(self.mgr.air.dbId, self.mgr.air.dclassesByName['DistributedEstateAI'], {}, self.__handleEstateCreate)

    def __handleEstateCreate(self, estateId):
        if self.state != 'CreateEstate':
            return
        self.estateId = estateId
        self.demand('StoreEstate')

    def enterStoreEstate(self):
        self.mgr.air.dbInterface.updateObject(self.mgr.air.dbId, self.accountId, self.mgr.air.dclassesByName['AccountAI'], {'ESTATE_ID': self.estateId}, {'ESTATE_ID': 0}, self.__handleStoreEstate)

    def __handleStoreEstate(self, fields):
        if fields:
            self.notify.warning('Failed to associate Estate %d with account %d, loading anyway.' % (self.estateId, self.accountId))
        self.demand('LoadEstate')

    def enterLoadEstate(self):
        fields = {}
        for i, toon in enumerate(self.toonIds):
            fields['setSlot%dToonId' % i] = (toon,)

        self.mgr.air.sendActivate(self.estateId, self.mgr.air.districtId, self.zoneId, self.mgr.air.dclassesByName['DistributedEstateAI'], fields)
        self.acceptOnce('generate-%d' % self.estateId, self.__gotEstate)

    def __gotEstate(self, estate):
        self.estate = estate
        estate.pets = []
        self.estate.toons = self.toonIds
        self.estate.updateToons()
        self.demand('LoadHouses')

    def exitLoadEstate(self):
        self.ignore('generate-%d' % self.estateId)

    def enterLoadHouses(self):
        self.houseFSMs = []
        for houseIndex in range(6):
            fsm = LoadHouseFSM(self.mgr, self.estate, houseIndex, self.toons[houseIndex], self.__houseDone)
            self.houseFSMs.append(fsm)
            fsm.start()

    def __houseDone(self, house):
        if self.state != 'LoadHouses':
            house.requestDelete()
            return
        if all((houseFSM.done for houseFSM in self.houseFSMs)):
            self.demand('LoadPets')

    def enterLoadPets(self):
        self.petFSMs = []
        for houseIndex in range(6):
            toon = self.toons[houseIndex]
            if toon and toon['setPetId'][0] != 0:
                fsm = LoadPetFSM(self.mgr, self.estate, toon, self.__petDone)
                self.petFSMs.append(fsm)
                fsm.start()

        if not self.petFSMs:
            taskMgr.doMethodLater(0, lambda : self.demand('Finished'), 'nopets', extraArgs=[])

    def __petDone(self, pet):
        if self.state != 'LoadPets':
            pet.requestDelete()
            return
        if all((petFSM.done for petFSM in self.petFSMs)):
            self.demand('Finished')

    def enterFinished(self):
        self.callback(True)

    def enterFailure(self):
        self.cancel()
        self.callback(False)

    def cancel(self):
        if self.estate:
            self.estate.destroy()
            self.estate = None
        self.demand('Off')


class EstateManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('EstateManagerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.estate2toons = {}
        self.toon2estate = {}
        self.estate2timeout = {}
        self.zoneId2owner = {}

    def getEstateZone(self, avId):
        senderId = self.air.getAvatarIdFromSender()
        accId = self.air.getAccountIdFromSender()
        toon = self.air.doId2do.get(senderId)
        if not toon:
            self.air.writeServerEvent('suspicious', avId=senderId, issue='Sent getEstateZone() but not on district!')
            return
        if avId and avId != senderId:
            av = self.air.doId2do.get(avId)
            if av and av.dclass == self.air.dclassesByName['DistributedToonAI']:
                estate = self._lookupEstate(av)
                if estate:
                    avId = estate.owner.doId
                    zoneId = estate.zoneId
                    self._mapToEstate(toon, estate)
                    self._unloadEstate(toon)
                    self.sendUpdateToAvatarId(senderId, 'setEstateZone', [avId, zoneId])
            self.sendUpdateToAvatarId(senderId, 'setEstateZone', [0, 0])
            return
        estate = getattr(toon, 'estate', None)
        if estate:
            self._mapToEstate(toon, toon.estate)
            self.sendUpdateToAvatarId(senderId, 'setEstateZone', [senderId, estate.zoneId])
            if estate in self.estate2timeout:
                self.estate2timeout[estate].remove()
                del self.estate2timeout[estate]
            return
        if getattr(toon, 'loadEstateFSM', None):
            return
        zoneId = self.air.allocateZone(owner=self)

        def estateLoaded(success):
            if success:
                toon.estate = toon.loadEstateFSM.estate
                toon.estate.owner = toon
                self._mapToEstate(toon, toon.estate)
                self.sendUpdateToAvatarId(senderId, 'setEstateZone', [senderId, zoneId])
            else:
                self.sendUpdateToAvatarId(senderId, 'setEstateZone', [0, 0])
                self.air.deallocateZone(zoneId)
                del self.zoneId2owner[zoneId]
            toon.loadEstateFSM = None

        self.acceptOnce(self.air.getAvatarExitEvent(toon.doId), self._unloadEstate, extraArgs=[toon])
        self.zoneId2owner[zoneId] = avId
        toon.loadEstateFSM = LoadEstateFSM(self, estateLoaded)
        toon.loadEstateFSM.start(accId, zoneId)

    def exitEstate(self):
        senderId = self.air.getAvatarIdFromSender()
        toon = self.air.doId2do.get(senderId)
        if not toon:
            self.air.writeServerEvent('suspicious', avId=senderId, issue='Sent exitEstate() but not on district!')
            return
        self._unmapFromEstate(toon)
        self._unloadEstate(toon)

    def _unloadEstate(self, toon):
        if getattr(toon, 'estate', None):
            estate = toon.estate
            if estate not in self.estate2timeout:
                self.estate2timeout[estate] = taskMgr.doMethodLater(HouseGlobals.BOOT_GRACE_PERIOD, self._cleanupEstate, estate.uniqueName('emai-cleanup-task'), extraArgs=[estate])
            self._sendToonsToPlayground(toon.estate, 0)
        if getattr(toon, 'loadEstateFSM', None):
            self.air.deallocateZone(toon.loadEstateFSM.zoneId)
            toon.loadEstateFSM.cancel()
            toon.loadEstateFSM = None
        self.ignore(self.air.getAvatarExitEvent(toon.doId))

    def _cleanupEstate(self, estate):
        self._sendToonsToPlayground(estate, 1)
        for toon in self.estate2toons.get(estate, []):
            try:
                del self.toon2estate[toon]
            except KeyError:
                pass

        try:
            del self.estate2toons[estate]
        except KeyError:
            pass

        if estate in self.estate2timeout:
            del self.estate2timeout[estate]
        estate.destroy()
        estate.owner.estate = None
        for pet in estate.pets:
            pet.requestDelete()

        estate.pets = []
        self.air.deallocateZone(estate.zoneId)
        del self.zoneId2owner[estate.zoneId]

    def _sendToonsToPlayground(self, estate, reason):
        for toon in self.estate2toons.get(estate, []):
            self.sendUpdateToAvatarId(toon.doId, 'sendAvToPlayground', [toon.doId, reason])

    def _mapToEstate(self, toon, estate):
        self._unmapFromEstate(toon)
        self.estate2toons.setdefault(estate, []).append(toon)
        self.toon2estate[toon] = estate

    def _unmapFromEstate(self, toon):
        estate = self.toon2estate.get(toon)
        if not estate:
            return
        del self.toon2estate[toon]
        try:
            self.estate2toons[estate].remove(toon)
        except (KeyError, ValueError):
            pass

    def _lookupEstate(self, toon):
        return self.toon2estate.get(toon)

    def getOwnerFromZone(self, zoneId):
        return self.zoneId2owner.get(zoneId, 0)

    def getEstateZones(self, ownerId):
        estate = self._lookupEstate(self.air.doId2do.get(ownerId))
        if estate:
            return [estate.zoneId]
        return []
