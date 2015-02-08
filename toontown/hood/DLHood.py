from toontown.safezone.DLSafeZoneLoader import DLSafeZoneLoader
from toontown.town.DLTownLoader import DLTownLoader
from toontown.toonbase import ToontownGlobals
from toontown.hood.ToonHood import ToonHood


class DLHood(ToonHood):
    notify = directNotify.newCategory('DLHood')

    ID = ToontownGlobals.DonaldsDreamland
    TOWNLOADER_CLASS = DLTownLoader
    SAFEZONELOADER_CLASS = DLSafeZoneLoader
    STORAGE_DNA = 'phase_8/dna/storage_DL.pdna'
    SKY_FILE = 'phase_8/models/props/DL_sky'
    TITLE_COLOR = (1.0, 0.9, 0.5, 1.0)

    HOLIDAY_DNA = {
      ToontownGlobals.WINTER_DECORATIONS: ['phase_8/dna/winter_storage_DL.pdna'],
      ToontownGlobals.WACKY_WINTER_DECORATIONS: ['phase_8/dna/winter_storage_DL.pdna'],
      ToontownGlobals.HALLOWEEN_PROPS: ['phase_8/dna/halloween_props_storage_DL.pdna'],
      ToontownGlobals.SPOOKY_PROPS: ['phase_8/dna/halloween_props_storage_DL.pdna']}

    def enter(self, requestStatus):
        ToonHood.enter(self, requestStatus)

        base.camLens.setNearFar(ToontownGlobals.DreamlandCameraNear, ToontownGlobals.DreamlandCameraFar)

    def exit(self):
        base.camLens.setNearFar(ToontownGlobals.DefaultCameraNear, ToontownGlobals.DefaultCameraFar)

        ToonHood.exit(self)
