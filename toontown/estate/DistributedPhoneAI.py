from direct.directnotify import DirectNotifyGlobal
from direct.distributed.ClockDelta import *
from toontown.estate.DistributedFurnitureItemAI import DistributedFurnitureItemAI
from PhoneGlobals import *

from toontown.toonbase import ToontownGlobals
from toontown.catalog import CatalogItem, CatalogInvalidItem, GiftAvatar
from toontown.catalog.CatalogItemList import CatalogItemList

import json

class LoadGiftAvatar:

    def __init__(self, phone, avId, targetId, optional, callback):
        self.air = phone.air
        self.phone = phone
        self.avId = avId
        self.targetId = targetId
        self.optional = optional
        self.callback = callback

    def start(self):
        self.air.dbInterface.queryObject(self.air.dbId, self.targetId, self.__gotAvatar)
    
    def copyDict(self, dict, *keys):
        return {key: dict[key] for key in keys}
    
    def __gotAvatar(self, dclass, fields):
        if dclass != self.air.dclassesByName['DistributedToonAI']:
            return
        
        for key in ('setDNAString', 'setMailboxContents', 'setGiftSchedule', 'setDeliverySchedule'):
            fields[key] = fields[key][0].encode('base64')
        
        newDict = self.copyDict(fields, 'setDNAString', 'setMailboxContents', 'setGiftSchedule', 'setDeliverySchedule', 'setHat', 'setGlasses', 'setBackpack',
                                'setShoes', 'setHatList', 'setGlassesList', 'setBackpackList', 'setShoes', 'setShoesList', 'setCustomMessages', 'setEmoteAccess',
                                'setClothesTopsList', 'setClothesBottomsList', 'setPetTrickPhrases', 'setNametagStyles')
        
        self.callback(self.avId, self.targetId, newDict, self.optional)
        del self.phone.fsms[self.avId]

class DistributedPhoneAI(DistributedFurnitureItemAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedPhoneAI")
    
    def __init__(self, air, furnitureMgr, catalogItem):
        DistributedFurnitureItemAI.__init__(self, air, furnitureMgr, catalogItem)
        self.fsms = {}
        self.initialScale = (0.8, 0.8, 0.8)
        self.inUse = False
        self.currAvId = 0
    
    def calcHouseItems(self, avatar):
        houseId = avatar.houseId
        
        if not houseId:
            self.notify.warning('Avatar %s has no houseId associated.' % avatar.doId)
            return 0
            
        house = simbase.air.doId2do.get(houseId)
        if not house:
            self.notify.warning('House %s (for avatar %s) not instantiated.' % (houseId, avatar.doId))
            return 0
            
        mgr = house.interior.furnitureManager
        attic = (mgr.atticItems, mgr.atticWallpaper, mgr.atticWindows)
        numHouseItems = len(CatalogItemList(house.getInteriorItems(), store=CatalogItem.Customization | CatalogItem.Location))
        numAtticItems = sum(len(x) for x in attic)
        
        return numHouseItems + numAtticItems
        
    def setInitialScale(self, scale):
        self.initialScale = scale
    
    def getInitialScale(self):
        return self.initialScale

    def avatarEnter(self):
        avId = self.air.getAvatarIdFromSender()
        if self.inUse:
            self.ejectAvatar(avId)
            return
            
        av = self.air.doId2do.get(avId)
        if av:
            self.setInUse(avId)
            self.sendUpdateToAvatarId(avId, 'setLimits', [self.calcHouseItems(av)])
            self.d_setMovie(PHONE_MOVIE_PICKUP, avId)
            av.b_setCatalogNotify(0, av.mailboxNotify)
            
            self.air.questManager.toonCalledClarabelle(av)
            
    def avatarExit(self):
        if not self.inUse:
            self.notify.warning('Requested avatarExit but phone isn\'t in use!')
            return
        avId = self.air.getAvatarIdFromSender()
        if avId != self.currAvId:
            self.notify.warning('Requested avatarExit from unknown avatar %s' %avId)
            return
        self.d_setMovie(PHONE_MOVIE_HANGUP, avId)
        taskMgr.doMethodLater(1, self.resetMovie, self.taskName('resetMovie'))
        self.setFree()
        
    def setFree(self):
        self.inUse = False
        self.currAvId = 0
        
    def setInUse(self, avId):
        self.inUse = True
        self.currAvId = avId
        
    def d_setMovie(self, movie, avId):
        self.sendUpdate('setMovie', args=[movie, avId, globalClockDelta.getRealNetworkTime(bits=32)])
        
    def ejectAvatar(self, avId):
        self.sendUpdateToAvatarId(avId, 'freeAvatar', [])
        
    def __getCaller(self):
        avId = self.air.getAvatarIdFromSender()
        if avId != self.currAvId:
            self.air.writeServerEvent('suspicious', avId, 'tried purchasing item, but not using phone')
            self.notify.warning('%d tried purchasing item, but not using phone' % avId)
            return
            
        av = self.air.doId2do.get(avId)
        if not av:
            self.air.writeServerEvent('suspicious', avId, 'tried purchasing item, but not on shard')
            self.notify.warning('%d tried purchasing item, but not on shard' % avId)
            return
            
        return av
    
    def checkPurchaseLimit(self, recipient, item):
        if len(recipient.mailboxContents) + len(recipient.onOrder) + len(recipient.onGiftOrder) + 1 >= ToontownGlobals.MaxMailboxContents:
            return ToontownGlobals.P_MailboxFull
        elif item.reachedPurchaseLimit(recipient):
            return ToontownGlobals.P_ReachedPurchaseLimit

        return ToontownGlobals.P_ItemOnOrder
    
    def chargeAvatar(self, av, money, emblems):
        av.takeMoney(money)
        av.subtractEmblems(emblems)
    
    def attemptPurchase(self, context, av, blob, optional, gifting=False):
        avId = av.doId
        item = CatalogItem.getItem(blob, CatalogItem.Customization)
        
        if isinstance(item, CatalogInvalidItem.CatalogInvalidItem):
            self.air.writeServerEvent('suspicious', avId, 'tried purchasing invalid item')
            self.notify.warning('%d tried purchasing invalid item' % avId)
            return ToontownGlobals.P_NotInCatalog
        elif (not item.hasEmblemPrices()) and item not in av.backCatalog and item not in av.weeklyCatalog and item not in av.monthlyCatalog:
            self.air.writeServerEvent('suspicious', avId, 'tried purchasing non-existing item')
            self.notify.warning('%d tried purchasing non-existing item' % avId)
            return ToontownGlobals.P_NotInCatalog
        
        if gifting and not item.isGift():
            return ToontownGlobals.P_NotAGift

        price = item.getPrice(CatalogItem.CatalogTypeBackorder if item in av.backCatalog else 0)
        
        if price > av.getTotalMoney() or (item.hasEmblemPrices() and not av.isEnoughEmblemsToBuy(item.getEmblemPrices())):
            return ToontownGlobals.P_NotEnoughMoney
        
        if gifting:
            return self.requestGiftAvatarOperation(avId, gifting, [context, item, price], self.attemptGiftPurchase)
        else:
            returnCode = self.checkPurchaseLimit(av, item)
            
            if returnCode != ToontownGlobals.P_ItemOnOrder:
                return returnCode

            if item.getDeliveryTime():
                self.chargeAvatar(av, price, item.getEmblemPrices())
                av.addToDeliverySchedule(item, item.getDeliveryTime())
                # av.addStat(ToontownGlobals.STAT_ITEMS)
            else:
                returnCode = item.recordPurchase(av, optional)
                
                if returnCode == ToontownGlobals.P_ItemAvailable:
                    self.chargeAvatar(av, price, item.getEmblemPrices())
                    # av.addStat(ToontownGlobals.STAT_ITEMS)

            return returnCode

        return None
    
    def attemptGiftPurchase(self, avId, targetId, avatar, optional):
        av = self.air.doId2do.get(avId)
        
        if not av:
            return

        recipient = GiftAvatar.createFromFields(avatar)
        context = optional[0]
        item = optional[1]
        returnCode = self.checkPurchaseLimit(recipient, item)
            
        if returnCode != ToontownGlobals.P_ItemOnOrder:
            self.sendGiftPurchaseResponse(context, avId, returnCode)
            return

        self.chargeAvatar(av, optional[2], item.getEmblemPrices())
        recipient.addToGiftSchedule(avId, targetId, item, item.getDeliveryTime())
        # av.addStat(ToontownGlobals.STAT_ITEMS)

        self.sendGiftPurchaseResponse(context, avId, ToontownGlobals.P_ItemOnOrder)
    
    def sendGiftPurchaseResponse(self, context, avId, returnCode):
        # if returnCode in (ToontownGlobals.P_ItemOnOrder, ToontownGlobals.P_ItemAvailable):
        #     messenger.send('topToonsManager-event', [avId, TopToonsGlobals.CAT_CATALOG | TopToonsGlobals.CAT_GIFTS, 1])

        self.sendUpdateToAvatarId(avId, 'requestGiftPurchaseResponse', [context, returnCode])

    def requestPurchaseMessage(self, context, blob, optional):
        av = self.__getCaller()

        if not av:
            return

        returnCode = self.attemptPurchase(context, av, blob, optional)
        
        # if returnCode in (ToontownGlobals.P_ItemOnOrder, ToontownGlobals.P_ItemAvailable):
        #     messenger.send('topToonsManager-event', [av.doId, TopToonsGlobals.CAT_CATALOG, 1])
        
        self.sendUpdateToAvatarId(av.doId, 'requestPurchaseResponse', [context, returnCode])
        
    def requestGiftPurchaseMessage(self, context, targetId, blob, optional):
        av = self.__getCaller()
        
        if not av:
            return
        
        returnCode = self.attemptPurchase(context, av, blob, optional, gifting=targetId)
        
        if returnCode:
            self.sendGiftPurchaseResponse(context, av.doId, returnCode)
    
    def requestGiftAvatar(self, doId):
        self.requestGiftAvatarOperation(self.air.getAvatarIdFromSender(), doId, None, self.sendGiftAvatarResponse)
    
    def requestGiftAvatarOperation(self, avId, doId, optional, callback):
        if avId in self.fsms:
            return ToontownGlobals.P_TooFast
        
        loadOperation = LoadGiftAvatar(self, avId, doId, optional, callback)
        loadOperation.start()
        self.fsms[avId] = loadOperation
        return None
    
    def sendGiftAvatarResponse(self, avId, targetId, avatar, optional):
        self.sendUpdateToAvatarId(avId, 'setGiftAvatar', [json.dumps(avatar)])

    def resetMovie(self, task):
        self.d_setMovie(PHONE_MOVIE_CLEAR, 0)
        return task.done