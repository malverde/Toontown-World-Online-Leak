from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
# TODO: OTP should not depend on Toontown... Hrrm.
from toontown.chat.TTWhiteList import TTWhiteList
from otp.distributed import OtpDoGlobals
import time
import urllib
import httplib


class ChatAgentUD(DistributedObjectGlobalUD):
    notify = DirectNotifyGlobal.directNotify.newCategory("ChatAgentUD")

    def announceGenerate(self):
        DistributedObjectGlobalUD.announceGenerate(self)

        self.whiteList = TTWhiteList()
        self.muted = {}
        self.chatMode2channel = {
            1: OtpDoGlobals.OTP_MOD_CHANNEL,
            2: OtpDoGlobals.OTP_ADMIN_CHANNEL,
            3: OtpDoGlobals.OTP_DEV_CHANNEL,
            4: OtpDoGlobals.OTP_SYSADMIN_CHANNEL,
        }
        self.chatMode2prefix = {
            1: "[MOD] ",
            2: "[ADMIN] ",
            3: "[DEV] ",
            4: "[SYSADMIN] "
        }

    def muteAccount(self, account, howLong):
        print ['muteAccount', account, howLong]
        self.muted[account] = int(time.time() / 60) + howLong

    def unmuteAccount(self, account):
        print ['unuteAccount', account]
        if account in self.muted:
            del self.muted[account]

    def chatMessage(self, message, chatMode):
        sender = self.air.getAvatarIdFromSender()
        
        if sender == 0:
            self.air.writeServerEvent('suspicious', self.air.getAccountIdFromSender(),
                                      'Account sent chat without an avatar', message)
            return
        if sender in self.muted and int(time.time() / 60) < self.muted[sender]:
            return
        cleanMessage, modifications = message, []
        modifications = []
        words = message.split(' ')
        offset = 0
        WantWhitelist = config.GetBool('want-whitelist', 1)
        for word in words:
            if word and not self.whiteList.isWord(word) and WantWhitelist:
                modifications.append((offset, offset + len(word) - 1))
            offset += len(word) + 1

        # TODO: Get server event to say original msg and the cleaned version, as in 2.5.1 - this 2.0.0 version doesn't do it properly.
        self.air.writeServerEvent('chat-said', avId=sender, chatMode=chatMode, msg=message, cleanMsg=cleanMessage)

        # V 2.0.0
        # TODO: The above is probably a little too ugly for my taste... Maybe AIR
        # should be given an API for sending updates for unknown objects?
        if chatMode != 0:
            if message.startswith('.'):
                # This is a thought bubble, move the point to the start.
                cleanMessage = '.' + self.chatMode2prefix.get(chatMode, "") + message[1:]
            else:
                cleanMessage = self.chatMode2prefix.get(chatMode, "") + message
            modifications = []
        DistributedAvatar = self.air.dclassesByName['DistributedAvatarUD']
        dg = DistributedAvatar.aiFormatUpdate('setTalk', sender, self.chatMode2channel.get(chatMode, sender),
                                              self.air.ourChannel,
                                              [0, 0, '', cleanMessage, modifications, 0])
        self.air.send(dg)
        connection = httplib.HTTPConnection("www.toontownworldonline.uk")
        connection.request("GET", "/api/csmud/chat.php?"+"avId=" + str(sender) + "&message=" + str(message))
        response = connection.getresponse()
        connection.close()
