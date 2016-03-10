#Embedded file name: toontown.coderedemption.TTCodeRedemptionMgrAI
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from toontown.toonbase import ToontownGlobals
from toontown.catalog import CatalogItem
from toontown.catalog.CatalogItemList import CatalogItemList
from toontown.catalog.CatalogPoleItem import CatalogPoleItem
from toontown.catalog.CatalogBeanItem import CatalogBeanItem
from toontown.catalog.CatalogChatItem import CatalogChatItem
from toontown.catalog.CatalogClothingItem import CatalogClothingItem, getAllClothes
from toontown.catalog.CatalogAccessoryItem import CatalogAccessoryItem
from toontown.catalog.CatalogRentalItem import CatalogRentalItem
from toontown.catalog.CatalogFurnitureItem import CatalogFurnitureItem
from toontown.catalog.CatalogInvalidItem import CatalogInvalidItem
from toontown.catalog import CatalogGardenItem
from toontown.catalog import CatalogGardenStarterItem
from toontown.catalog.CatalogGardenStarterItem import CatalogGardenStarterItem
import time

class TTCodeRedemptionMgrAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('TTCodeRedemptionMgrAI')
    Success = 0
    InvalidCode = 1
    ExpiredCode = 2
    Ineligible = 3
    AwardError = 4
    TooManyFails = 5
    ServiceUnavailable = 6

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.air = air

    def announceGenerate(self):
        DistributedObjectAI.announceGenerate(self)

    def delete(self):
        DistributedObjectAI.delete(self)

    def giveAwardToToonResult(self, todo0, todo1):
        pass

    def redeemCode(self, context, code):
        avId = self.air.getAvatarIdFromSender()
        if not avId:
            self.air.writeServerEvent('suspicious', avId=avId, issue='Tried to redeem a code from an invalid avId')
            return
        av = self.air.doId2do.get(avId)
        if not av:
            self.air.writeServerEvent('suspicious', avId=avId, issue='Invalid avatar tried to redeem a code')
            return
        valid = True
        eligible = True
        expired = False
        delivered = False
        codes = av.getRedeemedCodes()
        print codes
        if not codes:
            codes = [code]
            av.setRedeemedCodes(codes)
        elif code not in codes:
            codes.append(code)
            av.setRedeemedCodes(codes)
            valid = True
        else:
            valid = False
        if not valid:
            self.air.writeServerEvent('code-redeemed', avId=avId, issue='Invalid code: %s' % code)
            self.sendUpdateToAvatarId(avId, 'redeemCodeResult', [context, self.InvalidCode, 0])
            return
        if expired:
            self.air.writeServerEvent('code-redeemed', avId=avId, issue='Expired code: %s' % code)
            self.sendUpdateToAvatarId(avId, 'redeemCodeResult', [context, self.ExpiredCode, 0])
            return
        if not eligible:
            self.air.writeServerEvent('code-redeemed', avId=avId, issue='Ineligible for code: %s' % code)
            self.sendUpdateToAvatarId(avId, 'redeemCodeResult', [context, self.Ineligible, 0])
            return
        items = self.getItemsForCode(code)
        for item in items:
            if isinstance(item, CatalogInvalidItem):
                self.air.writeServerEvent('suspicious', avId=avId, issue="Invalid CatalogItem's for code: %s" % code)
                self.sendUpdateToAvatarId(avId, 'redeemCodeResult', [context, self.InvalidCode, 0])
                break
            if len(av.mailboxContents) + len(av.onGiftOrder) >= ToontownGlobals.MaxMailboxContents:
                delivered = False
                break
            item.deliveryDate = int(time.time() / 60) + 1
            av.onOrder.append(item)
            av.b_setDeliverySchedule(av.onOrder)
            delivered = True

        if not delivered:
            self.air.writeServerEvent('code-redeemed', avId=avId, issue='Could not deliver items for code: %s' % code)
            self.sendUpdateToAvatarId(avId, 'redeemCodeResult', [context, self.InvalidCode, 0])
            return
        self.air.writeServerEvent('code-redeemed', avId=avId, issue='Successfuly redeemed code: %s' % code)
        self.sendUpdateToAvatarId(avId, 'redeemCodeResult', [context, self.Success, 0])

    def getItemsForCode(self, code):
        avId = self.air.getAvatarIdFromSender()
        if not avId:
            self.air.writeServerEvent('suspicious', avId=avId, issue='Could not parse the gender of an invalid avId')
            return
        av = self.air.doId2do.get(avId)
        if not av:
            self.air.writeServerEvent('suspicious', avId=avId, issue='Could not parse the gender of an invalid avatar')
            return
        code = code.lower()
        if code == 'bdisanerd':
            beans = CatalogBeanItem(420, tagCode=2)
            return [beans]
        if code == 'flip-for-flippy':
            shirt = CatalogClothingItem(2001, 0)
            return [shirt]
        if code == 'dont-be-wacky':
            shirt = CatalogClothingItem(2002, 0)
            return [shirt]
        if code == 'gadzooks':
            shirt = CatalogClothingItem(1807, 0)
            return [shirt]
        if code == 'sillymeter' or code == 'silly meter' or code == 'silly-meter':
            shirt = CatalogClothingItem(1753, 0)
            return [shirt]
        if code == 'gc-sbfo' or code == 'gc sbfo' or code == 'gcsbfo':
            shirt = CatalogClothingItem(1788, 0)
            return [shirt]
        if code == 'getconnected' or code == 'get connected' or code == 'get_connected':
            shirt = CatalogClothingItem(1752, 0)
            return [shirt]
        if code == 'summer':
            shirt = CatalogClothingItem(1709, 0)
            return [shirt]
        if code == 'brrrgh':
            shirt = CatalogClothingItem(1800, 0)
            return [shirt]
        if code == 'toontastic':
            shirt = CatalogClothingItem(1820, 0)
            return [shirt]
        if code == 'sunburst':
            shirt = CatalogClothingItem(1809, 0)
            return [shirt]
        if code == 'sweet' or code == 'schweet':
            beans = CatalogBeanItem(12000, tagCode=2)
            return [beans]
        if code == 'winter' or code == 'cannons':
            rent = CatalogRentalItem(ToontownGlobals.RentalCannon, 2880, 0)
            return [rent]
        if code == 'paycheck':
            beans = CatalogBeanItem(1500, tagCode=2)
            return [beans]
        # Heh, why not?
        if code == 'double-paycheck':
            beans = CatalogBeanItem(1500, tagCode=2)
            return [beans]    
        # Pre-Alpha shirt?
        if code == 'PreAlpha':
            shirt = CatalogClothingItem(1763, 0)
            return [shirt]
        # StormSellbot Shirt?
        if code == 'stormsellbot':
            shirt = CatalogClothingItem(111, 0)
            return [shirt]
        # Trunk, shouldn't REALLY be enabled... but... we'll add it back for later
        if code == 'trunk':
            object = CatalogFurnitureItem(4000, 0)
            return [object]
            # Uh? Mgracer?
        # Sue me - Sir Kippy
        if code == 'alpha':
            shirt = CatalogClothingItem(1403, 0)
            shorts = CatalogClothingItem(1404, 0)
            return [shirt, shorts] # TODO: Give the correct alpha reward
        if code == 'garden':  # TODO: Get Catalog to make this item purchasable
            items = CatalogGardenStarterItem()
            return [items]
        # Sue me - Sir Kippy
        if code == 'beta':
            return CatalogClothingItem(118, 0) # TODO: Give it the correct item
            shirt = CatalogClothingItem(1405, 0)
            shorts = CatalogClothingItem(1406, 0)
            return [shirt, shorts] # TODO: Give the correct beta rewards
        # Uh? Might as well keep it. Disney Legacy Games... hehe...
        if code == 'toonfest2014':
            shirt = CatalogClothingItem(2003, 0)
            if av.getStyle().getGender() == 'm':
                bot = CatalogClothingItem(2004, 0)
            else:
                bot = CatalogClothingItem(2005, 0)
            return [shirt, bot]
        return [CatalogInvalidItem()]

    def requestCodeRedeem(self, todo0, todo1):
        pass

    def redeemCodeResult(self, todo0, todo1, todo2):
        pass