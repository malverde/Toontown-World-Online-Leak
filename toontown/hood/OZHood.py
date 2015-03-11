from pandac.PandaModules import Vec4

from toontown.safezone.OZSafeZoneLoader import OZSafeZoneLoader
from toontown.toonbase import ToontownGlobals
from toontown.hood.ToonHood import ToonHood


class OZHood(ToonHood):
    notify = directNotify.newCategory('OZHood')

    ID = ToontownGlobals.OutdoorZone
    SAFEZONELOADER_CLASS = OZSafeZoneLoader
    STORAGE_DNA = 'phase_6/dna/storage_OZ.pdna'
    SKY_FILE = 'phase_3.5/models/props/TT_sky'
    SPOOKY_SKY_FILE = 'phase_3.5/models/props/BR_sky'
    TITLE_COLOR = (1.0, 0.5, 0.4, 1.0)

    def __init__(self, parentFSM, doneEvent, dnaStore, hoodId):
        ToonHood.__init__(self, parentFSM, doneEvent, dnaStore, hoodId)

        # Load content pack ambience settings:
        ambience = contentPacksMgr.getAmbience('outdoor-zone')

        color = ambience.get('underwater-color')
        if color is not None:
            try:
                self.underwaterColor = Vec4(color['r'], color['g'], color['b'], color['a'])
            except Exception, e:
                raise ContentPackError(e)
        elif self.underwaterColor is None:
            self.underwaterColor = Vec4(0, 0, 0.6, 1)

    def load(self):
        ToonHood.load(self)

        self.fog = Fog('OZFog')

    def enter(self, requestStatus):
        ToonHood.enter(self, requestStatus)

        base.camLens.setNearFar(ToontownGlobals.SpeedwayCameraNear, ToontownGlobals.SpeedwayCameraFar)

    def exit(self):
        base.camLens.setNearFar(ToontownGlobals.DefaultCameraNear, ToontownGlobals.DefaultCameraFar)

        ToonHood.exit(self)
