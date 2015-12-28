from toontown.achievements import AchievementsGlobals
from direct.interval.IntervalGlobal import *
from direct.interval.LerpInterval import *
from toontown.toonbase import ToontownGlobals
from direct.gui.DirectGui import *
from pandac.PandaModules import *

class AchievementGui():

    def __init__(self):
        self.queue = []
        self.currentShowingAward = 0

    def earnAchievement(self, achievementId):
        if self.queue == []:
            applause = loader.loadSfx('phase_6/audio/sfx/KART_Applause_2.ogg')
            applause.play()

            self.queue.append(achievementId)
            self.showAchievement()
        else:
            self.queue.append(achievementId)

    def showAchievement(self):
        if self.queue != []:
            if self.currentShowingAward == 0:
                self.currentShowingAward = self.queue[0]
                self.displayAchievement()
                self.frameSequence()

    def displayAchievement(self):
        currentAchievement = AchievementsGlobals.AchievementImages[self.currentShowingAward]
        image = loader.loadModel(currentAchievement[0])
        imageNode = image.find(currentAchievement[1])
        imageNode.setColor(currentAchievement[2])
        imageNode.setScale(currentAchievement[3])

        self.frame = OnscreenGeom(geom='phase_3/models/gui/dialog_box_gui', scale=(0.8, 1, 0.55), parent=base.a2dTopRight,
                                  pos=(0.45, 0, -0.275))

        self.image = OnscreenGeom(geom=imageNode, parent=self.frame)

        self.title = OnscreenText(text='You earned an Achievement!', scale=(0.06, 0.11), font=ToontownGlobals.getMinnieFont(),
                                  parent=self.frame, pos=(0, 0.33), align=TextNode.ACenter)

        self.achievementName = OnscreenText(text=AchievementsGlobals.AchievementTitles[self.currentShowingAward], scale=(0.06, 0.09),
                                            font=ToontownGlobals.getMinnieFont(), parent=self.frame, align=TextNode.ACenter, pos=(0, 0.2))

        self.details = OnscreenText(text=AchievementsGlobals.AchievementDesc[self.currentShowingAward], scale=(0.04, 0.07),
                                    font=ToontownGlobals.getMinnieFont(), parent=self.frame, align=TextNode.ACenter, pos=(0, -0.4))

    def frameSequence(self):
        self.seq = Sequence()
        self.seq.append(LerpPosInterval(self.frame, 1, (-0.45, 0, -0.275)))
        self.seq.append(Wait(2))
        self.seq.append(LerpPosInterval(self.frame, 1, (0.45, 0, -0.275)))
        self.seq.append(Func(self.cleanupCurrentFrame))

        self.seq.start()

    def cleanupCurrentFrame(self):
        self.frame.destroy()
        del self.frame

        self.title.destroy()
        del self.title

        self.achievementName.destroy()
        del self.achievementName

        self.details.destroy()
        del self.details

        del self.queue[0]
        self.currentShowingAward = 0
        self.showAchievement()
