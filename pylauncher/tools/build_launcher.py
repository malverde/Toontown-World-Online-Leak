#!/usr/bin/python2.7 -OO
# Yes, the above flags matter: We have to do this on 2.7 and we have to optimize.

from modulefinder import ModuleFinder
import os
import sys
import subprocess
import imp
import marshal
import tempfile
import shutil
import atexit
import argparse
import zipfile

# These are to get the dependency walker to find and binarize them, as they would not be found by it normally
EXTRA_MODULES = (
  'encodings.ascii',
  'encodings.latin_1',
  'encodings.hex_codec',
  '_strptime',

  'bz2',
  'httplib',
)

root = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))

class ClientBuilder(object):
    MAINMODULE = 'start'

    def __init__(self, directory):
        self.directory = directory
        self.modules = {}
        self.path_overrides = {}
        self.mf = ModuleFinder(sys.path+[self.directory])

    def should_exclude(self, modname):
        # The NonRepeatableRandomSource modules are imported by the dc file explicitly,
        # so we have to allow them.
        if 'NonRepeatableRandomSource' in modname:
            return False

        if modname.endswith('AI'):
            return True
        if modname.endswith('UD'):
            return True
        if modname.endswith('.ServiceStart'):
            return True

    def find_excludes(self):
        for path, dirs, files in os.walk(self.directory):
            for filename in files:
                filepath = os.path.join(path, filename)
                filepath = os.path.relpath(filepath, self.directory)
                if not filepath.endswith('.py'): continue
                filepath = filepath[:-3]
                modname = filepath.replace(os.path.sep, '.')
                if modname.endswith('.__init__'): modname = modname[:-9]
                if self.should_exclude(modname):
                    self.mf.excludes.append(modname)

    def build_modules(self):
        for modname, mod in self.mf.modules.items():
            if modname in self.path_overrides:
                modfile = self.path_overrides[modname]
            else:
                modfile = mod.__file__
            if not (modfile and modfile.endswith('.py')): continue
            is_package = modfile.endswith('__init__.py')
            with open(modfile, 'r') as f:
                code = compile(f.read(), modname, 'exec')
            self.modules[modname] = (is_package, code)

    def load_modules(self):
        self.find_excludes()

        self.mf.import_hook(self.MAINMODULE)

        for module in EXTRA_MODULES:
            self.mf.import_hook(module)

        self.modules['__main__'] = (False, compile('import %s' % self.MAINMODULE,
                                                   '__main__', 'exec'))
        self.build_modules()


    def write_zip(self, outfile):
        zip = zipfile.ZipFile(outfile, 'w')
        for modname, (is_package, code) in self.modules.items():
            mcode = imp.get_magic() + '\x00'*4 + marshal.dumps(code)
            name = modname.replace('.','/')
            if is_package:
                name += '/__init__'
            name += '.pyo'
            zip.writestr(name, mcode)
        zip.close()

    def write_list(self, outfile):
        with open(outfile,'w') as out:
            for modname in sorted(self.modules.keys()):
                is_package, code = self.modules[modname]
                out.write('%s%s\n' % (modname, ' [PKG]' if is_package else ''))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--mirai-path', help='The path to the Mirai repository root.')
    parser.add_argument('--format', default='mirai', choices=['mirai', 'zip', 'list'],
                        help='The output format to produce. Choices are:\n'
                        'mirai -- a Mirai package\n'
                        'zip -- a zip file of pyos\n'
                        'list -- a plaintext list of included modules')
    parser.add_argument('output', help='The filename of the built file to output.')

    args = parser.parse_args()
    if args.mirai_path:
        sys.path.append(args.mirai_path)
        p3d_path = os.path.join(args.mirai_path, 'panda3d-1.8.1')
        sys.path.insert(0, p3d_path)

    cb = ClientBuilder(root)
    cb.load_modules()

    if args.format == 'zip':
        cb.write_zip(args.output)
    elif args.format == 'list':
        cb.write_list(args.output)
    elif args.format == 'mirai':
        try:
            from mirai.packager import MiraiPackager
        except ImportError:
            sys.stderr.write('Could not import Mirai! Check your --mirai-path\n')
            sys.exit(1)

        mp = MiraiPackager(args.output)
        mp.write_modules(cb.modules)
        mp.close()
