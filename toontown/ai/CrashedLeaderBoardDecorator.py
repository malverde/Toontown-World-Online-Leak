<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> parent of 4ac8727... fixed credits and added zander and zander's picture he took
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
import HolidayDecorator
from toontown.toonbase import ToontownGlobals
from pandac.PandaModules import Vec4, TransformState, NodePath, TransparencyAttrib
from toontown.hood import GSHood

class CrashedLeaderBoardDecorator(HolidayDecorator.HolidayDecorator):
    notify = DirectNotifyGlobal.directNotify.newCategory('CrashedLeaderBoardDecorator')

    def __init__(self):
        HolidayDecorator.HolidayDecorator.__init__(self)

    def decorate(self):
        self.updateHoodDNAStore()
        self.swapIval = self.getSwapVisibleIval()
        if self.swapIval:
            self.swapIval.start()
        holidayIds = base.cr.newsManager.getDecorationHolidayId()
        if ToontownGlobals.CRASHED_LEADERBOARD not in holidayIds:
            return
        if config.GetBool('want-crashedLeaderBoard-Smoke', 1):
            self.startSmokeEffect()

    def startSmokeEffect(self):
        if isinstance(base.cr.playGame.getPlace().loader.hood, GSHood.GSHood):
            base.cr.playGame.getPlace().loader.startSmokeEffect()

    def stopSmokeEffect(self):
        if isinstance(base.cr.playGame.getPlace().loader.hood, GSHood.GSHood):
            base.cr.playGame.getPlace().loader.stopSmokeEffect()

    def undecorate(self):
        if config.GetBool('want-crashedLeaderBoard-Smoke', 1):
            self.stopSmokeEffect()
        holidayIds = base.cr.newsManager.getDecorationHolidayId()
        if len(holidayIds) > 0:
            self.decorate()
            return
        storageFile = base.cr.playGame.hood.storageDNAFile
        if storageFile:
            pass # TODO: DNATODO
            #loadDNAFile(self.dnaStore, storageFile, CSDefault)
        self.swapIval = self.getSwapVisibleIval()
        if self.swapIval:
            self.swapIval.start()
<<<<<<< HEAD
=======
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
import HolidayDecorator
from toontown.toonbase import ToontownGlobals
from pandac.PandaModules import Vec4, TransformState, NodePath, TransparencyAttrib
from toontown.hood import GSHood

class CrashedLeaderBoardDecorator(HolidayDecorator.HolidayDecorator):
    notify = DirectNotifyGlobal.directNotify.newCategory('CrashedLeaderBoardDecorator')

    def __init__(self):
        HolidayDecorator.HolidayDecorator.__init__(self)

    def decorate(self):
        self.updateHoodDNAStore()
        self.swapIval = self.getSwapVisibleIval()
        if self.swapIval:
            self.swapIval.start()
        holidayIds = base.cr.newsManager.getDecorationHolidayId()
        if ToontownGlobals.CRASHED_LEADERBOARD not in holidayIds:
            return
        if config.GetBool('want-crashedLeaderBoard-Smoke', 1):
            self.startSmokeEffect()

    def startSmokeEffect(self):
        if isinstance(base.cr.playGame.getPlace().loader.hood, GSHood.GSHood):
            base.cr.playGame.getPlace().loader.startSmokeEffect()

    def stopSmokeEffect(self):
        if isinstance(base.cr.playGame.getPlace().loader.hood, GSHood.GSHood):
            base.cr.playGame.getPlace().loader.stopSmokeEffect()

    def undecorate(self):
        if config.GetBool('want-crashedLeaderBoard-Smoke', 1):
            self.stopSmokeEffect()
        holidayIds = base.cr.newsManager.getDecorationHolidayId()
        if len(holidayIds) > 0:
            self.decorate()
            return
        storageFile = base.cr.playGame.hood.storageDNAFile
        if storageFile:
            pass # TODO: DNATODO
            #loadDNAFile(self.dnaStore, storageFile, CSDefault)
        self.swapIval = self.getSwapVisibleIval()
        if self.swapIval:
            self.swapIval.start()
>>>>>>> 30847815294dd00139dc93e7849d6bffd935eca9
=======
>>>>>>> parent of 4ac8727... fixed credits and added zander and zander's picture he took
