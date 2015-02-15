########################## THE TOON LAND PROJECT ##########################
# Filename: FFHood.py
# Created by: Cody/Fd Green Cat Fd (January 31st, 2013)
####
# Description:
#
# The Funny Farm neighborhood module.
####

from pandac.PandaModules import *
from toontown.hood import ToonHood
from toontown.hood import SkyUtil

WINTER_DECORATIONS = 4
HALLOWEEN_PROPS = 26

class FFHood(ToonHood.ToonHood):

    notify = directNotify.newCategory('FFHood')

    def __init__(self, parentFSM, doneEvent, dnaStore, hoodId):
        ToonHood.ToonHood.__init__(self, parentFSM, doneEvent, dnaStore, hoodId)
        self.id = PlaygroundGlobals.FUNNY_FARM
        self.townLoaderClass = FFTownLoader.FFTownLoader
        self.safeZoneLoaderClass = FFSafeZoneLoader.FFSafeZoneLoader
        filepath = '%s/toonland/playground/funnyfarm/dna' % __filebase__
        self.storageDNAFile = '%s/storage_FF.dna' % filepath
        self.holidayStorageDNADict = {WINTER_DECORATIONS: ['%s/winter_storage_FF.dna' % filepath,
                                                           '%s/winter_storage_FF_sz.dna' % filepath],
                                      HALLOWEEN_PROPS: ['%s/halloween_props_storage_FF.dna' % filepath,
                                                        '%s/halloween_props_storage_FF_sz.dna' % filepath]}
        self.skyFile = 'phase_3.5/models/props/TT_sky'
        self.spookySkyFile = 'phase_3.5/models/props/BR_sky'
        self.titleColor = (0.55, 1.0, 0.55, 1.0)

    def load(self):
        ToonHood.ToonHood.load(self)
        self.parentFSM.getStateNamed('FFHood').addChild(self.fsm)

    def unload(self):
        self.parentFSM.getStateNamed('FFHood').removeChild(self.fsm)
        ToonHood.ToonHood.unload(self)

    def skyTrack(self, task):
        return SkyUtil.cloudSkyTrack(task)

    def startSky(self):
        self.sky.setTransparency(TransparencyAttrib.MDual, 1)
        self.sky.setScale(1.2)
        base.camLens.setFar(1024)
        self.notify.debug('The sky is: %s' % self.sky)
        if not self.sky.getTag('sky') == 'Regular':
            self.endSpookySky()
        SkyUtil.startCloudSky(self)

    def startSpookySky(self):
        if hasattr(self, 'sky') and self.sky:
            self.stopSky()
        self.sky = loader.loadModel(self.spookySkyFile)
        self.sky.setTag('sky', 'Halloween')
        self.sky.setScale(1.2)
        base.camLens.setFar(1024)
        self.sky.setDepthTest(0)
        self.sky.setDepthWrite(0)
        self.sky.setColor(0.5, 0.5, 0.5, 1)
        self.sky.setBin('background', 100)
        self.sky.setFogOff()
        self.sky.reparentTo(camera)
        self.sky.setTransparency(TransparencyAttrib.MDual, 1)
        fadeIn = self.sky.colorScaleInterval(1.5, Vec4(1, 1, 1, 1),
         startColorScale=Vec4(1, 1, 1, 0.25), blendType='easeInOut')
        fadeIn.start()
        self.sky.setZ(0.0)
        self.sky.setHpr(0.0, 0.0, 0.0)
        ce = CompassEffect.make(NodePath(), (CompassEffect.PRot|CompassEffect.PZ))
        self.sky.node().setEffect(ce)

    def enter(self, *args):
        ToonHood.ToonHood.enter(self, *args)

    def exit(self):
        ToonHood.ToonHood.exit(self)