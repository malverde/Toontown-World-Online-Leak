from toontown.town.TutorialTownLoader import TutorialTownLoader
from toontown.toonbase import ToontownGlobals
from toontown.hood.ToonHood import ToonHood


class TutorialHood(ToonHood):
    notify = directNotify.newCategory('TutorialHood')

    ID = ToontownGlobals.Tutorial
    TOWNLOADER_CLASS = TutorialTownLoader
    SKY_FILE = 'phase_3.5/models/props/TT_sky'
    TITLE_COLOR = (1.0, 0.5, 0.4, 1.0)
