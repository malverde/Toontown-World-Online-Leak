#!/usr/bin/env python2
import os
import sys

import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--build-dir', default='build',
                    help='The directory of which the build was prepared.')
parser.add_argument('--output', default='GameData.pyd',
                    help='The built file.')
parser.add_argument('--main-module', default='infinite.base.ClientStart',
                    help='The module to load at the start of the game.')
parser.add_argument('modules', nargs='*', default=['shared', 'infinite'],
                    help='The Toontown Infinite modules to be included in the build.')
args = parser.parse_args()

print 'Building the client...'

os.chdir(args.build_dir)

cmd = sys.executable + ' -m direct.showutil.pfreeze'
args.modules.extend(['direct', 'pandac'])
for module in args.modules:
    cmd += ' -i %s.*.*' % module
cmd += ' -i encodings.*'
cmd += ' -i base64'
cmd += ' -i site'
cmd += ' -o ' + args.output
cmd += ' ' + args.main_module
os.system(cmd)

print 'Done building the client.'
