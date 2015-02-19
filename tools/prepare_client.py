#!/usr/bin/env python2
import argparse
import hashlib
import os
from pandac.PandaModules import *
import shutil


parser = argparse.ArgumentParser()
parser.add_argument('--distribution', default='en',
                    help='The distribution string.')
parser.add_argument('--build-dir', default='build',
                    help='The directory in which to store the build files.')
parser.add_argument('--src-dir', default='..',
                    help='The directory of the Toontown Infinite source code.')
parser.add_argument('--server-ver', default='infinite-dev',
                    help='The server version of this build.')
parser.add_argument('--build-mfs', action='store_true',
                    help='When present, the resource multifiles will be built.')
parser.add_argument('--resources-dir', default='../resources',
                    help='The directory of the Toontown Infinite resources.')
parser.add_argument('--config-dir', default='../config/release',
                    help='The directory of the Toontown Infinite configuration files.')
parser.add_argument('--include', '-i', action='append',
                    help='Explicitly include this file in the build.')
parser.add_argument('--exclude', '-x', action='append',
                    help='Explicitly exclude this file from the build.')
parser.add_argument('--vfs', action='append',
                    help='Add this file to the virtual file system at runtime.')
parser.add_argument('modules', nargs='*', default=['otp', 'toontown'],
                    help='The Toontown Infinite modules to be included in the build.')
args = parser.parse_args()

print 'Preparing the client...'

# Create a clean directory to store the build files in:
if os.path.exists(args.build_dir):
    shutil.rmtree(args.build_dir)
os.mkdir(args.build_dir)
print 'Build directory = ' + args.build_dir

# Copy the provided Toontown Infinite modules:


def minify(f):
    """
    Returns the "minified" file data with removed __debug__ code blocks.
    """

    data = ''

    debugBlock = False  # Marks when we're in a __debug__ code block.
    elseBlock = False  # Marks when we're in an else code block.

    # The number of spaces in which the __debug__ condition is indented:
    indentLevel = 0

    for line in f:
        thisIndentLevel = len(line) - len(line.lstrip())
        if ('if __debug__:' not in line) and (not debugBlock):
            data += line
            continue
        elif 'if __debug__:' in line:
            debugBlock = True
            indentLevel = thisIndentLevel
            continue
        if thisIndentLevel <= indentLevel:
            if 'else' in line:
                elseBlock = True
                continue
            if 'elif' in line:
                line = line[:thisIndentLevel] + line[thisIndentLevel+2:]
            data += line
            debugBlock = False
            elseBlock = False
            indentLevel = 0
            continue
        if elseBlock:
            data += line[4:]

    return data


for module in args.modules:
    print 'Writing module...', module
    for root, folders, files in os.walk(os.path.join(args.src_dir, module)):
        outputDir = root.replace(args.src_dir, args.build_dir)
        if not os.path.exists(outputDir):
            os.mkdir(outputDir)
        for filename in files:
            if filename not in args.include:
                if not filename.endswith('.py'):
                    continue
                if filename.endswith('UD.py'):
                    continue
                if filename.endswith('AI.py'):
                    continue
                if filename in args.exclude:
                    continue
            with open(os.path.join(root, filename), 'r') as f:
                data = minify(f)
            with open(os.path.join(outputDir, filename), 'w') as f:
                f.write(data)

# Let's write game_data.py now. game_data.py is a compile-time generated
# collection of data that will be used by the game at runtime. It contains the
# PRC file data, and (stripped) DC file:

# First, we need to add the configuration pages:
configData = []
with open('../config/general.prc') as f:
    configData.append(f.read())

configFileName = args.distribution + '.prc'
configFilePath = os.path.join(args.config_dir, configFileName)
print 'Using configuration file: ' + configFilePath

with open(configFilePath) as f:
    data = f.readlines()

    # Replace server-version definitions with the desired server version:
    for i, line in enumerate(data):
        if 'server-version' in line:
            data[i] = 'server-version ' + args.server_ver

    # Add our virtual file system data:
    data.append('\n# Virtual file system...\nmodel-path /\n')
    for filepath in args.vfs:
        data.append('vfs-mount %s /\n' % filepath)

    configData.append('\n'.join(data))

# Next, we need the DC file:
dcData = ''
filepath = os.path.join(args.src_dir, 'astron/dclass')
for filename in os.listdir(filepath):
    if filename.endswith('.dc'):
        fullpath = str(Filename.fromOsSpecific(os.path.join(filepath, filename)))
        print 'Reading %s...' % fullpath
        with open(fullpath, 'r') as f:
            data = f.read()
            for line in data.split('\n'):
                if 'import' in line:
                    data = data.replace(line + '\n', '')
            dcData += data

# Finally, write our data to game_data.py:
print 'Writing game_data.py...'
gameData = 'CONFIG = %r\nDC = %r\n'
with open(os.path.join(args.build_dir, 'game_data.py'), 'wb') as f:
    f.write(gameData % (configData, dcData.strip()))

# We have all of the code gathered together. Let's create the multifiles now:
if args.build_mfs:
    print 'Building multifiles...'
    dest = os.path.join(args.build_dir, 'resources')
    if not os.path.exists(dest):
        os.mkdir(dest)
    dest = os.path.realpath(dest)
    os.chdir(args.resources_dir)
    for phase in os.listdir('.'):
        if not phase.startswith('phase_'):
            continue
        if not os.path.isdir(phase):
            continue
        filename = phase + '.mf'
        print 'Writing...', filename
        filepath = os.path.join(dest, filename)
        os.system('multify -c -f "%s" "%s"' % (filepath, phase))

print 'Done preparing the client.'
