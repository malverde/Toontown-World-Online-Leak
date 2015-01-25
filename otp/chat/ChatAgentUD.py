from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
# TODO: OTP should not depend on Toontown... Hrrm.
from toontown.chat.TTWhiteList import TTWhiteList
from toontown.chat.TTSequenceList import TTSequenceList
from otp.distributed import OtpDoGlobals

class ChatAgentUD(DistributedObjectGlobalUD):
    notify = DirectNotifyGlobal.directNotify.newCategory("ChatAgentUD")

    def announceGenerate(self):
        DistributedObjectGlobalUD.announceGenerate(self)
        self.wantBlacklistSequence = config.GetBool('want-blacklist-sequence', True)
        self.wantWhitelist = config.GetBool('want-whitelist', True)
        if self.wantWhitelist:
            self.whiteList = TTWhiteList()
            if self.wantBlacklistSequence:
                self.sequenceList = TTSequenceList()
        self.chatMode2channel = {
            1 : OtpDoGlobals.OTP_MOD_CHANNEL,
            2 : OtpDoGlobals.OTP_ADMIN_CHANNEL,
            3 : OtpDoGlobals.OTP_SYSADMIN_CHANNEL,
        }
        self.chatMode2prefix = {
            1 : "[MOD] ",
            2 : "[ADMIN] ",
            3 : "[SYSADMIN] ",
        }
        
    def chatMessage(self, message, chatMode):
        sender = self.air.getAvatarIdFromSender()
        if sender == 0:
            self.air.writeServerEvent('suspicious', self.air.getAccountIdFromSender(),
                                         issue='Account sent chat without an avatar', message=message)
            return

        cleanMessage, modifications = message, []
        self.air.writeServerEvent('chat-said', avId=sender, chatMode=chatMode, msg=message, cleanMsg=cleanMessage)

        # TODO: The above is probably a little too ugly for my taste... Maybe AIR
        # should be given an API for sending updates for unknown objects?
        if chatMode != 0:
            # Staff messages do not need to be cleaned. [TODO: Blacklist this?]
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

