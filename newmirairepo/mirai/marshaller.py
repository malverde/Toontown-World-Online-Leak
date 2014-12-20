import random
import marshal
import struct
import types
import hashlib
from StringIO import StringIO

MIRAISALT = "Remember when you tried to kill me twice?"

# The Mirai-specific bit:
def makeSBox(seed):
    sbox = range(256)

    for i in xrange(256):
        seed *= 0x61697473656c6543
        seed += 0x616e754c
        seed &= 0xFFFFFFFFFFFFFFFF
        b = seed>>56
        sbox[i], sbox[b] = sbox[b], sbox[i]

    return sbox

def invertSBox(sbox):
    inverse = [None]*256
    # This is so trivial:
    for i,v in enumerate(sbox):
        inverse[v] = i
    return inverse

def obfuscate(sbox, code):
    sbox = invertSBox(sbox)

    out = ''
    for p,c in enumerate(code):
        c = ord(c)
        c = sbox[c]
        c ^= p&0xFF
        c = sbox[c]
        c ^= (p>>8)&0xFF
        c = sbox[c]
        out += chr(c)
    return out

def deobfuscate(sbox, code):
    out = ''
    for p,c in enumerate(code):
        c = ord(c)
        c = sbox[c]
        c ^= (p>>8)&0xFF
        c = sbox[c]
        c ^= p&0xFF
        c = sbox[c]
        out += chr(c)
    return out

END = object()

def dump(value, file):
    if isinstance(value, types.CodeType):
        dump_code(value, file)
    elif type(value) in (list, tuple):
        file.write('[' if type(value) == list else '(')
        file.write(struct.pack('<I', len(value)))
        for x in value:
            dump(x, file)
    elif type(value) == dict:
        file.write('{')
        for k,v in value.items():
            dump(k, file)
            dump(v, file)
        file.write('0')
    else:
        file.write(marshal.dumps(value))

def dump_code(value, file):
    file.write(struct.pack(
        '<cIIII', 'C', value.co_argcount, value.co_nlocals,
                       value.co_stacksize, value.co_flags))

    # Randomize a seed:
    seed, = struct.unpack('<Q', hashlib.sha256(value.co_code + MIRAISALT).digest()[:8])
    file.write(struct.pack('<Q', seed))

    sbox = makeSBox(seed)

    dump(obfuscate(sbox, value.co_code), file)
    dump(value.co_consts, file)
    dump(value.co_names, file)
    dump(value.co_varnames, file)
    dump(value.co_freevars, file)
    dump(value.co_cellvars, file)
    dump(value.co_filename, file)
    dump(value.co_name, file)
    file.write(struct.pack('<I', value.co_firstlineno))
    dump(value.co_lnotab, file)

def dumps(value):
    sio = StringIO()
    dump(value, sio)
    return sio.getvalue()

def load(file):
    mtype = file.read(1)
    if mtype == 'C':
        return load_code(file)
    elif mtype == '[':
        l, = struct.unpack('<I', file.read(4))
        return [load(file) for x in xrange(l)]
    elif mtype == '(':
        l, = struct.unpack('<I', file.read(4))
        return tuple(load(file) for x in xrange(l))
    elif mtype == '{':
        d = {}
        while True:
            k = load(file)
            if k == END: return d
            d[k] = load(file)
    elif mtype == '0':
        return END
    else:
        # Because marshal doesn't accept file-like objects, this inefficient
        # hack is required:
        pos = file.tell()
        obj = marshal.loads(mtype+file.read())
        file.seek(pos-1 + len(marshal.dumps(obj)))
        return obj

def load_code(file):
    argcount, nlocals, stacksize, flags = struct.unpack('<IIII', file.read(16))
    seed, = struct.unpack('<Q', file.read(8))

    sbox = makeSBox(seed)

    code = deobfuscate(sbox, load(file))
    consts = load(file)
    names = load(file)
    varnames = load(file)
    freevars = load(file)
    cellvars = load(file)
    filename = load(file)
    name = load(file)
    firstlineno, = struct.unpack('<I', file.read(4))
    lnotab = load(file)

    return types.CodeType(argcount, nlocals, stacksize, flags, code, consts,
                          names, varnames, filename, name, firstlineno,
                          lnotab, freevars, cellvars) 

def loads(buf):
    return load(StringIO(buf))
