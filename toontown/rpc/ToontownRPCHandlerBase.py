from direct.directnotify.DirectNotifyGlobal import directNotify
import json
import time

from Crypto.Cipher import AES


UNKNOWN = 700
USER = 100
COMMUNITY_MANAGER = 200
MODERATOR = 300
ARTIST = 400
PROGRAMMER = 500
ADMINISTRATOR = 600
SYSTEM_ADMINISTRATOR = 700


class RPCMethod:
    def __init__(self, accessLevel=UNKNOWN):
        self.accessLevel = accessLevel

    def __call__(self, method):
        method.accessLevel = self.accessLevel
        return method


rpcmethod = RPCMethod


class ToontownRPCHandlerBase:
    notify = directNotify.newCategory('ToontownRPCHandlerBase')

    def __init__(self, air):
        self.air = air

    def authenticate(self, token, method):
        """
        Ensure the provided token is valid, and meets the access level
        requirements of the method.
        """
        # First, base64 decode the token:
        try:
            token = token.decode('base64')
        except TypeError:
            return (-32001, 'Token decode failure')

        # Ensure this token is a valid size:
        if (not token) or ((len(token) % 16) != 0):
            return (-32002, 'Invalid token length')

        # Next, decrypt the token using AES-128 in CBC mode:
        rpcServerSecret = config.GetString('rpc-server-secret', '6163636f756e7473')

        # Ensure that our secret is the correct size:
        if len(rpcServerSecret) > AES.block_size:
            self.notify.error('rpc-server-secret is too big!')
        elif len(rpcServerSecret) < AES.block_size:
            self.notify.error('rpc-server-secret is too small!')

        # Take the initialization vector off the front of the token:
        iv = token[:AES.block_size]

        # Truncate the token to get our cipher text:
        cipherText = token[AES.block_size:]

        # Decrypt!
        cipher = AES.new(rpcServerSecret, mode=AES.MODE_CBC, IV=iv)
        try:
            token = json.loads(cipher.decrypt(cipherText).replace('\x00', ''))
            if ('timestamp' not in token) or (not isinstance(token['timestamp'], int)):
                raise ValueError
            if ('accesslevel' not in token) or (not isinstance(token['accesslevel'], int)):
                raise ValueError
        except ValueError:
            return (-32003, 'Invalid token')

        # Next, check if this token has expired:
        period = config.GetInt('rpc-token-period', 5)
        delta = int(time.time()) - token['timestamp']
        if delta > period:
            return (-32004, 'Token expired')

        if token['accesslevel'] < method.accessLevel:
            return (-32005, 'Insufficient access')
