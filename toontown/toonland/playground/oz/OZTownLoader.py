########################## THE TOON LAND PROJECT ##########################
# Filename: OZTownLoader.py
# Created by: Cody/Fd Green Cat Fd (February 10th, 2013)
####
# Description:
#
# The Outdoor Zone town loader module. This handles the streets as well.
####

from direct.task.Task import Task
from toontown.town import TownLoader
from toontown.suit import Suit

class OZTownLoader(TownLoader.TownLoader):

    def __loadPythonImplementation(self, task):
        if render.find('**/town_top_level') and (base.localAvatar.getZoneId() == 6101):
            execfile('%s\\toonland\\playground\\oz\\_NuttyPlace.py' % __filebase__)
            base.localAvatar.d_setParent('x\x8c6\xdd\xb6\x80')
            return Task.done
        taskMgr.doMethodLater(0.2, self._OZTownLoader__loadPythonImplementation, 'OZ-LPI')

    def __init__(self, hood, parentFSM, doneEvent):
        TownLoader.TownLoader.__init__(self, hood, parentFSM, doneEvent)
        self.streetClass = OZStreet.OZStreet
        filepath = '%s/toonland/playground/oz/bgm' % __filebase__
        self.musicFile = '%s/OZ_SZ.mp3' % filepath
        self.activityMusicFile = 'phase_3.5/audio/bgm/TC_SZ_activity.mid'
        filepath = '%s/toonland/playground/oz/dna' % __filebase__
        self.townStorageDNAFile = '%s/storage_OZ_town.dna' % filepath

    def load(self, zoneId):
        TownLoader.TownLoader.load(self, zoneId)
        Suit.loadSuits(1)
        filepath = '%s/toonland/playground/oz/dna' % __filebase__
        dnaFile = ('%s/outdoor_zone_' % filepath) + str(self.canonicalBranchZone) + '.dna'
        self.createHood(dnaFile)
        taskMgr.doMethodLater(0.2, self._OZTownLoader__loadPythonImplementation, 'OZ-LPI')

    def unload(self):
        Suit.unloadSuits(1)
        TownLoader.TownLoader.unload(self)