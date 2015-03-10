from direct.task.Task import Task
import random

from toontown.classicchars import CCharPaths
from toontown.safezone import Playground
from toontown.toonbase import TTLocalizer


class BRPlayground(Playground.Playground):
    def enter(self, requestStatus):
        Playground.Playground.enter(self, requestStatus)
        taskMgr.doMethodLater(1, self.__windTask, 'BR-wind')

    def exit(self):
        Playground.Playground.exit(self)
        taskMgr.remove('BR-wind')

    def showPaths(self):
        self.showPathPoints(CCharPaths.getPaths(TTLocalizer.Pluto))

    def __windTask(self, task):
        base.playSfx(random.choice(self.loader.windSound))
        time = random.random() * 8.0 + 1
        taskMgr.doMethodLater(time, self.__windTask, 'BR-wind')
        return Task.done