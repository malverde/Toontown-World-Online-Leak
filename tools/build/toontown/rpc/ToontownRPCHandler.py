import datetime
from direct.distributed.MsgTypes import CLIENTAGENT_EJECT
from direct.distributed.PyDatagram import PyDatagram
from direct.stdpy import threading2
import re

from otp.distributed import OtpDoGlobals
from toontown.distributed.ShardStatusReceiver import ShardStatusReceiver
from toontown.rpc.ToontownRPCHandlerBase import *
from toontown.suit.SuitInvasionGlobals import INVASION_TYPE_NORMAL
from toontown.toon import ToonDNA
from toontown.toonbase import TTLocalizer
from toontown.uberdog.ClientServicesManagerUD import executeHttpRequest


class ToontownRPCHandler(ToontownRPCHandlerBase):
    def __init__(self, air):
        ToontownRPCHandlerBase.__init__(self, air)

        self.shardStatus = ShardStatusReceiver(air)

    # --- TESTS ---

    @rpcmethod(accessLevel=COMMUNITY_MANAGER)
    def rpc_ping(self, data):
        """
        Summary:
            Responds with the provided [data]. This method exists for testing
            purposes.

        Parameters:
            [any data] = The data to be given back in response.

        Example response: 'pong'
        """
        return data

    # --- GENERAL ---

    @rpcmethod(accessLevel=SYSTEM_ADMINISTRATOR)
    def rpc_queryObject(self, doId):
        """
        Summary:
            Responds with the values of all database fields associated with the
            provided [doId].

        Parameters:
            [int doId] = The ID of the object to query database fields on.

        Example response:
            On success: ['DistributedObject', {'fieldName': ('arg1', ...), ...}]
            On failure: [None, None]
        """
        result = []
        unblocked = threading2.Event()


        def callback(dclass, fields):
            if dclass is not None:
                dclass = dclass.getName()
            result.extend([dclass, fields])
            unblocked.set()


        self.air.dbInterface.queryObject(self.air.dbId, doId, callback)

        # Block until the callback is executed:
        unblocked.wait()

        return result

    @rpcmethod(accessLevel=SYSTEM_ADMINISTRATOR)
    def rpc_updateObject(self, doId, dclassName, newFields, oldFields=None):
        """
        Summary:
            Update the field(s) of the object associated with the provided
            [doId]. If <oldFields> is provided, then this method will fail if
            the object's current fields don't match.

        Parameters:
            [int doId] = The ID of the object whose fields are to be updated.
            [str dclassName] = The name of the object's DClass.
            [dict newFields] = The new field values.
            <dict oldFields> = The old field values to assert.

        Example response:
            On success: True
            On failure: False
        """
        # Ensure that the provided DClass exists:
        if dclassName not in self.air.dclassesByName:
            dclassName += 'UD'
            if dclassName not in self.air.dclassesByName:
                return False

        dclass = self.air.dclassesByName[dclassName]

        if oldFields is None:
            self.air.dbInterface.updateObject(
                self.air.dbId, doId, dclass, newFields)
            return True

        result = [True]
        unblocked = threading2.Event()


        def callback(fields):
            if fields is not None:
                result[0] = False
            unblocked.set()


        self.air.dbInterface.updateObject(
            self.air.dbId, doId, dclass, newFields, oldFields=oldFields,
            callback=callback)

        # Block until the callback is executed:
        unblocked.wait()

        return result[0]

    @rpcmethod(accessLevel=SYSTEM_ADMINISTRATOR)
    def rpc_setField(self, doId, dclassName, fieldName, args=[]):
        """
        Summary:
            Set the value of the field named [fieldName] on the suggested
            object.

        Parameters:
            [int doId] = The ID of the object whose field is being modified.
            [str dclassName] = The name of the object's DClass.
            [str fieldName] = The name of the field to be modified.
            [list args] = The new value for the field.

        Example response:
            On success: True
            On failure: False
        """
        # Ensure that the provided DClass exists:
        if dclassName not in self.air.dclassesByName:
            dclassName += 'UD'
            if dclassName not in self.air.dclassesByName:
                return False

        dclass = self.air.dclassesByName[dclassName]

        datagram = dclass.aiFormatUpdate(
            fieldName, doId, doId, self.air.ourChannel, args)
        self.air.send(datagram)

        return True

    # --- MESSAGES ---

    @rpcmethod(accessLevel=SYSTEM_ADMINISTRATOR)
    def rpc_messageChannel(self, channel, message):
        """
        Summary:
            Broadcasts a [message] to any client whose Client Agent is
            subscribed to the provided [channel].

        Parameters:
            [int channel] = The channel to direct the message to.
            [str message] = The message to broadcast.
        """
        dclass = self.air.dclassesByName['ClientServicesManagerUD']
        datagram = dclass.aiFormatUpdate(
            'systemMessage', OtpDoGlobals.OTP_DO_ID_CLIENT_SERVICES_MANAGER,
            channel, 1000000, [message])
        self.air.send(datagram)

    @rpcmethod(accessLevel=SYSTEM_ADMINISTRATOR)
    def rpc_messageAll(self, message):
        """
        Summary: Broadcasts a [message] to all clients.

        Parameters:
            [str message] = The message to broadcast.
        """
        self.rpc_messageChannel(10, message)

    @rpcmethod(accessLevel=SYSTEM_ADMINISTRATOR)
    def rpc_messageShard(self, shardId, message):
        """
        Summary:
            Broadcasts a [message] to all clients under the provided [shardId].

        Parameters:
            [int shardId] = The ID of the shard to direct the message to.
            [str message] = The message to broadcast.
        """
        # Get the ID of the ToontownDistrict object:
        districtId = shardId + 1

        # Use it to get the uber zone's channel:
        channel = (districtId<<32) | 2

        self.rpc_messageChannel(channel, message)

    @rpcmethod(accessLevel=MODERATOR)
    def rpc_messageStaff(self, message):
        """
        Summary:
            Broadcasts a [message] to any client whose access level is higher
            than that of a standard user.

        Parameters:
            [str message] = The message to broadcast.
        """
        self.rpc_messageChannel(OtpDoGlobals.OTP_STAFF_CHANNEL, message)

    @rpcmethod(accessLevel=MODERATOR)
    def rpc_messageUser(self, userId, message):
        """
        Summary:
            Sends a [message] to the client associated with the provided
            [userId].

        Parameters:
            [int/str userId] = The ID of the user to send the message to.
            [str message] = The message to send.
        """
        accountId = self.rpc_getUserAccountId(userId)
        if accountId is not None:
            self.rpc_messageAccount(accountId, message)

    @rpcmethod(accessLevel=MODERATOR)
    def rpc_messageAccount(self, accountId, message):
        """
        Summary:
            Sends a [message] to the client associated with the provided
            [accountId].

        Parameters:
            [int accountId] = The ID of the account to send the message to.
            [str message] = The message to send.
        """
        channel = accountId + (1003L<<32)
        self.rpc_messageChannel(channel, message)

    @rpcmethod(accessLevel=MODERATOR)
    def rpc_messageAvatar(self, avId, message):
        """
        Summary:
            Sends a [message] to the client associated with the provided
            [avId].

        Parameters:
            [int avId] = The ID of the avatar to send the message to.
            [str message] = The message to send.
        """
        channel = avId + (1001L<<32)
        self.rpc_messageChannel(channel, message)

    # --- KICKS ---

    @rpcmethod(accessLevel=SYSTEM_ADMINISTRATOR)
    def rpc_kickChannel(self, channel, code, reason):
        """
        Summary:
            Kicks any client whose Client Agent is subscribed to the provided
            [channel].

        Parameters:
            [int channel] = The channel to kick.
            [int code] = The code for the kick.
            [str reason] = The reason for the kick.
        """
        datagram = PyDatagram()
        datagram.addServerHeader(channel, self.air.ourChannel, CLIENTAGENT_EJECT)
        datagram.addUint16(code)
        datagram.addString(reason)
        self.air.send(datagram)

    @rpcmethod(accessLevel=SYSTEM_ADMINISTRATOR)
    def rpc_kickAll(self, code, reason):
        """
        Summary: Kicks all clients.

        Parameters:
            [int code] = The code for the kick.
            [str reason] = The reason for the kick.
        """
        self.rpc_kickChannel(10, code, reason)

    @rpcmethod(accessLevel=SYSTEM_ADMINISTRATOR)
    def rpc_kickShard(self, shardId, code, reason):
        """
        Summary: Kicks all clients under the provided [shardId].

        Parameters:
            [int shardId] = The ID of the shard to kick.
            [int code] = The code for the kick.
            [str reason] = The reason for the kick.
        """
        # Get the ID of the ToontownDistrict object:
        districtId = shardId + 1

        # Use it to get the uber zone's channel:
        channel = (districtId<<32) | 2

        self.rpc_kickChannel(channel, code, reason)

    @rpcmethod(accessLevel=MODERATOR)
    def rpc_kickUser(self, userId, code, reason):
        """
        Summary: Kicks the client associated with the provided [userId].

        Parameters:
            [int/str userId] = The ID of the user to kick.
            [int code] = The code for the kick.
            [str reason] = The reason for the kick.
        """
        accountId = self.rpc_getUserAccountId(userId)
        if accountId is not None:
            self.rpc_kickAccount(accountId, code, reason)

    @rpcmethod(accessLevel=MODERATOR)
    def rpc_kickAccount(self, accountId, code, reason):
        """
        Summary: Kicks the client associated with the provided [accountId].

        Parameters:
            [int accountId] = The ID of the account to kick.
            [int code] = The code for the kick.
            [str reason] = The reason for the kick.
        """
        channel = accountId + (1003L<<32)
        self.rpc_kickChannel(channel, code, reason)

    @rpcmethod(accessLevel=MODERATOR)
    def rpc_kickAvatar(self, avId, code, reason):
        """
        Summary: Kicks the client associated with the provided [avId].

        Parameters:
            [int avId] = The ID of the avatar to kick.
            [int code] = The code for the kick.
            [str reason] = The reason for the kick.
        """
        channel = avId + (1001L<<32)
        self.rpc_kickChannel(channel, code, reason)

    # --- BANS ---

    @rpcmethod(accessLevel=MODERATOR)
    def rpc_banUser(self, userId, duration, reason):
        """
        Summary:
            Bans the user associated with the provided [userId] for the
            specified [duration].

        Parameters:
            [int/str userId] = The ID of the user to ban.
            [int duration] = The ban's duration in hours. If this is 0 or less,
                the user will be permanently banned.
            [str reason] = A short description of why this user is being
                banned. This can be one of the following values: 'hacking',
                'language', 'other'.

        Example response:
            On success: True
            On failure: False
        """
        if reason not in ('hacking', 'language', 'other'):
            return False
        self.air.writeServerEvent('ban', userId, duration, reason)
        if duration > 0:
            now = datetime.date.today()
            release = str(now + datetime.timedelta(hours=duration))
        else:
            release = '0000-00-00'  # Permanent ban.
        executeHttpRequest('accounts/ban/', Id=userId, Release=release,
                           Reason=reason)
        self.rpc_kickUser(userId, 152, reason)
        return True

    @rpcmethod(accessLevel=MODERATOR)
    def rpc_banAccount(self, accountId, duration, reason):
        """
        Summary:
            Bans the user associated with the provided [accountId] for the
            specified [duration].

        Parameters:
            [int accountId] = The ID of the account associated with the user to
                ban.
            [int duration] = The ban's duration in hours. If this is 0 or less,
                the user will be permanently banned.
            [str reason] = A short description of why this user is being
                banned. This can be one of the following values: 'hacking',
                'language', 'other'.

        Example response:
            On success: True
            On failure: False
        """
        userId = self.rpc_getAccountUserId(accountId)
        return self.rpc_banUser(userId, duration, reason)

    @rpcmethod(accessLevel=MODERATOR)
    def rpc_banAvatar(self, avId, duration, reason):
        """
        Summary:
            Bans the user associated with the provided [avId] for the specified
            [duration].

        Parameters:
            [int/str avId] = The ID of the avatar associated with the user to
                be banned.
            [int duration] = The ban's duration in hours. If this is 0 or less,
                the user will be permanently banned.
            [str reason] = A short description of why this user is being
                banned. This can be one of the following values: 'hacking',
                'language', 'other'.

        Example response:
            On success: True
            On failure: False
        """
        userId = self.rpc_getAvatarUserId(avId)
        return self.rpc_banUser(userId, duration, reason)

    # --- USERS ---

    @rpcmethod(accessLevel=MODERATOR)
    def rpc_getUserAccountId(self, userId):
        """
        Summary:
            Responds with the ID of the account associated with the provided
            [userId].

        Parameters:
            [int/str userId] = The ID of the user to query the account ID on.

        Example response:
            On success: 100000000
            On failure: None
        """
        if str(userId) in self.air.csm.accountDB.dbm:
            return int(self.air.csm.accountDB.dbm[str(userId)])

    @rpcmethod(accessLevel=MODERATOR)
    def rpc_getUserAvatars(self, userId):
        """
        Summary:
            Responds with a list of avatar IDs associated with the provided
            [userId].

        Parameters:
            [int/str userId] = The ID of the user to query the avatars on.

        Example response:
            On success: [0, 100000001, 0, 0, 0, 0]
            On failure: None
        """
        accountId = self.rpc_getUserAccountId(userId)
        if accountId is not None:
            return self.rpc_getAccountAvatars(accountId)

    @rpcmethod(accessLevel=MODERATOR)
    def rpc_getUserDeletedAvatars(self, userId):
        """
        Summary:
            Responds with a list of deleted avatar IDs associated with the
            provided [userId], along with the time at which each avatar was
            deleted.

        Parameters:
            [int/str userId] = The ID of the user to query the deleted avatars
                on.

        Example response:
            On success: [[100000001, 1409665000], ...]
            On failure: None
        """
        accountId = self.rpc_getUserAccountId(userId)
        if accountId is not None:
            return self.rpc_getAccountDeletedAvatars(accountId)

    # --- ACCOUNTS ---

    @rpcmethod(accessLevel=MODERATOR)
    def rpc_getAccountUserId(self, accountId):
        """
        Summary:
            Responds with the ID of the user associated with the provided
            [accountId].

        Parameters:
            [int accountId] = The ID of the account to query the user ID on.

        Example response:
            On success: 1
            On failure: None
        """
        dclassName, fields = self.rpc_queryObject(accountId)
        if dclassName == 'Account':
            return fields['ACCOUNT_ID']

    @rpcmethod(accessLevel=MODERATOR)
    def rpc_getAccountAvatars(self, accountId):
        """
        Summary:
            Responds with a list of avatar IDs associated with the provided
            [accountId].

        Parameters:
            [int accountId] = The ID of the account to query the avatar IDs on.

        Example response:
            On success: [0, 100000001, 0, 0, 0, 0]
            On failure: None
        """
        dclassName, fields = self.rpc_queryObject(accountId)
        if dclassName == 'Account':
            return fields['ACCOUNT_AV_SET']

    @rpcmethod(accessLevel=MODERATOR)
    def rpc_getAccountDeletedAvatars(self, accountId):
        """
        Summary:
            Responds with a list of deleted avatar IDs associated with the
            provided [accountId], along with the time at which each avatar was
            deleted.

        Parameters:
            [int accountId] = The ID of the account to query the deleted
                avatars on.

        Example response:
            On success: [[100000001, 1409665000], ...]
            On failure: None
        """
        dclassName, fields = self.rpc_queryObject(accountId)
        if dclassName == 'Account':
            return fields['ACCOUNT_AV_SET_DEL']

    # --- AVATARS ---

    @rpcmethod(accessLevel=MODERATOR)
    def rpc_getAvatarUserId(self, avId):
        """
        Summary:
            Responds with the ID of the user associated with the provided
            [avId].

        Parameters:
            [int avId] = The ID of the avatar to query the user ID on.

        Example response:
            On success: 1
            On failure: None
        """
        accountId = self.rpc_getAvatarAccountId(avId)
        if accountId is not None:
            return self.rpc_getAccountUserId(accountId)

    @rpcmethod(accessLevel=MODERATOR)
    def rpc_getAvatarAccountId(self, avId):
        """
        Summary:
            Responds with the ID of the account associated with the provided
            [avId].

        Parameters:
            [int avId] = The ID of the avatar to query the account ID on.

        Example response:
            On success: 100000000
            On failure: None
        """
        dclassName, fields = self.rpc_queryObject(avId)
        if dclassName == 'DistributedToon':
            return fields['setDISLid'][0]

    @rpcmethod(accessLevel=MODERATOR)
    def rpc_getAvatarAvatars(self, avId):
        """
        Summary:
            Responds with a list of avatar IDs associated with the provided
            [avId].

        Parameters:
            [int avId] = The ID of the avatar to query the avatar IDs on.

        Example response:
            On success: [0, 100000001, 0, 0, 0, 0]
            On failure: None
        """
        accountId = self.rpc_getAvatarAccountId(avId)
        if accountId is not None:
            return self.rpc_getAccountAvatars(accountId)

    @rpcmethod(accessLevel=MODERATOR)
    def rpc_getAvatarDeletedAvatars(self, avId):
        """
        Summary:
            Responds with a list of deleted avatar IDs associated with the
            provided [avId], along with the time at which each avatar was
            deleted.

        Parameters:
            [int avId] = The ID of the avatar to query the deleted avatars on.

        Example response:
            On success: [[100000001, 1409665000], ...]
            On failure: None
        """
        accountId = self.rpc_getAvatarAccountId(avId)
        if accountId is not None:
            return self.rpc_getAccountDeletedAvatars(accountId)

    @rpcmethod(accessLevel=MODERATOR)
    def rpc_getAvatarDetails(self, avId):
        """
        Summary:
            Responds with basic details on the avatar associated with the
            provided [avId].

        Parameters:
            [int avId] = The ID of the avatar to query basic details on.

        Example response:
            On success:
                {
                   'name': 'Toon Name',
                   'species': 'cat',
                   'head-color': 'Red',
                   'max-hp': 15,
                   'online': True
                }
            On failure: None
        """
        dclassName, fields = self.rpc_queryObject(avId)
        if dclassName == 'DistributedToon':
            result = {}

            result['name'] = fields['setName'][0]

            dna = ToonDNA.ToonDNA()
            dna.makeFromNetString(fields['setDNAString'][0])
            result['species'] = ToonDNA.getSpeciesName(dna.head)

            result['head-color'] = TTLocalizer.NumToColor[dna.headColor]
            result['max-hp'] = fields['setMaxHp'][0]
            result['online'] = (avId in self.air.friendsManager.onlineToons)

            return result

    @rpcmethod(accessLevel=MODERATOR)
    def rpc_findAvatarsByName(self, needle):
        """
        Summary:
            Responds with the IDs of each avatar whose name matches, or
            contains the provided [needle].

        Parameters:
            [str needle] = The string to filter avatars by name with. This is
                case insensitive.

        Example response: [100000001, ...]
        """
        if not config.GetBool('want-mongo-client', False):
            return []
        if not needle:
            return []
        self.air.mongodb.astron.objects.ensure_index('fields.setName')
        exp = re.compile('.*%s.*' % needle, re.IGNORECASE)
        result = self.air.mongodb.astron.objects.find({'fields.setName._0': exp})
        return [avatar['_id'] for avatar in result]

    # --- SHARDS ---

    @rpcmethod(accessLevel=USER)
    def rpc_listShards(self):
        """
        Summary:
            Responds with the current status of each shard that has ever been
            created in the lifetime of the UberDOG.

        Example response:
            {
               401000000: {
                  'name': 'District Name'
                  'available': True,
                  'created': 1409665000,
                  'population': 150,
                  'invasion': {
                     'type': 'Flunky',
                     'flags': 0,
                     'remaining': 1000,
                     'total': 1000,
                     'start': 1409665000
                  }
               },
               ...
            }
        """
        return self.shardStatus.getShards()

    # --- INVASIONS ---

    @rpcmethod(accessLevel=ADMINISTRATOR)
    def rpc_startInvasion(self, shardId, suitDeptIndex=None, suitTypeIndex=None,
                          flags=0, type=INVASION_TYPE_NORMAL):
        """
        Summary:
            Starts an invasion under the provided [shardId] with the specified
            configuration.

        Parameters:
            [int shardId] = The ID of the shard to start the invasion in.
            <int/NoneType suitDeptIndex> = The invading Cog's department index.
            <int/NoneType suitTypeIndex> = The invading Cog's type index.
            <int flags> = Extra invasion flags.
            <int type> = The invasion type.
        """
        self.air.netMessenger.send(
            'startInvasion',
            [shardId, suitDeptIndex, suitTypeIndex, flags, type])

    @rpcmethod(accessLevel=ADMINISTRATOR)
    def rpc_stopInvasion(self, shardId):
        """
        Summary:
            Stops any invasion currently running under the provided [shardId].

        Parameters:
            [int shardId] = The ID of the shard that is running the invasion to
                be terminated.
        """
        self.air.netMessenger.send('stopInvasion', [shardId])

    # --- NAME APPROVAL ---

    @rpcmethod(accessLevel=MODERATOR)
    def rpc_approveName(self, avId):
        """
        Summary:
            Approves the pending name of the avatar associated with the
            provided [avId].

        Parameters:
            [int avId] = The ID of the avatar whose pending name is to be
                approved.

        Example response:
            On success: True
            On failure: False
        """
        newFields = {'WishNameState': 'APPROVED'}
        oldFields = {'WishNameState': 'PENDING'}
        return self.rpc_updateObject(
            avId, 'DistributedToonUD', newFields, oldFields=oldFields)

    @rpcmethod(accessLevel=MODERATOR)
    def rpc_rejectName(self, avId):
        """
        Summary:
            Rejects the pending name of the avatar associated with the provided
            [avId].

        Parameters:
            [int avId] = The ID of the avatar whose pending name is to be
                rejected.

        Example response:
            On success: True
            On failure: False
        """
        newFields = {'WishNameState': 'REJECTED'}
        oldFields = {'WishNameState': 'PENDING'}
        return self.rpc_updateObject(
            avId, 'DistributedToonUD', newFields, oldFields=oldFields)
