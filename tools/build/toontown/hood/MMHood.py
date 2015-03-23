from toontown.safezone.MMSafeZoneLoader import MMSafeZoneLoader
from toontown.town.MMTownLoader import MMTownLoader
from toontown.toonbase import ToontownGlobals
from toontown.hood.ToonHood import ToonHood


class MMHood(ToonHood):
    notify = directNotify.newCategory('MMHood')

    ID = ToontownGlobals.MinniesMelodyland
    TOWNLOADER_CLASS = MMTownLoader
    SAFEZONELOADER_CLASS = MMSafeZoneLoader
    STORAGE_DNA = 'phase_6/dna/storage_MM.pdna'
    SKY_FILE = 'phase_6/models/props/MM_sky'
    SPOOKY_SKY_FILE = 'phase_6/models/props/MM_sky'
    TITLE_COLOR = (1.0, 0.5, 0.5, 1.0)

    HOLIDAY_DNA = {
      ToontownGlobals.WINTER_DECORATIONS: ['phase_6/dna/winter_storage_MM.pdna'],
      ToontownGlobals.WACKY_WINTER_DECORATIONS: ['phase_6/dna/winter_storage_MM.pdna'],
      ToontownGlobals.HALLOWEEN_PROPS: ['phase_6/dna/halloween_props_storage_MM.pdna'],
      ToontownGlobals.SPOOKY_PROPS: ['phase_6/dna/halloween_props_storage_MM.pdna']}
