from toontown.safezone.DGSafeZoneLoader import DGSafeZoneLoader
from toontown.town.DGTownLoader import DGTownLoader
from toontown.toonbase import ToontownGlobals
from toontown.hood.ToonHood import ToonHood


class DGHood(ToonHood):
    notify = directNotify.newCategory('DGHood')

    ID = ToontownGlobals.DaisyGardens
    TOWNLOADER_CLASS = DGTownLoader
    SAFEZONELOADER_CLASS = DGSafeZoneLoader
    STORAGE_DNA = 'phase_8/dna/storage_DG.pdna'
    SKY_FILE = 'phase_3.5/models/props/TT_sky'
    SPOOKY_SKY_FILE = 'phase_3.5/models/props/BR_sky'
    TITLE_COLOR = (0.8, 0.6, 1.0, 1.0)

    HOLIDAY_DNA = {
      ToontownGlobals.WINTER_DECORATIONS: ['phase_8/dna/winter_storage_DG.pdna'],
      ToontownGlobals.WACKY_WINTER_DECORATIONS: ['phase_8/dna/winter_storage_DG.pdna'],
      ToontownGlobals.HALLOWEEN_PROPS: ['phase_8/dna/halloween_props_storage_DG.pdna'],
      ToontownGlobals.SPOOKY_PROPS: ['phase_8/dna/halloween_props_storage_DG.pdna']}
