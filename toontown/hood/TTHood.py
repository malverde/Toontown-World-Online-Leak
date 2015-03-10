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

    HOLIDAY_DNA = {
      ToontownGlobals.WINTER_DECORATIONS: ['phase_4/dna/winter_storage_TT.pdna', 'phase_4/dna/winter_storage_TT_sz.pdna'],
      ToontownGlobals.WACKY_WINTER_DECORATIONS: ['phase_4/dna/winter_storage_TT.pdna', 'phase_4/dna/winter_storage_TT_sz.pdna'],
      ToontownGlobals.HALLOWEEN_PROPS: ['phase_4/dna/halloween_props_storage_TT.pdna', 'phase_4/dna/halloween_props_storage_TT_sz.pdna'],
      ToontownGlobals.SPOOKY_PROPS: ['phase_4/dna/halloween_props_storage_TT.pdna', 'phase_4/dna/halloween_props_storage_TT_sz.pdna']}


@magicWord(category=CATEGORY_CREATIVE)
def spooky():
    """
    Activates the 'spooky' effect on the current area.
    """
    hood = base.cr.playGame.hood
    if not hasattr(hood, 'startSpookySky'):
        return "Couldn't find spooky sky."
    if hasattr(hood, 'magicWordSpookyEffect'):
        return 'The spooky effect is already active!'
    hood.magicWordSpookyEffect = True
    hood.startSpookySky()
    fadeOut = base.cr.playGame.getPlace().loader.geom.colorScaleInterval(
        1.5, Vec4(0.55, 0.55, 0.65, 1), startColorScale=Vec4(1, 1, 1, 1),
        blendType='easeInOut')
    fadeOut.start()
    spookySfx = base.loadSfx('phase_4/audio/sfx/spooky.ogg')
    spookySfx.play()
    return 'Activating the spooky effect...'
