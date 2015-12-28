import ShtikerPage
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from toontown.toonbase import TTLocalizer
from toontown.toonbase import ToontownGlobals

from toontown.achievements import AchievementsGlobals

class AchievementsPage(ShtikerPage.ShtikerPage):

    def __init__(self):
        ShtikerPage.ShtikerPage.__init__(self)
        self.avatar = None
        self.achievements = []

        self.gui = loader.loadModel('phase_3.5/models/gui/friendslist_gui')
        self.accept(localAvatar.uniqueName('achievementsChange'), self.updatePage)

    def load(self):
        ShtikerPage.ShtikerPage.load(self)
        self.avAchievements = localAvatar.achievements
        self.title = DirectLabel(parent=self, relief=None, text=TTLocalizer.AchievementsPageTitle, text_scale=0.12, textMayChange=1, pos=(0, 0, 0.62))

        start_pos = LVecBase3(0.72, 1, -0.21)
        seperation = LVecBase3(0.45, 0, 0.4)

        cardModel = loader.loadModel('phase_3.5/models/gui/playingCard')

        incButton = (self.gui.find('**/FndsLst_ScrollUp'),
                     self.gui.find('**/FndsLst_ScrollDN'),
                     self.gui.find('**/FndsLst_ScrollUp_Rllvr'),
                     self.gui.find('**/FndsLst_ScrollUp'))

        self.scrollFrame = DirectScrolledFrame(parent=self, frameSize=(0, 1.5, -1.2, 0), pos=(-0.75, 1, 0.52),
                                               canvasSize=(0, 1, -7, 0), frameColor=(0.85, 0.95, 1, 1))
        for achievement in xrange(len(AchievementsGlobals.AchievementTitles)):
            achievementFrame = DirectFrame(parent=self.scrollFrame.getCanvas(), image=DGG.getDefaultDialogGeom(), scale=(1.3, 0, 0.32),
                                           relief=None, pos=(start_pos.x, 1, start_pos.z - seperation.z * achievement),
                                           text=AchievementsGlobals.AchievementTitles[achievement], text_scale=(0.05, 0.13),
                                           text_font=ToontownGlobals.getMinnieFont(), text_pos=(0, 0, 0))

            self.achievements.append(achievementFrame)

            if achievement in  self.avAchievements:
                achievementFrame['text'] = AchievementsGlobals.AchievementTitles[achievement]
                achievementFrame['text_pos'] = (0, 0.2, -0.2)
            else:
                achievementFrame['text'] = '???'

    def setAvatar(self, av):
        self.avatar = av

    def updatePage(self):
        print 'updating achievements page'
        self.avAchievements = localAvatar.achievements

        for achievement in self.achievements:
            achievement.destroy()

        del self.achievements
        self.achievements = []

        start_pos = LVecBase3(0.72, 1, -0.21)
        seperation = LVecBase3(0.45, 0, 0.4)

        for achievement in xrange(len(AchievementsGlobals.AchievementTitles)):
            achievementFrame = DirectFrame(parent=self.scrollFrame.getCanvas(), image=DGG.getDefaultDialogGeom(), scale=(1.3, 0, 0.32),
                                           relief=None, pos=(start_pos.x, 1, start_pos.z - seperation.z * achievement),
                                           text=AchievementsGlobals.AchievementTitles[achievement], text_scale=(0.05, 0.13),
                                           text_font=ToontownGlobals.getMinnieFont(), text_pos=(0, 0, 0))

            self.achievements.append(achievementFrame)

            if achievement in  self.avAchievements:
                achievementFrame['text'] = AchievementsGlobals.AchievementTitles[achievement]
                achievementFrame['text_pos'] = (0, 0.2, -0.2)

                currentAchievement = AchievementsGlobals.AchievementImages[achievement]
                image = loader.loadModel(currentAchievement[0])
                imageNode = image.find(currentAchievement[1])
                imageNode.setColor(currentAchievement[2])

                img = OnscreenGeom(geom=imageNode, parent=achievementFrame, pos=(-0.3, 0, 0))
            else:
                achievementFrame['text'] = '???'
