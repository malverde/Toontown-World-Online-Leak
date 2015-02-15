########################## THE TOON LAND PROJECT ##########################
# Filename: HackerCrypt.py
# Created by: Cody/Fd Green Cat Fd (January 31st, 2013)
####
# Description:
#
# Encryption method written by Team FD in 2011 for their personal releases.
# The script has been modified to meet Toon Land's coding standards.
####

from base64 import b64encode, b64decode
from binascii import hexlify, unhexlify
from random import randrange

from __main__ import __dict__ as __main__
from bz2 import compress as c_bz2
from bz2 import decompress as d_bz2
from zlib import compress as c_zlib
from zlib import decompress as d_zlib
from sha import sha as sha1

class HackerCrypt:

    __version__ = 'v1.2.0.2'

    def __init__(self):
        self.MAGIC = sha1('[TL]').digest()
        self.KEY   = sha1('TL-Cookies').digest()

    def makeIV(self):
        iv = ''
        for i in range(4):
            iv += chr(randrange(256))
        return iv

    def rc4(self, data, key):
        j = 0
        s = range(256)
        for i in range(256):
            j = (j + s[i] + ord(key[i % len(key)])) % 256
            s[i], s[j] = s[j], s[i]
        j = i = 0
        results = []
        for c in data:
            j = (j + 1) % 256
            i = (i + s[j]) % 256
            s[j], s[i] = s[i], s[j]
            results.append(chr(ord(c) ^ s[(s[j] + s[i]) % 256]))
        return ''.join(results)

    def encode(self, data):
        b64 = b64encode(data)
        hex = hexlify(b64)
        encoded = list(hexlify(hex))
        for x in range(len(encoded)):
            alpha = int(encoded[x]) + 2
            encoded[x] = chr(alpha)
        return ''.join(encoded)

    def decode(self, encoded):
        encoded = list(encoded)
        for x in range(len(encoded)):
            alpha = str(encoded[x])
            encoded[x] = str(ord(alpha) - 2)
        encoded = unhexlify(''.join(encoded))
        unhexed = unhexlify(encoded)
        return b64decode(unhexed)

    def compress(self, data):
        bz2 = b64encode(c_bz2(data))
        return c_zlib(hexlify(bz2))

    def decompress(self, compressed):
        unhexed = unhexlify(d_zlib(compressed))
        return d_bz2(b64decode(unhexed))

    def encrypt(self, data):
        compressed = self.compress(data)
        encoded = self.encode(compressed)
        data = self.MAGIC + encoded
        iv = self.makeIV()
        key = self.KEY + iv
        return iv + self.rc4(data, key)

    def decrypt(self, encrypted):
        if len(encrypted) < 4:
            return None
        iv = encrypted[:4]
        data = encrypted[4:]
        key = self.KEY + iv
        data = self.rc4(data, key)
        if not data.startswith(self.MAGIC):
            return None
        decoded = self.decode(data[len(self.MAGIC):])
        return self.decompress(decoded)