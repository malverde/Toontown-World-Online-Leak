from toontown.safezone.BRSafeZoneLoader import BRSafeZoneLoader
from toontown.town.BRTownLoader import BRTownLoader
from toontown.toonbase import ToontownGlobals
from toontown.hood.ToonHood import ToonHood


class BRHood(ToonHood):
    notify = directNotify.newCategory('BRHood')

    ID = ToontownGlobals.TheBrrrgh
    TOWNLOADER_CLASS = BRTownLoader
    SAFEZONELOADER_CLASS = BRSafeZoneLoader
    STORAGE_DNA = 'phase_8/dna/storage_BR.pdna'
    SKY_FILE = 'phase_3.5/models/props/BR_sky'
    SPOOKY_SKY_FILE = 'phase_3.5/models/props/BR_sky'
    TITLE_COLOR = (0.3, 0.6, 1.0, 1.0)

    HOLIDAY_DNA = {
      ToontownGlobals.WINTER_DECORATIONS: ['phase_8/dna/winter_storage_BR.pdna'],
      ToontownGlobals.WACKY_WINTER_DECORATIONS: ['phase_8/dna/winter_storage_BR.pdna'],
      ToontownGlobals.HALLOWEEN_PROPS: ['phase_8/dna/halloween_props_storage_BR.pdna'],
      ToontownGlobals.SPOOKY_PROPS: ['phase_8/dna/halloween_props_storage_BR.pdna']}
