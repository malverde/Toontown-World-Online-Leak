from toontown.classicchars import CCharPaths
from toontown.safezone import Playground
from toontown.toonbase import TTLocalizer


class MMPlayground(Playground.Playground):
    def showPaths(self):
        self.showPathPoints(CCharPaths.getPaths(TTLocalizer.Minnie))
