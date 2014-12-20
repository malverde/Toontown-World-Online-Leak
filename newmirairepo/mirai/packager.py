from marshaller import loads, dumps
from cStringIO import StringIO
import hashlib
import struct
import subprocess
import imp
import sys

class MiraiUnpackager(object):
    AES_KEY = '\x14\x8B\xA2\xDA\xE8\x0E\x5B\x29\xCE\x25\xFD\xCF\x7B\x80\x08\x99'

    def __init__(self):
        self.modules = {}
        self.digest = hashlib.sha256()

    def load(self, filename):
        self.modules = {}
        self.digest = hashlib.sha256()

        with open(filename, 'rb') as f:
            openssl = subprocess.Popen(['openssl', 'enc', '-d',
                                        '-K', self.AES_KEY.encode('hex'),
                                        '-iv', '00'*16,
                                        '-aes-128-cbc', '-nopad'],
                stdin=f, stdout=subprocess.PIPE)
            stdout, stderr = openssl.communicate()
            stdout = StringIO(stdout)

            self.read_modules(stdout)

            digestbytes = stdout.tell()
            f.seek(0)
            self.digest.update(f.read(digestbytes))

            self.verify_signature(f)

    def verify_signature(self, f):
        digest = f.read(32) # Read SHA256 digest...
        if digest != self.digest.digest():
            raise ValueError('Signature is incorrect!')

    def read_modules(self, f):
        while self.read_module(f): pass

    def read_module(self, f):
        f.read(16) # Discard 16 bytes of padding...

        # A little ugly, but it works:
        name = ''
        while True:
            byte = f.read(1)
            if byte == '\x00': break
            name += byte

        if name == '':
            # Discard the post-padding:
            total = 16 + len(name)+1
            if total % 16:
                # We're not directly on the 16-byte boundary: Discard padding.
                f.read(16 - (total%16))
            return False

        size, = struct.unpack('<i', f.read(4))
        is_package = (size < 0)
        size = abs(size)

        # Now read data:
        rawcode = f.read(size)

        # Discard the post-padding:
        total = 16 + len(name)+1 + 4 + size
        if total % 16:
            # We're not directly on the 16-byte boundary: Discard padding.
            f.read(16 - (total%16))

        self.modules[name] = (is_package, loads(rawcode))
        return True

    def find_module(self, name, path=None):
        if name in self.modules:
            return self
        else:
            return None

    def load_module(self, name):
        if name in sys.modules:
            return sys.modules[name]

        is_package, code = self.modules[name]

        mod = imp.new_module(name)
        sys.modules[name] = mod
        mod.__loader__ = self
        mod.__file__ = code.co_name
        if is_package:
            mod.__path__ = []
            mod.__package__ = name
        else:
            mod.__package__ = name.rpartition('.')[0]

        exec(code, mod.__dict__)
        return mod

class MiraiPackager(object):
    # AES key must be 16 bytes and should be kept super secret. I've disguised
    # this key as a string to make it a little deceptive to would-be attackers.
    AES_KEY = '\x14\x8B\xA2\xDA\xE8\x0E\x5B\x29\xCE\x25\xFD\xCF\x7B\x80\x08\x99'

    # Salts: These don't have to be cryptographically secure, they're just used
    # for deterministic IV/sorting.
    IV_SALT = "What the heck, I'm seriously using MD5??!"
    SORT_SALT = "I guess MD5 is fine as a non-cryptographically-secure PRNG..."

    def __init__(self, filename):
        self.filename = filename
        self.file = open(filename, 'wb')
        self.digest = hashlib.sha256()

    def sort_key(self, modname):
        key, = struct.unpack('<Q', hashlib.md5(modname + self.SORT_SALT).digest()[:8])
        return key

    def write_modules(self, modules):
        modlist = sorted(modules, key=self.sort_key)
        for i, modname in enumerate(modlist):
            print '%i / %i' % (i, len(modlist))
            is_package, code = modules[modname]
            self.write_module(modname, is_package, code)

    def write_module(self, modname, is_package, code):
        rawcode = dumps(code)

        data = ''
        data += modname + '\0'
        data += struct.pack('<i', len(rawcode) * (-1 if is_package else 1))
        data += rawcode

        # Pad to align with 16-byte boundary.
        if len(data) % 16:
            # We're not directly on the 16-byte boundary: Add padding.
            data += 'x'*(16 - (len(data)%16))

        data = self.encrypt(modname, data)
        self.digest.update(data)
        self.file.write(data)

    def encrypt(self, seed, data):
        iv = hashlib.md5(seed + self.IV_SALT).digest()

        openssl = subprocess.Popen(['openssl', 'enc', '-e',
                                    '-K', self.AES_KEY.encode('hex'),
                                    '-iv', iv.encode('hex'),
                                    '-aes-128-cbc', '-nopad'],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE)

        output = iv
        output += openssl.communicate(data)[0]
        return output

    def close(self):
        # Write the lead-out:
        data = self.encrypt('leadout', '\x00'*16)
        self.digest.update(data)
        self.file.write(data)

        # Write the digest (TODO this should be a full signature...)
        self.file.write(self.digest.digest())

        self.file.close()
