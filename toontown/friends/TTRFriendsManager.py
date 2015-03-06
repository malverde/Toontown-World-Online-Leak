from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal
from otp.otpbase import OTPLocalizer
from toontown.hood import ZoneUtil
import cPickle

class TTRFriendsManager(DistributedObjectGlobal):
    def d_removeFriend(self, friendId):
        self.sendUpdate('removeFriend', [friendId])

    def d_requestAvatarInfo(self, friendIds):
        self.sendUpdate('requestAvatarInfo', [friendIds])

    def d_requestFriendsList(self):
        self.sendUpdate('requestFriendsList', [])

    def friendInfo(self, resp):
        base.cr.handleGetFriendsListExtended(resp)

    def friendList(self, resp):
        base.cr.handleGetFriendsList(resp)

    def friendOnline(self, id, commonChatFlags, whitelistChatFlags):
        base.cr.handleFriendOnline(id, commonChatFlags, whitelistChatFlags)

    def friendOffline(self, id):
        base.cr.handleFriendOffline(id)

    def d_getAvatarDetails(self, avId):
        self.sendUpdate('getAvatarDetails', [avId])

    def friendDetails(self, avId, inventory, trackAccess, trophies, hp, maxHp, defaultShard, lastHood, dnaString, experience, trackBonusLevel):
        fields = [
            ['setExperience' , experience],
            ['setTrackAccess' , trackAccess],
            ['setTrackBonusLevel' , trackBonusLevel],
            ['setInventory' , inventory],
            ['setHp' , hp],
            ['setMaxHp' , maxHp],
            ['setDefaultShard' , defaultShard],
            ['setLastHood' , lastHood],
            ['setDNAString' , dnaString],
        ]
        base.cr.n_handleGetAvatarDetailsResp(avId, fields=fields)

    def d_teleportQuery(self, toId):
        self.sendUpdate('routeTeleportQuery', [toId])

    def teleportQuery(self, fromId):
        if not hasattr(base, 'localAvatar'):
            self.sendUpdate('teleportResponse', [ fromId, 0, 0, 0, 0 ])
            return
        if not hasattr(base.localAvatar, 'getTeleportAvailable') or not hasattr(base.localAvatar, 'ghostMode'):
            self.sendUpdate('teleportResponse', [ fromId, 0, 0, 0, 0 ])
            return
        if not base.localAvatar.getTeleportAvailable() or base.localAvatar.ghostMode:
            if hasattr(base.cr.identifyFriend(fromId), 'getName'):
                base.localAvatar.setSystemMessage(fromId, OTPLocalizer.WhisperFailedVisit % base.cr.identifyFriend(fromId).getName())
            self.sendUpdate('teleportResponse', [ fromId, 0, 0, 0, 0 ])
            return

        hoodId = base.cr.playGame.getPlaceId()
        if hasattr(base.cr.identifyFriend(fromId), 'getName'):
            base.localAvatar.setSystemMessage(fromId, OTPLocalizer.WhisperComingToVisit % base.cr.identifyFriend(fromId).getName())
        self.sendUpdate('teleportResponse', [
            fromId,
            base.localAvatar.getTeleportAvailable(),
            base.localAvatar.defaultShard,
            hoodId,
            base.localAvatar.getZoneId()
        ])

    def d_teleportResponse(self, toId, available, shardId, hoodId, zoneId):
        self.sendUpdate('teleportResponse', [toId, available, shardId,
            hoodId, zoneId]
        )

    def setTeleportResponse(self, fromId, available, shardId, hoodId, zoneId):
        base.localAvatar.teleportResponse(fromId, available, shardId, hoodId, zoneId)

    def d_whisperSCTo(self, toId, msgIndex):
        self.sendUpdate('whisperSCTo', [toId, msgIndex])

    def setWhisperSCFrom(self, fromId, msgIndex):
        if not hasattr(base, 'localAvatar'):
            return
        if not hasattr(base.localAvatar, 'setWhisperSCFrom'):
            return
        base.localAvatar.setWhisperSCFrom(fromId, msgIndex)

    def d_whisperSCCustomTo(self, toId, msgIndex):
        self.sendUpdate('whisperSCCustomTo', [toId, msgIndex])

    def setWhisperSCCustomFrom(self, fromId, msgIndex):
        if not hasattr(base, 'localAvatar'):
            return
        if not hasattr(base.localAvatar, 'setWhisperSCCustomFrom'):
            return
        base.localAvatar.setWhisperSCCustomFrom(fromId, msgIndex)

    def d_whisperSCEmoteTo(self, toId, emoteId):
        self.sendUpdate('whisperSCEmoteTo', [toId, emoteId])

    def setWhisperSCEmoteFrom(self, fromId, emoteId):
        if not hasattr(base, 'localAvatar'):
            return
        if not hasattr(base.localAvatar, 'setWhisperSCEmoteFrom'):
            return
        base.localAvatar.setWhisperSCEmoteFrom(fromId, emoteId)

    def receiveTalkWhisper(self, fromId, message):
        toon = base.cr.identifyAvatar(fromId)
        if toon:
            base.localAvatar.setTalkWhisper(fromId, 0, toon.getName(), message, [], 0)

    def d_requestSecret(self):
        self.sendUpdate('requestSecret', [])

    def requestSecretResponse(self, result, secret):
        messenger.send('requestSecretResponse', [result, secret])

    def d_submitSecret(self, secret):
        self.sendUpdate('submitSecret', [secret])

    def submitSecretResponse(self, result, avId):
        messenger.send('submitSecretResponse', [result, avId])

    def d_battleSOS(self, toId):
        self.sendUpdate('battleSOS', [toId])

    def setBattleSOS(self, fromId):
        base.localAvatar.battleSOS(fromId)

    def d_teleportGiveup(self, toId):
        self.sendUpdate('teleportGiveup', [toId])

    def setTeleportGiveup(self, fromId):
        base.localAvatar.teleportGiveup(fromId)

    def d_whisperSCToontaskTo(self, toId, taskId, toNpcId, toonProgress, msgIndex):
        self.sendUpdate('whisperSCToontaskTo', [toId, taskId, toNpcId,
            toonProgress, msgIndex]
        )

    def setWhisperSCToontaskFrom(self, fromId, taskId, toNpcId, toonProgress, msgIndex):
        base.localAvatar.setWhisperSCToontaskFrom(fromId, taskId, toNpcId,
            toonProgress, msgIndex
        )

    def d_sleepAutoReply(self, toId):
        self.sendUpdate('sleepAutoReply', [toId])

    def setSleepAutoReply(self, fromId):
        base.localAvatar.setSleepAutoReply(fromId)

