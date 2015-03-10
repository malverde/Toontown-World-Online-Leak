from TrolleyConstants import *
from direct.distributed.ClockDelta import *
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *
from toontown.toonbase import TTLocalizer
from toontown.toonbase import ToontownGlobals
from toontown.safezone import PicnicGameGlobals


class PicnicGameSelectMenu(DirectFrame):
    def __init__(self, picnicFunction, menuType):
        self.picnicFunction = picnicFunction
        DirectFrame.__init__(
            self, pos=(0.0, 0.0, 0.85),
            image_color=ToontownGlobals.GlobalDialogColor,
            image_scale=(1.8, 0.9, 0.13), text='', text_scale=0.05)
        self.buttonModels = loader.loadModel('phase_3.5/models/gui/inventory_gui.bam')
        self.upButton = self.buttonModels.find('**//InventoryButtonUp')
        self.downButton = self.buttonModels.find('**/InventoryButtonDown')
        self.rolloverButton = self.buttonModels.find('**/InventoryButtonRollover')
        if menuType == PicnicGameGlobals.TutorialMenu:
            self.title = DirectLabel(
                self, relief=None,
                text=TTLocalizer.PicnicTableMenuTutorial,
                text_pos=(0.0, -0.038), text_fg=(1, 1, 1, 1),
                text_scale=0.09, text_font=ToontownGlobals.getSignFont(),
                text_shadow=(0, 0, 0, 0.8), text_shadowOffset=(-0.1, -0.1))
        elif menuType == PicnicGameGlobals.GameMenu:
            self.title = DirectLabel(
                self, relief=None, text=TTLocalizer.PicnicTableMenuSelect,
                text_pos=(0.0, -0.038), text_fg=(1, 1, 1, 1), text_scale=0.09,
                text_font=ToontownGlobals.getSignFont(),
                text_shadow=(0, 0, 0, 0.8), text_shadowOffset=(-0.1, -0.1))
        self.selectionButtons = loader.loadModel('phase_6/models/golf/picnic_game_menu.bam')
        btn1 = self.selectionButtons.find('**/Btn1')
        btn2 = self.selectionButtons.find('**/Btn2')
        btn3 = self.selectionButtons.find('**/Btn3')
        self.ChineseCheckers = DirectButton(
            self, image=(btn1.find('**/checkersBtnUp'),
                         btn1.find('**/checkersBtnDn'),
                         btn1.find('**/checkersBtnHi'),
                         btn1.find('**/checkersBtnUp')),
            scale=0.36, relief=0, pos=(0, 0, -0.7),
            command=self.chineseCheckersSelected)
        self.Checkers = DirectButton(
            self, image=(btn2.find('**/regular_checkersBtnUp'),
                         btn2.find('**/regular_checkersBtnDn'),
                         btn2.find('**/regular_checkersBtnHi'),
                         btn2.find('**/regular_checkersBtnUp')),
            scale=0.36, relief=0, pos=(0.8, 0, -0.7),
            command=self.checkersSelected)
        self.FindFour = DirectButton(
            self, image=(btn3.find('**/findfourBtnUp'),
                         btn3.find('**/findfourBtnDn'),
                         btn3.find('**/findfourBtnHi'),
                         btn3.find('**/findfourBtnUp')),
            scale=0.36, relief=0, pos=(-0.8, 0, -0.7),
            command=self.findFourSelected)
        if not base.config.GetBool('want-checkers', 0):
            self.Checkers['command'] = lambda:None
            self.Checkers.setColor(0.7, 0.7, 0.7, 0.7)
        if not base.config.GetBool('want-chinese-checkers', 0):
            self.ChineseCheckers['command'] = lambda:None
            self.ChineseCheckers.setColor(0.7, 0.7, 0.7, 0.7)
        if not base.config.GetBool('want-find-four', 0):
            self.FindFour['command'] = lambda:None
            self.FindFour.setColor(0.7, 0.7, 0.7, 0.7)
        self.chineseText = OnscreenText(
            text='Chinese Checkers', pos=(0, 0.56, -0.8), scale=0.15,
            fg=Vec4(1, 1, 1, 1), align=TextNode.ACenter,
            font=ToontownGlobals.getMinnieFont(), wordwrap=7,
            shadow=(0, 0, 0, 0.8), shadowOffset=(-0.1, -0.1), mayChange=True)
        self.chineseText.setR(-8)
        self.checkersText = OnscreenText(
            text='Checkers', pos=(0.81, -.1, -0.8), scale=0.15,
            fg=Vec4(1, 1, 1, 1), align=TextNode.ACenter,
            font=ToontownGlobals.getMinnieFont(), wordwrap=7,
            shadow=(0, 0, 0, 0.8), shadowOffset=(0.1, -0.1), mayChange=True)
        self.findFourText = OnscreenText(
            text='Find Four', pos=(-0.81, -.08, -0.8), scale=0.15,
            fg=Vec4(1, 1, 1, 1), align=TextNode.ACenter,
            font=ToontownGlobals.getMinnieFont(), wordwrap=8,
            shadow=(0, 0, 0, 0.8), shadowOffset=(-0.1, -0.1), mayChange=True)
        self.exitButton = DirectButton(
            relief=None, text=TTLocalizer.PicnicTableCancelButton,
            text_fg=(1, 1, 0.65, 1), text_pos=(0, -0.23), text_scale=0.8,
            image=(self.upButton, self.downButton, self.rolloverButton),
            image_color=(1, 0, 0, 1), image_scale=(20, 1, 11), pos=(0, 0, -0.4),
            scale=0.15, command=lambda self=self: self.cancelButtonPushed())
        self.findFourText.setR(-8)
        self.checkersText.setR(8)

    def delete(self):
        self.removeButtons()

    def removeButtons(self):
        self.ChineseCheckers.destroy()
        self.Checkers.destroy()
        self.FindFour.destroy()
        self.chineseText.destroy()
        self.checkersText.destroy()
        self.findFourText.destroy()
        self.exitButton.destroy()
        DirectFrame.destroy(self)

    def checkersSelected(self):
        self.picnicFunction(PicnicGameGlobals.CheckersGameIndex)
        self.picnicFunction = lambda gameIndex: None

    def chineseCheckersSelected(self):
        self.picnicFunction(PicnicGameGlobals.ChineseCheckersGameIndex)
        self.picnicFunction = lambda gameIndex: None

    def findFourSelected(self):
        self.picnicFunction(PicnicGameGlobals.FindFourGameIndex)
        self.picnicFunction = lambda gameIndex: None

    def cancelButtonPushed(self):
        self.picnicFunction(-1)
        self.picnicFunction = lambda gameIndex: None
