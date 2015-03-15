import argparse
import hashlib
import os
import shutil
import subprocess

from pandac.PandaModules import *
import pytz


parser = argparse.ArgumentParser()
parser.add_argument('--build-dir', default='build',
                    help='The directory in which to store the build files.')
parser.add_argument('--src-dir', default='..',
                    help='The directory of the Toontown source code.')
parser.add_argument('--server-ver', default='dev',
                    help='The server version of this build.\n')
parser.add_argument('--build-mfs', action='store_true',
                    help='When present, multifiles will be built.')
parser.add_argument('--resources-dir', default='../resources',
                    help='The directory of the Toontown resources.')
parser.add_argument('modules', nargs='*', default=['otp', 'toontown'],
                    help='The Toontown modules to be included in the build.')
args = parser.parse_args()

print 'Preparing the client...'

# Create a clean build directory for us to store our build material:
if not os.path.exists(args.build_dir):
    os.mkdir(args.build_dir)
print 'Build directory = {0}'.format(args.build_dir)

# Set the build version.
serverVersion = args.server_ver
print 'serverVersion = {0}'.format(serverVersion)

# Copy the provided Toontown modules:

# NonRepeatableRandomSourceUD.py, and NonRepeatableRandomSourceAI.py are
# required to be included. This is because they are explicitly imported by the
# DC file:
includes = ('NonRepeatableRandomSourceUD.py', 'NonRepeatableRandomSourceAI.py')

# This is a list of explicitly excluded files:
excludes = ('ServiceStart.py', 'ToontownUberRepository', 'ToontownAIRepository')

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
            if filename not in includes:
                if not filename.endswith('.py'):
                    continue
                if filename.endswith('UD.py'):
                    continue
                if filename.endswith('AI.py'):
                    continue
                if filename in excludes:
                    continue
            with open(os.path.join(root, filename), 'r') as f:
                data = minify(f)
            with open(os.path.join(outputDir, filename), 'w') as f:
                f.write(data)

# Let's write _miraidata.py now. _miraidata is a compile-time generated
# collection of data that will be used by the game at runtime. It contains the
# PRC file data, (stripped) DC file, and time zone info.

# First, we need the PRC file data:
configFileName = 'public_client.prc'
configData = []
with open(os.path.join(args.src_dir, 'config', configFileName)) as f:
    data = f.read()
    configData.append(data.replace('SERVER_VERSION', serverVersion))
print 'Using config file: {0}'.format(configFileName)

# Next, we need the (stripped) DC file:
dcFile = DCFile()
filepath = os.path.join(args.src_dir, 'astron')
for filename in os.listdir(filepath):
    if filename.endswith('.dc'):
        dcFile.read(Filename.fromOsSpecific(os.path.join(filepath, filename)))
dcStream = StringStream()
dcFile.write(dcStream, True)
dcData = dcStream.getData()

# Now, collect our timezone info:
zoneInfo = {}
for timezone in pytz.all_timezones:
    zoneInfo['zoneinfo/' + timezone] = pytz.open_resource(timezone).read()

# Finally, write our data to _miraidata.py:
print 'Writing _miraidata.py...'
gameData = '''\
CONFIG = %r
DC = %r
ZONEINFO = %r'''
with open(os.path.join(args.build_dir, '_miraidata.py'), 'w') as f:
    f.write(gameData % (configData, dcData, zoneInfo))


def getDirectoryMD5Hash(directory):
    def _updateChecksum(checksum, dirname, filenames):
        for filename in sorted(filenames):
            path = os.path.join(dirname, filename)
            if os.path.isfile(path):
                fh = open(path, 'rb')
                while True:
                    buf = fh.read(4096)
                    if not buf:
                        break
                    checksum.update(buf)
                fh.close()
    checksum = hashlib.md5()
    directory = os.path.normpath(directory)
    if os.path.exists(directory):
        if os.path.isdir(directory):
            os.path.walk(directory, _updateChecksum, checksum)
        elif os.path.isfile(directory):
            _updateChecksum(
                checksum, os.path.dirname(directory),
                os.path.basename(directory))
    return checksum.hexdigest()


# We have all of the code gathered together. Let's create the multifiles now:
if args.build_mfs:
    print 'Building multifiles...'
    dest = os.path.join(args.build_dir, 'resources')
    if not os.path.exists(dest):
        os.mkdir(dest)
    dest = os.path.realpath(dest)
    os.chdir(args.resources_dir)
    if not os.path.exists('local-patcher.ver'):
        with open('local-patcher.ver', 'w') as f:
            f.write('RESOURCES = {}')
    with open('local-patcher.ver', 'r') as f:
        exec(f.read())
    for phase in os.listdir('.'):
        if not phase.startswith('phase_'):
            continue
        if not os.path.isdir(phase):
            continue
        phaseMd5 = getDirectoryMD5Hash(phase)
        if phase in RESOURCES:
            if RESOURCES[phase] == phaseMd5:
                continue
        filename = phase + '.mf'
        print 'Writing...', filename
        filepath = os.path.join(dest, filename)
        os.system('multify -c -f {0} {1}'.format(filepath, phase))
        RESOURCES[phase] = phaseMd5
    with open('local-patcher.ver', 'w') as f:
        f.write('RESOURCES = %r' % RESOURCES)

print 'Done preparing the client.'
