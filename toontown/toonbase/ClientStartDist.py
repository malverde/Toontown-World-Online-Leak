#!/usr/bin/env python2
# This is the "main" module that will start a production copy of
# Toontown Infinite.

# This is a temp patch.
# It should really be done by the runtime (e.g. infinite.exe):
import sys
sys.path = ['.']

# Replace some modules that do exec:
import collections
collections.namedtuple = lambda *x: tuple

# This is included in the package by the prepare_client script. It contains the
# PRC file data, and (stripped) DC file:
import game_data
import __builtin__

# Load all of the packaged PRC config page(s):
from panda3d.core import *
for i, config in enumerate(game_data.CONFIG):
    name = 'GameData config page #' + str(i)
    loadPrcFileData(name, config)

# The VirtualFileSystem, which has already initialized, doesn't see the mount
# directives in the config(s) yet. We have to force it to load them manually:
vfs = VirtualFileSystem.getGlobalPtr()
mounts = ConfigVariableList('vfs-mount')
for mount in mounts:
    mountFile, mountPoint = (mount.split(' ', 2) + [None, None, None])[:2]
    mountFile = Filename(mountFile)
    mountFile.makeAbsolute()
    mountPoint = Filename(mountPoint)
    vfs.mount(mountFile, mountPoint, 0)

# Next, let's get the DC stream:
__builtin__.dcStream = StringStream(game_data.DC)

# Finally, start the game:
import toontown.toonbase.ToontownStart
