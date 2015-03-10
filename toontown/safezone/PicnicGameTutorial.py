import inspect

from direct.fsm import FSM
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from toontown.toonbase import TTLocalizer
from toontown.toonbase import ToontownGlobals


class GameTutorial(DirectFrame, FSM.FSM):
    def __init__(self, doneFunction, doneEvent=None, callback=None):
        FSM.FSM.__init__(self, 'GameTutorial')

        self.doneFunction = doneFunction
        self.doneEvent = doneEvent
        self.callback = callback

        base.localAvatar.startSleepWatch(self.handleQuit)
        self.accept('stoppedAsleep', self.handleQuit)

        stateArray = []
        pageNum = 1
        for name, _ in inspect.getmembers(self):
            if name.startswith('enterPage'):
                stateArray.append('Page' + str(pageNum))
                pageNum += 1
        stateArray.append('Quit')
        self.setStateArray(stateArray)

        DirectFrame.__init__(
            self, pos=(-0.5, 0, 0),
            image_color=ToontownGlobals.GlobalDialogColor,
            image_scale=(1.0, 1.5, 1.0), text='', text_scale=0.06)
        self['image'] = DGG.getDefaultDialogGeom()

        self.title = DirectLabel(
            self, relief=None, text='', text_pos=(0.0, 0.35),
            text_fg=(1, 0, 0, 1), text_scale=0.13,
            text_font=ToontownGlobals.getSignFont())

        buttons = loader.loadModel('phase_3/models/gui/dialog_box_buttons_gui.bam')
        gui = loader.loadModel('phase_3.5/models/gui/friendslist_gui.bam')

        self.nextButton = DirectButton(
            self, image=(gui.find('**/Horiz_Arrow_UP'),
                         gui.find('**/Horiz_Arrow_DN'),
                         gui.find('**/Horiz_Arrow_Rllvr'),
                         gui.find('**/Horiz_Arrow_UP')),
            image3_color=Vec4(1, 1, 1, 0.5), relief=None,
            text=TTLocalizer.ChineseTutorialNext, text3_fg=Vec4(0, 0, 0, 0.5),
            text_scale=0.05, text_pos=(0.0, -0.1), pos=(0.35, -0.3, -0.33),
            command=self.requestNext)
        self.nextButton.hide()
        self.prevButton = DirectButton(
            self, image=(gui.find('**/Horiz_Arrow_UP'),
                         gui.find('**/Horiz_Arrow_DN'),
                         gui.find('**/Horiz_Arrow_Rllvr'),
                         gui.find('**/Horiz_Arrow_UP')),
            image3_color=Vec4(1, 1, 1, 0.5), image_scale=(-1.0, 1.0, 1.0),
            relief=None, text=TTLocalizer.ChineseTutorialPrev,
            text3_fg=Vec4(0, 0, 0, 0.5), text_scale=0.05, text_pos=(0.0, -0.1),
            pos=(-0.3, -0.3, -0.33), command=self.requestPrev)
        self.prevButton.hide()
        self.quitButton = DirectButton(
            self, image=(buttons.find('**/ChtBx_OKBtn_UP'),
                         buttons.find('**/ChtBx_OKBtn_DN'),
                         buttons.find('**/ChtBx_OKBtn_Rllvr')),
            relief=None, text=TTLocalizer.ChineseTutorialDone, text_scale=0.05,
            text_pos=(0.0, -0.1), pos=(0.35, -0.3, -0.33),
            command=self.handleQuit)
        self.quitButton.hide()

        buttons.removeNode()
        gui.removeNode()

    def __del__(self):
        self.cleanup()

    def enterQuit(self, *args):
        self.nextButton.destroy()
        self.prevButton.destroy()
        self.quitButton.destroy()
        DirectFrame.destroy(self)

    def exitQuit(self, *args):
        pass

    def handleQuit(self, task=None):
        self.forceTransition('Quit')
        base.cr.playGame.getPlace().setState('walk')
        self.doneFunction()
        if task is not None:
            task.done


class CheckersTutorial(GameTutorial):
    def __init__(self, doneFunction):
        GameTutorial.__init__(self, doneFunction)

        images = loader.loadModel('phase_6/models/golf/regularchecker_tutorial.bam')
        images.setTransparency(1)

        self.page1 = images.find('**/tutorialPage1*')
        self.page1.reparentTo(aspect2d)
        self.page1.setPos(0.63, -0.1, 0.0)
        self.page1.setScale(0.4)
        self.page1.setTransparency(1)
        self.page1.hide()

        self.page2 = images.find('**/tutorialPage2*')
        self.page2.reparentTo(aspect2d)
        self.page2.setPos(0.63, -0.1, 0.0)
        self.page2.setScale(0.4)
        self.page2.setTransparency(1)
        self.page2.hide()

        self.page3 = images.find('**/tutorialPage3*')
        self.page3.reparentTo(aspect2d)
        self.page3.setPos(0.63, -0.1, 0.0)
        self.page3.setScale(0.4)
        self.page3.setTransparency(1)
        self.obj = self.page3.find('**/king*')
        self.page3.hide()

        self.page4 = images.find('**/tutorialPage4*')
        self.page4.reparentTo(aspect2d)
        self.page4.setPos(0.63, -0.1, 0.0)
        self.page4.setScale(0.4)
        self.page4.setTransparency(1)
        self.page4.hide()

        self.request('Page1')

    def enterPage1(self, *args):
        self.nextButton.show()
        self.prevButton.hide()
        self.nextButton['state'] = DGG.NORMAL
        self.prevButton['state'] = DGG.DISABLED
        self.title['text'] = (TTLocalizer.ChineseTutorialTitle1,)
        self['text'] = TTLocalizer.CheckersPage1
        self['text_pos'] = (0.0, 0.23)
        self['text_wordwrap'] = 13.5
        self['text_scale'] = 0.06
        self.page1.show()

    def exitPage1(self, *args):
        self.page1.hide()

    def enterPage2(self, *args):
        self.nextButton.show()
        self.prevButton.show()
        self.nextButton['state'] = DGG.NORMAL
        self.prevButton['state'] = DGG.NORMAL
        self.title['text'] = (TTLocalizer.ChineseTutorialTitle2,)
        self['text'] = TTLocalizer.CheckersPage2
        self['text_pos'] = (0.0, 0.28)
        self['text_wordwrap'] = 12.5
        self['text_scale'] = 0.06
        self.page2.show()

    def exitPage2(self, *args):
        self.page2.hide()

    def enterPage3(self, *args):
        self.nextButton.show()
        self.prevButton.show()
        self.nextButton['state'] = DGG.NORMAL
        self.prevButton['state'] = DGG.NORMAL
        self.title['text'] = (TTLocalizer.ChineseTutorialTitle2,)
        self['text'] = TTLocalizer.CheckersPage3
        self.blinker = Sequence(
            LerpColorInterval(self.obj, 0.5, Vec4(0.5, 0.5, 0, 0), Vec4(0.9, 0.9, 0, 1)),
            LerpColorInterval(self.obj, 0.5, Vec4(0.9, 0.9, 0, 1), Vec4(0.5, 0.5, 0, 0))
        )
        self.blinker.loop()
        self.page3.show()

    def exitPage3(self, *args):
        self.blinker.finish()
        self.page3.hide()

    def enterPage4(self, *args):
        self.nextButton.hide()
        self.prevButton.show()
        self.nextButton['state'] = DGG.DISABLED
        self.prevButton['state'] = DGG.NORMAL
        self.title['text'] = (TTLocalizer.ChineseTutorialTitle2,)
        self['text'] = TTLocalizer.CheckersPage4
        self.quitButton.show()
        self.page4.show()

    def exitPage4(self, *args):
        self.quitButton.hide()
        self.page4.hide()


class ChineseCheckersTutorial(GameTutorial):
    def __init__(self, doneFunction, doneEvent=None, callback=None):
        GameTutorial.__init__(self, doneFunction)

        images = loader.loadModel('phase_6/models/golf/checker_tutorial.bam')
        images.setTransparency(1)

        self.page1 = images.find('**/tutorialPage1*')
        self.page1.reparentTo(aspect2d)
        self.page1.setPos(0.63, -0.1, 0.0)
        self.page1.setScale(13.95)
        self.page1.setTransparency(1)
        self.page1.hide()
        self.page1.getChildren()[1].hide()

        self.page2 = images.find('**/tutorialPage3*')
        self.page2.reparentTo(aspect2d)
        self.page2.setPos(0.63, -0.1, 0.5)
        self.page2.setScale(13.95)
        self.page2.setTransparency(1)
        self.page2.hide()

        self.page3 = images.find('**/tutorialPage2*')
        self.page3.reparentTo(aspect2d)
        self.page3.setPos(0.63, -0.1, -0.5)
        self.page3.setScale(13.95)
        self.page3.setTransparency(1)
        self.page3.hide()

        self.request('Page1')

    def enterPage1(self, *args):
        self.nextButton.show()
        self.prevButton.hide()
        self.nextButton['state'] = DGG.NORMAL
        self.prevButton['state'] = DGG.DISABLED
        self.title['text'] = (TTLocalizer.ChineseTutorialTitle1,)
        self['text'] = TTLocalizer.ChinesePage1
        self['text_pos'] = (0.0, 0.23)
        self['text_wordwrap'] = 13.5
        obj = self.page1.getChildren()[1]
        obj.show()
        self.blinker = Sequence(
            LerpColorInterval(
                obj, 0.5,
                Vec4(0.5, 0.5, 0, 0.0),
                Vec4(0.2, 0.2, 0.2, 1)
            ),
            LerpColorInterval(
                obj, 0.5,
                Vec4(0.2, 0.2, 0.2, 1),
                Vec4(0.5, 0.5, 0, 0.0)
            )
        )
        self.blinker.loop()
        self.page1.show()

    def exitPage1(self, *args):
        self.page1.hide()
        self.page1.getChildren()[1].hide()
        self.blinker.finish()

    def enterPage2(self, *args):
        self.nextButton.hide()
        self.prevButton.show()
        self.nextButton['state'] = DGG.DISABLED
        self.prevButton['state'] = DGG.NORMAL
        self.title['text'] = (TTLocalizer.ChineseTutorialTitle2,)
        self['text'] = TTLocalizer.ChinesePage2
        self['text_pos'] = (0.0, 0.28)
        self['text_wordwrap'] = 12.5
        self.page2.show()
        self.page3.show()
        self.quitButton.show()

    def exitPage2(self, *args):
        self.page2.hide()
        self.page3.hide()
        self.quitButton.hide()
