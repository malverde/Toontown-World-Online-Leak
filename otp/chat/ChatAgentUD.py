from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from toontown.chat.TTWhiteList import TTWhiteList
from otp.distributed import OtpDoGlobals

class ChatAgentUD(DistributedObjectGlobalUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('ChatAgentUD')

    def announceGenerate(self):
        DistributedObjectGlobalUD.announceGenerate(self)
        self.wantWhitelist = config.GetBool('want-whitelist', True)
        if self.wantWhitelist:
            self.whiteList = TTWhiteList()
        self.chatMode2channel = {1: OtpDoGlobals.OTP_MOD_CHANNEL,
         2: OtpDoGlobals.OTP_ADMIN_CHANNEL,
         3: OtpDoGlobals.OTP_SYSADMIN_CHANNEL}
        self.chatMode2prefix = {1: '[MOD] ',
         2: '[ADMIN] ',
         3: '[SYSADMIN] '}

    def chatMessage(self, message, chatMode):
        sender = self.air.getAvatarIdFromSender()
        if sender == 0:
            self.air.writeServerEvent('suspicious', self.air.getAccountIdFromSender(), issue='Account sent chat without an avatar', message=message)
            return
        cleanMessage, modifications = message, []
        self.air.writeServerEvent('chat-said', avId=sender, chatMode=chatMode, msg=message, cleanMsg=cleanMessage)
        if chatMode != 0:
            if message.startswith('.'):
                cleanMessage = '.' + self.chatMode2prefix.get(chatMode, '') + message[1:]
            else:
                cleanMessage = self.chatMode2prefix.get(chatMode, '') + message
            modifications = []
        DistributedAvatar = self.air.dclassesByName['DistributedAvatarUD']
        dg = DistributedAvatar.aiFormatUpdate('setTalk', sender, self.chatMode2channel.get(chatMode, sender), self.air.ourChannel, [0,
         0,
         '',
         cleanMessage,
         modifications,
         0])
        self.air.send(dg)
