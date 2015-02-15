########################## THE TOON LAND PROJECT ##########################
# Filename: FFTownLoader.py
# Created by: Cody/Fd Green Cat Fd (January 31st, 2013)
####
# Description:
#
# The Funny Farm town loader module. This handles the streets as well.
####

from direct.task.Task import Task
from toontown.town import TownLoader
from toontown.suit import Suit

class FFTownLoader(TownLoader.TownLoader):

    def __loadPythonImplementation(self, task):
        if render.find('**/town_top_level') and (base.localAvatar.getZoneId() in (19101, 19105)):
            execfile('%s\\toonland\\playground\\funnyfarm\\_BarkingBoulevard.py' % __filebase__)
            base.localAvatar.d_setParent('x\x8c6\xdd\xb6\x80')
            return Task.done
        taskMgr.doMethodLater(0.2, self._FFTownLoader__loadPythonImplementation, 'FF-LPI')

    def __init__(self, hood, parentFSM, doneEvent):
        TownLoader.TownLoader.__init__(self, hood, parentFSM, doneEvent)
        self.streetClass = FFStreet.FFStreet
        filepath = '%s/toonland/playground/funnyfarm/bgm' % __filebase__
        self.musicFile = '%s/FF_SZ.mp3' % filepath
        self.activityMusicFile = '%s/FF_SZ_activity.mp3' % filepath
        filepath = '%s/toonland/playground/funnyfarm/dna' % __filebase__
        self.townStorageDNAFile = '%s/storage_FF_town.dna' % filepath

    def load(self, zoneId):
        TownLoader.TownLoader.load(self, zoneId)
        Suit.loadSuits(1)
        filepath = '%s/toonland/playground/funnyfarm/dna' % __filebase__
        dnaFile = ('%s/funny_farm_' % filepath) + str(self.canonicalBranchZone) + '.dna'
        self.createHood(dnaFile)
        taskMgr.doMethodLater(0.2, self._FFTownLoader__loadPythonImplementation, 'FF-LPI')

    def unload(self):
        Suit.unloadSuits(1)
        TownLoader.TownLoader.unload(self)