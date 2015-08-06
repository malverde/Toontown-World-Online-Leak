from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.distributed.PyDatagram import *
from direct.task import Task
from direct.directnotify.DirectNotifyGlobal import directNotify
import string
import random
import functools
import time
from direct.fsm.FSM import FSM

# -- FSMS --
class OperationFSM(FSM):

    def __init__(self, mgr, air, senderAvId, targetAvId=None, callback=None):
        FSM.__init__(self, 'OperationFSM-%s' % senderAvId)
        self.mgr = mgr
        self.air = air
        self.sender = senderAvId
        self.result = None
        self.target = targetAvId
        self.callback = callback

    def enterOff(self):
        if self.callback:
            if self.result is not None:
                self.callback(self.sender, self.result)
            else:
                self.callback()

        if self in self.mgr.operations:
            self.mgr.operations.remove(self)

    def enterError(self, message=None):
        self.mgr.notify.warning("An error has occurred in a '%s'. Message: %s" %
            (type(self).__name__, message) )
        if self.sender in self.mgr.operations:
            del self.mgr.operations[self.sender]


# -- Friends list --
class FriendsListOperation(OperationFSM):

    def enterStart(self):
        self.air.dbInterface.queryObject(self.air.dbId, self.sender,
            self.handleRetrieveSender)

    def handleRetrieveSender(self, dclass, fields):
        if dclass != self.air.dclassesByName['DistributedToonUD']:
            self.demand('Error', 'Distributed Class was not a Toon.')
            return

        self.demand('Retrieved', fields['setFriendsList'][0])

    def enterRetrieved(self, friendsList):
        self.friendsList = friendsList
        if len(self.friendsList) <= 0:
            self.result = []
            self.demand('Off')
            return

        self.friendIndex = 0
        self.realFriendsList = []

        self.air.dbInterface.queryObject(self.air.dbId, self.friendsList[0][0],
            self.addFriend)

        def addFriend(dclass, fields, friendId = 0, avId = 0):
            if not (avId or friendId):
                return
            if dclass == self.air.dclassesByName['DistributedToonUD']:
                self.listResponses[avId].append([friendId,
                 fields['setName'][0],
                 fields['setDNAString'][0],
                 fields['setPetId'][0]])
            if len(self.listResponses[avId]) >= len(self.friendsLists[avId]):
                self.sendUpdateToAvatarId(avId, 'friendList', [self.listResponses[avId]])
                del self.friendsLists[avId]
                del self.friendIndexes[avId]
                del self.listResponses[avId]
            else:
                self.friendIndexes[avId] += 1
                self.air.dbInterface.queryObject(self.air.dbId, self.friendsLists[avId][self.friendIndexes[avId]][0], functools.partial(addFriend, avId=avId, friendId=self.friendsLists[avId][self.friendIndexes[avId]][0]))
                


# -- Remove Friends --
class RemoveFriendOperation(OperationFSM):

    def __init__(self, mgr, air, senderAvId, targetAvId=None, callback=None, alert=False):
        OperationFSM.__init__(self, mgr, air, senderAvId, targetAvId, callback)
        self.alert = alert

    def enterStart(self):
        self.air.dbInterface.queryObject(self.air.dbId, self.sender,
            self.handleRetrieve)

    def handleRetrieve(self, dclass, fields):
        if dclass != self.air.dclassesByName['DistributedToonUD']:
            self.demand('Error', 'Distributed Class was not a Toon.')
            return

        self.demand('Retrieved', fields['setFriendsList'][0])

    def enterRetrieved(self, friendsList):
        newList = []
        for i in xrange(len(friendsList)):
            if friendsList[i][0] == self.target:
                continue
            newList.append(friendsList[i])
        if self.sender in self.mgr.onlineToons:
            dg = self.air.dclassesByName['DistributedToonUD'].aiFormatUpdate(
                    'setFriendsList', self.sender, self.sender,
                    self.air.ourChannel, [newList])
            self.air.send(dg)
            if self.alert:
                dg = self.air.dclassesByName['DistributedToonUD'].aiFormatUpdate(
                     'friendsNotify', self.sender, self.sender,
                     self.air.ourChannel, [self.target, 1])
                self.air.send(dg)
            self.demand('Off')
            return

        self.air.dbInterface.updateObject(self.air.dbId, self.sender,
            self.air.dclassesByName['DistributedToonUD'],
            {'setFriendsList' : [newList]})
        self.demand('Off')


# -- Avatar Details --
class FriendDetailsOperation(OperationFSM):

    def __init__(self, mgr, air, senderAvId, targetAvId=None, callback=None, friendIds=None):
        OperationFSM.__init__(self, mgr, air, senderAvId, targetAvId, callback)
        self.friendIds = friendIds

    def enterStart(self):
        self.air.dbInterface.queryObject(self.air.dbId, self.sender,
            self.handleRetrieve)

    def handleRetrieve(self, dclass, fields):
        if dclass != self.air.dclassesByName['DistributedToonUD']:
            self.demand('Error', 'Distributed Class was not a Toon.')
            return

        self.demand('Retrieved', fields['setFriendsList'][0])

    def enterRetrieved(self, friendsList):
        self.currId = 0
        for id in self.friendIds:
            for friend in friendsList:
                if friend[0] == id:
                    self.currId = id
                    self.air.dbInterface.queryObject(self.air.dbId, id,
                        self.handleFriend)
                    break
        self.demand('Off')

        def handleFriend(dclass, fields):
            if dclass != self.air.dclassesByName['DistributedToonUD']:
                return
            name = fields['setName'][0]
            dna = fields['setDNAString'][0]
            petId = fields['setPetId'][0]
            self.sendUpdateToAvatarId(avId, 'friendInfo', [self.currId,
             name,
             dna,
             petId])


# -- Clear List --
class ClearListOperation(OperationFSM):

    def enterStart(self):
        self.air.dbInterface.queryObject(self.air.dbId, self.sender,
            self.handleRetrieved)

    def handleRetrieved(self, dclass, fields):
        if dclass != self.air.dclassesByName['DistributedToonUD']:
            self.demand('Error', 'Distributed Class was not a Toon.')
            return
        self.demand('Retrieved', fields['setFriendsList'][0])

    def enterRetrieved(self, friendsList):
        for friend in friendsList:
            newOperation = RemoveFriendOperation(self.mgr, self.air, friend[0],
                targetAvId=self.sender, alert=True)
            self.mgr.operations.append(newOperation)
            newOperation.demand('Start')
        self.demand('Off')

# -- FriendsManager --

class TTRFriendsManagerUD(DistributedObjectGlobalUD):
    notify = directNotify.newCategory('TTRFriendsManagerUD')

    def announceGenerate(self):
        DistributedObjectGlobalUD.announceGenerate(self)

        self.onlineToons = []
        self.tpRequests = {}
        self.whisperRequests = {}
        self.operations = []
        self.secret2avId = {}
        self.delayTime = 1.0

    # -- Friends list --
    def requestFriendsList(self):
        avId = self.air.getAvatarIdFromSender()
        newOperation = FriendsListOperation(self, self.air, avId,
            callback = self.sendFriendsList)
        self.operations.append(newOperation)
        newOperation.demand('Start')

    def sendFriendsList(self, sender, friendsList):
        self.sendUpdateToAvatarId(sender, 'friendList', [friendsList])
        if sender not in self.onlineToons:
            self.toonOnline(sender, friendsList)

    # -- Remove Friend --
    def removeFriend(self, friendId):
        avId = self.air.getAvatarIdFromSender()

        # Sender remove Friend
        newOperation = RemoveFriendOperation(self, self.air, avId, friendId)
        self.operations.append(newOperation)
        newOperation.demand('Start')

        # Friend remove Sender
        newOperation = RemoveFriendOperation(self, self.air, friendId, avId,
            alert=True)
        self.operations.append(newOperation)
        newOperation.demand('Start')

    # -- Avatar Info --
    def requestAvatarInfo(self, friendIdList):
        avId = self.air.getAvatarIdFromSender()
        newOperation = FriendDetailsOperation(self, self.air, avId,
            friendIds = friendIdList)
        self.operations.append(newOperation)
        newOperation.demand('Start')

    def getAvatarDetails(self, avId):
        senderId = self.air.getAvatarIdFromSender()
        def handleToon(dclass, fields):
            if dclass != self.air.dclassesByName['DistributedToonUD']:
                return       
            experience = fields['setExperience'][0]
            trackAccess = fields['setTrackAccess'][0]
            trackBonusLevel =fields['setTrackBonusLevel'][0]
            inventory = fields['setInventory'][0]
            hp = fields['setHp'][0]
            maxHp = fields['setMaxHp'][0]
            defaultShard = fields['setDefaultShard'][0]
            lastHood = fields['setLastHood'][0]
            dnaString =  fields['setDNAString'][0]
            setLastSeen = fields.get('setLastSeen', [0])[0]
            self.sendUpdateToAvatarId(senderId, 'friendDetails', [avId, experience, trackAccess, trackBonusLevel , inventory, hp, maxHp, defaultShard, lastHood, dnaString, setLastSeen])
        self.air.dbInterface.queryObject(self.air.dbId, avId, handleToon)

    # -- Toon Online/Offline --
    def toonOnline(self, doId, friendsList):
        self.onlineToons.append(doId)

        channel = self.GetPuppetConnectionChannel(doId)
        dgcleanup = self.dclass.aiFormatUpdate('goingOffline', self.doId, self.doId, self.air.ourChannel, [doId])
        dg = PyDatagram()
        dg.addServerHeader(channel, self.air.ourChannel, CLIENTAGENT_ADD_POST_REMOVE)
        dg.addString(dgcleanup.getMessage())
        self.air.send(dg)

        for friend in friendsList:
            friendId = friend[0]
            if friend[0] in self.onlineToons:
                self.sendUpdateToAvatarId(doId, 'friendOnline', [friendId, 0, 0])
            self.sendUpdateToAvatarId(friendId, 'friendOnline', [doId, 0, 0])

    def goingOffline(self, avId):
        self.toonOffline(avId)

    def toonOffline(self, doId):
        if doId not in self.onlineToons:
            return
        def handleToon(dclass, fields):
            if dclass != self.air.dclassesByName['DistributedToonUD']:
                return
            friendsList = fields['setFriendsList'][0]
            for friend in friendsList:
                friendId = friend[0]
                if friendId in self.onlineToons:
                    self.sendUpdateToAvatarId(friendId, 'friendOffline', [doId])
            if doId in self.onlineToons:
                self.onlineToons.remove(doId)
        self.air.dbInterface.queryObject(self.air.dbId, doId, handleToon)

    # -- Clear List --
    def clearList(self, doId):
        newOperation = ClearListOperation(self, self.air, doId)
        self.operations.append(newOperation)
        newOperation.demand('Start')

    # -- Teleport and Whispers --
    def routeTeleportQuery(self, toId):
        fromId = self.air.getAvatarIdFromSender()
        if fromId in self.tpRequests.values():
            return
        self.tpRequests[fromId] = toId
        self.sendUpdateToAvatarId(toId, 'teleportQuery', [fromId])
        taskMgr.doMethodLater(5, self.giveUpTeleportQuery, 'tp-query-timeout-%d' % fromId, extraArgs=[fromId, toId])

    def giveUpTeleportQuery(self, fromId, toId):
        # The client didn't respond to the query within the set time,
        # So we will tell the query sender that the toon is unavailable.
        if fromId in self.tpRequests:
            del self.tpRequests[fromId]
            self.sendUpdateToAvatarId(fromId, 'setTeleportResponse', [toId, 0, 0, 0, 0])
            self.notify.warning('Teleport request that was sent by %d to %d timed out.' % (fromId, toId))

    def teleportResponse(self, toId, available, shardId, hoodId, zoneId):
        # Here is where the toId and fromId swap (because we are now sending it back)
        fromId = self.air.getAvatarIdFromSender()

        # We got the query response, so no need to give up!
        if taskMgr.hasTaskNamed('tp-query-timeout-%d' % toId):
            taskMgr.remove('tp-query-timeout-%d' % toId)

        if toId not in self.tpRequests:
            return
        if self.tpRequests.get(toId) != fromId:
            self.air.writeServerEvent('suspicious', fromId, 'toon tried to send teleportResponse for a query that isn\'t theirs!')
            return
        self.sendUpdateToAvatarId(toId, 'setTeleportResponse', [fromId, available, shardId, hoodId, zoneId])
        del self.tpRequests[toId]

    def whisperSCTo(self, toId, msgIndex):
        fromId = self.air.getAvatarIdFromSender()
        currStamp = time.time()
        if fromId in self.whisperRequests:
            elapsed = currStamp - self.whisperRequests[fromId]
            if elapsed < self.delayTime:
                self.whisperRequests[fromId] = currStamp
                return
        self.whisperRequests[fromId] = currStamp
        self.sendUpdateToAvatarId(toId, 'setWhisperSCFrom', [fromId, msgIndex])

    def whisperSCCustomTo(self, toId, msgIndex):
        fromId = self.air.getAvatarIdFromSender()
        currStamp = time.time()
        if fromId in self.whisperRequests:
            elapsed = currStamp - self.whisperRequests[fromId]
            if elapsed < self.delayTime:
                self.whisperRequests[fromId] = currStamp
                return
        self.whisperRequests[fromId] = currStamp
        self.sendUpdateToAvatarId(toId, 'setWhisperSCCustomFrom', [fromId, msgIndex])

    def whisperSCEmoteTo(self, toId, msgIndex):
        fromId = self.air.getAvatarIdFromSender()
        currStamp = time.time()
        if fromId in self.whisperRequests:
            elapsed = currStamp - self.whisperRequests[fromId]
            if elapsed < self.delayTime:
                self.whisperRequests[fromId] = currStamp
                return
        self.whisperRequests[fromId] = currStamp
        self.sendUpdateToAvatarId(toId, 'setWhisperSCEmoteFrom', [fromId, msgIndex])

    def sendTalkWhisper(self, toId, message):
        fromId = self.air.getAvatarIdFromSender()
        currStamp = time.time()
        if fromId in self.whisperRequests:
            elapsed = currStamp - self.whisperRequests[fromId]
            if elapsed < self.delayTime:
                self.whisperRequests[fromId] = currStamp
                return
        self.whisperRequests[fromId] = currStamp
        self.sendUpdateToAvatarId(toId, 'receiveTalkWhisper', [fromId, message])
        self.air.writeServerEvent('whisper-said', fromId, toId, message)

    # -- Secret Friends --
    def requestSecret(self):
        avId = self.air.getAvatarIdFromSender()
        allowed = string.lowercase + string.digits
        secret = ''
        for i in xrange(6):
            secret += random.choice(allowed)
            if i == 2:
                secret += ' '
        self.secret2avId[secret] = avId
        self.sendUpdateToAvatarId(avId, 'requestSecretResponse', [1, secret])

    def submitSecret(self, secret):
        requester = self.air.getAvatarIdFromSender()
        owner = self.secret2avId.get(secret)
        if not owner:
            self.sendUpdateToAvatarId(requester, 'submitSecretResponse', [0, 0])
            return
        if owner == requester:
            del self.secret2avId[secret]
            self.sendUpdateToAvatarId(requester, 'submitSecretResponse', [3, 0])
            return

        self.sendUpdateToAvatarId(requester, 'submitSecretResponse', [5, 0])

    # -- Routes --
    def battleSOS(self, toId):
        requester = self.air.getAvatarIdFromSender()
        self.sendUpdateToAvatarId(toId, 'setBattleSOS', [requester])

    def teleportGiveup(self, toId):
        requester = self.air.getAvatarIdFromSender()
        self.sendUpdateToAvatarId(toId, 'setTeleportGiveup', [requester])

    def whisperSCToontaskTo(self, toId, taskId, toNpcId, toonProgress, msgIndex):
        requester = self.air.getAvatarIdFromSender()
        self.sendUpdateToAvatarId(toId, 'setWhisperSCToontaskFrom', [requester,
            taskId, toNpcId, toonProgress, msgIndex]
        )

    def sleepAutoReply(self, toId):
        requester = self.air.getAvatarIdFromSender()
        self.sendUpdateToAvatarId(toId, 'setSleepAutoReply', [requester])
    
    
    
