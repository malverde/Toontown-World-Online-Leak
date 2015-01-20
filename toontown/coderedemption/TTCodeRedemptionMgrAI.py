from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from toontown.toonbase import ToontownGlobals


# Import the Catalog
from toontown.catalog import CatalogItem
from toontown.catalog.CatalogInvalidItem import CatalogInvalidItem
from toontown.catalog.CatalogItemList import CatalogItemList
from toontown.catalog.CatalogClothingItem import CatalogClothingItem, getAllClothes

import time

class TTCodeRedemptionMgrAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("TTCodeRedemptionMgrAI")

    # TODO: Possibly place these in a better location
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

        ### VALIDATEE THIS SHIT ###
        valid = True            ###
        eligible = True         ###
        expired = False         ###
        delivered = False       ###
        ###########################

       # TODO: Come up with a way to determine if the toon is eligible for the prize


        # Get our redeemed Codes
        codes = av.getRedeemedCodes()
        print codes
        if not codes:
            codes = [code]
            av.setRedeemedCodes(codes)
        else:
            if not code in codes:
                codes.append(code)
                av.setRedeemedCodes(codes)
                valid = True
            else:
                valid = False

        # Is the code valid?
        if not valid:
            self.air.writeServerEvent('code-redeemed', avId=avId, issue='Invalid code: %s' % code)
            self.sendUpdateToAvatarId(avId, 'redeemCodeResult', [context, self.InvalidCode, 0])
            return

        # Did out code expire?
        if expired:
            self.air.writeServerEvent('code-redeemed', avId=avId, issue='Expired code: %s' % code)
            self.sendUpdateToAvatarId(avId, 'redeemCodeResult', [context, self.ExpiredCode, 0])
            return

        # Are we able to redeem this code?
        if not eligible:
            self.air.writeServerEvent('code-redeemed', avId=avId, issue='Ineligible for code: %s' % code)
            self.sendUpdateToAvatarId(avId, 'redeemCodeResult', [context, self.Ineligible, 0])
            return

        # Deliver the reward to the user
        items = self.getItemsForCode(code)

        # Iterate over these shitty items
        for item in items:
            if isinstance(item, CatalogInvalidItem): # Umm, u wot m8?
                self.air.writeServerEvent('suspicious', avId=avId, issue='Invalid CatalogItem\'s for code: %s' % code)
                self.sendUpdateToAvatarId(avId, 'redeemCodeResult', [context, self.InvalidCode, 0]) # TODO: Come up with a special code for this
                break

            item.deliveryDate = int(time.time() / 60) + 1 # I don't give a shit here, just deliver it now
            av.onOrder.append(item)
            av.b_setDeliverySchedule(av.onOrder)
            delivered = True

        # Iterate over these shitty items
        for item in items:
            if isinstance(item, CatalogInvalidItem): # Umm, u wot m8?
                self.air.writeServerEvent('suspicious', avId=avId, issue='Invalid CatalogItem\'s for code: %s' % code)
                self.sendUpdateToAvatarId(avId, 'redeemCodeResult', [context, self.InvalidCode, 0]) # TODO: Come up with a special code for this
                break

            if len(av.mailboxContents) + len(av.onGiftOrder) >= ToontownGlobals.MaxMailboxContents:
                # Mailbox is full
                delivered = False
                break

            item.deliveryDate = int(time.time() / 60) + 1 # I don't give a shit here, just deliver it now
            av.onOrder.append(item)
            av.b_setDeliverySchedule(av.onOrder)
            delivered = True

        if not delivered:
            # 0 is Sucess
            # 1, 2, 15, & 16 is an UnknownError
            # 3 & 4 is MailboxFull
            # 5 & 10 is AlreadyInMailbox
            # 6, 7, & 11 is AlreadyInQueue
            # 8 is AlreadyInCloset
            # 9 is AlreadyBeingWorn
            # 12, 13, & 14 is AlreadyReceived
            self.air.writeServerEvent('code-redeemed', avId=avId, issue='Could not deliver items for code: %s' % code)
            self.sendUpdateToAvatarId(avId, 'redeemCodeResult', [context, self.AwardError, 3])
            return

        # Send the item and tell the user its A-Okay
        self.air.writeServerEvent('code-redeemed', avId=avId, issue='Successfuly redeemed code: %s' % code)
        self.sendUpdateToAvatarId(avId, 'redeemCodeResult', [context, self.Success, 0])

    def redeemCodeAiToUd(self, todo0, todo1, todo2, todo3, todo4):
        pass

    def redeemCodeResultUdToAi(self, todo0, todo1, todo2, todo3, todo4):
        pass

    def redeemCodeResult(self, todo0, todo1, todo2):
        pass

    ### Helper Methods ###

    def getItemsForCode(self, code):
        # TODO: Figure out how we want to get the items from the codes
        # I don't know what items are shorts, skirts or shirts... rip
        if code == "ALPHA":
            shirt = CatalogClothingItem(1403, 0)
            shorts = CatalogClothingItem(1404, 0)
            return [shirt, shorts] # TODO: Give the correct alpha reward

        if code == "BETA":
            return CatalogClothingItem(118, 0) # TODO: Give it the correct item
            shirt = CatalogClothingItem(1405, 0)
            shorts = CatalogClothingItem(1406, 0)
            return [shirt, shorts] # TODO: Give the correct beta rewards

        return [CatalogInvalidItem()]

