from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
# TODO: OTP should not depend on Toontown... Hrrm.
from toontown.chat.TTWhiteList import TTWhiteList
import time

class ChatAgentUD(DistributedObjectGlobalUD):
    notify = DirectNotifyGlobal.directNotify.newCategory("ChatAgentUD")

    def announceGenerate(self):
        DistributedObjectGlobalUD.announceGenerate(self)

        self.whiteList = TTWhiteList()
        self.muted = {}

    def muteAccount(self, account, howLong):
        print ['muteAccount', account, howLong]
        self.muted[account] = int(time.time()/60) + howLong

    def unmuteAccount(self, account):
        print ['unuteAccount', account]
        if account in self.muted:
            del self.muted[account]

    def chatMessage(self, message):
        sender = self.air.getAvatarIdFromSender()
        if sender == 0:
            self.air.writeServerEvent('suspicious', self.air.getAccountIdFromSender(),
                                         'Account sent chat without an avatar', message)
            return

        if sender in self.muted and int(time.time()/60) < self.muted[sender]:
            return

        modifications = []
        words = message.split(' ')
        offset = 0
        WantWhitelist = config.GetBool('want-whitelist', 1)
        for word in words:
            if word and not self.whiteList.isWord(word) and WantWhitelist:
                modifications.append((offset, offset+len(word)-1))
            offset += len(word) + 1

        cleanMessage = message
        for modStart, modStop in modifications:
            cleanMessage = cleanMessage[:modStart] + '*'*(modStop-modStart+1) + cleanMessage[modStop+1:]

        self.air.writeServerEvent('chat-said', sender, message, cleanMessage)

        # TODO: The above is probably a little too ugly for my taste... Maybe AIR
        # should be given an API for sending updates for unknown objects?
        DistributedAvatar = self.air.dclassesByName['DistributedAvatarUD']
        dg = DistributedAvatar.aiFormatUpdate('setTalk', sender, sender,
                                              self.air.ourChannel,
                                              [0, 0, '', cleanMessage, modifications, 0])
        self.air.send(dg)

        self.air.csm.accountDB.persistChat(sender, message, self.air.ourChannel)
