from toontown.safezone.TTSafeZoneLoader import TTSafeZoneLoader
from toontown.town.TTTownLoader import TTTownLoader
from toontown.toonbase import ToontownGlobals
from toontown.hood.ToonHood import ToonHood

from otp.ai.MagicWordGlobal import *


class TTHood(ToonHood):
    notify = directNotify.newCategory('TTHood')

    ID = ToontownGlobals.ToontownCentral
    TOWNLOADER_CLASS = TTTownLoader
    SAFEZONELOADER_CLASS = TTSafeZoneLoader
    STORAGE_DNA = 'phase_4/dna/storage_TT.pdna'
    SKY_FILE = 'phase_3.5/models/props/TT_sky'
    SPOOKY_SKY_FILE = 'phase_3.5/models/props/BR_sky'
    TITLE_COLOR = (1.0, 0.5, 0.4, 1.0)
    loader = TTTownLoader
    self.loader = TTTownLoader

    HOLIDAY_DNA = {
      ToontownGlobals.WINTER_DECORATIONS: ['phase_4/dna/winter_storage_TT.pdna', 'phase_4/dna/winter_storage_TT_sz.pdna'],
      ToontownGlobals.WACKY_WINTER_DECORATIONS: ['phase_4/dna/winter_storage_TT.pdna', 'phase_4/dna/winter_storage_TT_sz.pdna'],
      ToontownGlobals.HALLOWEEN_PROPS: ['phase_4/dna/halloween_props_storage_TT.pdna', 'phase_4/dna/halloween_props_storage_TT_sz.pdna'],
      ToontownGlobals.SPOOKY_PROPS: ['phase_4/dna/halloween_props_storage_TT.pdna', 'phase_4/dna/halloween_props_storage_TT_sz.pdna']}


