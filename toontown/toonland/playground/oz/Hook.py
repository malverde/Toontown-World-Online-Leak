########################## THE TOON LAND PROJECT ##########################
# Filename: Hook.py
# Created by: Cody/Fd Green Cat Fd (February 4th, 2013)
####
# Description:
#
# Creates hooks in the Outdoor Zone modules to use our modified DNA files.
####

from toontown.shtiker import MapPage
from toontown.safezone import OZSafeZoneLoader
from toontown.hood import OZHood
from direct.task.Task import Task

def _OZSafeZoneLoader__loadPythonImplementation(task):
    if render.find('**/%d:safe_zone' % PlaygroundGlobals.OUTDOOR_ZONE):
        execfile('%s\\toonland\\playground\\oz\\_OutdoorZone.py' % __filebase__)
        base.localAvatar.d_setParent('x\x8c6\xdd\xb6\x80')
        return Task.done
    taskMgr.doMethodLater(0.2, _OZSafeZoneLoader__loadPythonImplementation, 'OZ-LPI')

_Hook = OZSafeZoneLoader.OZSafeZoneLoader.__init__

def __init__(self, hood, parentFSM, doneEvent):
    returnCode = _Hook(self, hood, parentFSM, doneEvent)
    filepath = '%s/toonland/playground/oz/dna' % __filebase__
    self.dnaFile = '%s/outdoor_zone_sz.dna' % filepath
    self.safeZoneStorageDNAFile = '%s/storage_OZ_sz.dna' % filepath
    return returnCode

OZSafeZoneLoader.OZSafeZoneLoader.__init__ = __init__
_load = OZSafeZoneLoader.OZSafeZoneLoader.load

def load(self):
    returnCode = _load(self)
    taskMgr.doMethodLater(0.2, _OZSafeZoneLoader__loadPythonImplementation, 'FF-LPI')
    return returnCode

OZSafeZoneLoader.OZSafeZoneLoader.load = load
__Hook = OZHood.OZHood.__init__

def __init__(self, parentFSM, doneEvent, dnaStore, hoodId):
    returnCode = __Hook(self, parentFSM, doneEvent, dnaStore, hoodId)
    self.townLoaderClass = OZTownLoader.OZTownLoader
    return returnCode

OZHood.OZHood.__init__ = __init__
_enter = MapPage.MapPage.enter

def enter(self):
    returnCode = _enter(self)
    if base.localAvatar.getZoneId() == 6101:
        self.hoodLabel['text'] = 'You are in: Chip \'n Dale\'s Acorn Acres Nutty Place'
    return returnCode

MapPage.MapPage.enter = enter