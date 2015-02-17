#!/usr/bin/env python2
import hashlib
import os

import argparse
import xml.etree.ElementTree as ET


parser = argparse.ArgumentParser()
parser.add_argument('--build-dir', default='build',
                    help='The directory of the Toontown Infinite build.')
parser.add_argument('--dest-dir', default='.',
                    help='The directory in which to store the patcher.')
parser.add_argument('--output', default='patcher.xml',
                    help='The name of the output file.')
parser.add_argument('--launcher-version', default='infinite-dev',
                    help='The current version of the Toontown Infinite launcher.')
parser.add_argument('--account-server', default='toontowninfinite.com',
                    help='The address of the Toontown Infinite account server.')
parser.add_argument('--client-agent', default='192.99.200.107',
                    help='The IP address of the Client Agent to connect to.')
parser.add_argument('--server-version', default='infinite-dev',
                    help='The current version of the Toontown Infinite game.')
parser.add_argument('--resources-revision', default='',
                    help='The current revision of the resources repository.')
parser.add_argument('includes', nargs='*', default=['GameData.bin'],
                    help='The files to include in the main directory.')
args = parser.parse_args()


def getFileMD5Hash(filepath):
    md5 = hashlib.md5()
    readBlock = lambda: f.read(128 * md5.block_size)
    with open(filepath, 'rb') as f:
        for chunk in iter(readBlock, b''):
            md5.update(chunk)
    return md5.hexdigest()


def getFileInfo(filepath):
    return (
        os.path.basename(filepath),
        os.path.getsize(filepath),
        getFileMD5Hash(filepath)
    )


rootFiles = []
panda3dFiles = []
for include in args.includes:
    filepath = os.path.join(args.build_dir, include)
    if os.path.dirname(include) == 'panda3d':
        panda3dFiles.append(getFileInfo(filepath))
    else:
        rootFiles.append(getFileInfo(filepath))
    print 'Including...', include

resourcesFiles = []
resourcesDir = os.path.join(args.build_dir, 'resources')
for filename in os.listdir(resourcesDir):
    if not filename.startswith('phase_'):
        continue
    if not filename.endswith('.mf'):
        continue
    filepath = os.path.join(resourcesDir, filename)
    resourcesFiles.append(getFileInfo(filepath))
    print 'Including...', filename

print 'Writing %s...' % args.output

# First, add the element:
patcher = ET.Element('patcher')

# Next, add the Toontown Infinite launcher version:
launcher_version = ET.SubElement(patcher, 'launcher-version')
launcher_version.text = args.launcher_version

# Then add the account server address:
account_server = ET.SubElement(patcher, 'account-server')
account_server.text = args.account_server

# Then add the Client Agent IP:
client_agent = ET.SubElement(patcher, 'client-agent')
client_agent.text = args.client_agent

# Next, add the server version:
server_version = ET.SubElement(patcher, 'server-version')
server_version.text = args.server_version

# Next, add the resources revision:
resources_revision = ET.SubElement(patcher, 'resources-revision')
resources_revision.text = args.resources_revision

# Next, add the root directory:
root = ET.SubElement(patcher, 'directory')
root.set('name', '')

# Add all of the root files:
for filename, size, hash in rootFiles:
    _filename = ET.SubElement(root, 'file')
    _filename.set('name', filename)
    _size = ET.SubElement(_filename, 'size')
    _size.text = str(size)
    _hash = ET.SubElement(_filename, 'hash')
    _hash.text = str(hash)

# Next, add the panda3d directory:
panda3dRoot = ET.SubElement(patcher, 'directory')
panda3dRoot.set('name', 'panda3d')

# Add all of the panda3d files:
for filename, size, hash in panda3dFiles:
    _filename = ET.SubElement(panda3dRoot, 'file')
    _filename.set('name', filename)
    _size = ET.SubElement(_filename, 'size')
    _size.text = str(size)
    _hash = ET.SubElement(_filename, 'hash')
    _hash.text = str(hash)

# Next, add the resources directory:
resourcesRoot = ET.SubElement(patcher, 'directory')
resourcesRoot.set('name', 'resources')

# Add all of the resources files:
for filename, size, hash in resourcesFiles:
    _filename = ET.SubElement(resourcesRoot, 'file')
    _filename.set('name', filename)
    _size = ET.SubElement(_filename, 'size')
    _size.text = str(size)
    _hash = ET.SubElement(_filename, 'hash')
    _hash.text = str(hash)

# Finally, write the patcher.xml file:
filepath = os.path.join(args.dest_dir, args.output)
ET.ElementTree(patcher).write(filepath)

print 'Done writing %s.' % args.output
