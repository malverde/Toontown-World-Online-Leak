from pandac.PandaModules import *
import ShtikerPage
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from toontown.toonbase import TTLocalizer
import DisplaySettingsDialog
from direct.task import Task
from direct.showbase import PythonUtil
from direct.directnotify import DirectNotifyGlobal
from otp.ai.MagicWordGlobal import *
from otp.chat import ChatManager
from TTChatInputSpeedChat import TTChatInputSpeedChat
from TTChatInputNormal import TTChatInputNormal
from TTChatInputWhiteList import TTChatInputWhiteList

class CodesTabPage(DirectFrame):
    notify = DirectNotifyGlobal.directNotify.newCategory('CodesTabPage')

    def __init__(self, parent = aspect2d):
        self.parent = parent
        DirectFrame.__init__(self, parent=self.parent, relief=None, pos=(0.0, 0.0, 0.0), scale=(1.0, 1.0, 1.0))
        self.load()
        return

    def destroy(self):
        self.parent = None
        DirectFrame.destroy(self)
        return

    def load(self):
        cdrGui = loader.loadModel('phase_3.5/models/gui/tt_m_gui_sbk_codeRedemptionGui')
        # instructionGui = cdrGui.find('**/tt_t_gui_sbk_cdrPresent')
        # flippyGui = cdrGui.find('**/tt_t_gui_sbk_cdrFlippy')
        codeBoxGui = cdrGui.find('**/tt_t_gui_sbk_cdrCodeBox')
        self.resultPanelSuccessGui = cdrGui.find('**/tt_t_gui_sbk_cdrResultPanel_success')
        self.resultPanelFailureGui = cdrGui.find('**/tt_t_gui_sbk_cdrResultPanel_failure')
        self.resultPanelErrorGui = cdrGui.find('**/tt_t_gui_sbk_cdrResultPanel_error')
        self.successSfx = base.loadSfx('phase_3.5/audio/sfx/tt_s_gui_sbk_cdrSuccess.ogg')
        self.failureSfx = base.loadSfx('phase_3.5/audio/sfx/tt_s_gui_sbk_cdrFailure.ogg')
        # self.instructionPanel = DirectFrame(parent=self, relief=None, image=instructionGui, image_scale=0.8,
        #                                     text=TTLocalizer.CdrInstructions,
        #                                     text_pos=TTLocalizer.OPCodesInstructionPanelTextPos,
        #                                     text_align=TextNode.ACenter,
        #                                     text_scale=TTLocalizer.OPCodesResultPanelTextScale,
        #                                     text_wordwrap=TTLocalizer.OPCodesInstructionPanelTextWordWrap,
        #                                     pos=(-0.429, 0, -0.05))
        self.codeBox = DirectFrame(parent=self, relief=None, image=codeBoxGui, pos=(0.433, 0, 0.35))
        # self.flippyFrame = DirectFrame(parent=self, relief=None, image=flippyGui, pos=(0.44, 0, -0.353))
        self.codeInput = DirectEntry(parent=self.codeBox, relief=DGG.GROOVE, scale=0.08, pos=(-0.33, 0, -0.006),
                                     borderWidth=(0.05, 0.05),
                                     frameColor=((1, 1, 1, 1), (1, 1, 1, 1), (0.5, 0.5, 0.5, 0.5)), state=DGG.NORMAL,
                                     text_align=TextNode.ALeft, text_scale=TTLocalizer.OPCodesInputTextScale,
                                     width=10.5, numLines=1, focus=1, backgroundFocus=0, cursorKeys=1,
                                     text_fg=(0, 0, 0, 1), suppressMouse=1, autoCapitalize=0, command=self.__submitCode)
        submitButtonGui = loader.loadModel('phase_3/models/gui/quit_button')
        self.submitButton = DirectButton(parent=self, relief=None, image=(submitButtonGui.find('**/QuitBtn_UP'),
                                                                          submitButtonGui.find('**/QuitBtn_DN'),
                                                                          submitButtonGui.find('**/QuitBtn_RLVR'),
                                                                          submitButtonGui.find('**/QuitBtn_UP')),
                                         image3_color=Vec4(0.5, 0.5, 0.5, 0.5), image_scale=1.15, state=DGG.NORMAL,
                                         text=TTLocalizer.NameShopSubmitButton,
                                         text_scale=TTLocalizer.OPCodesSubmitTextScale, text_align=TextNode.ACenter,
                                         text_pos=TTLocalizer.OPCodesSubmitTextPos, text3_fg=(0.5, 0.5, 0.5, 0.75),
                                         textMayChange=0, pos=(0.45, 0.0, 0.0896), command=self.__submitCode)
        self.resultPanel = DirectFrame(parent=self, relief=None, image=self.resultPanelSuccessGui, text='',
                                       text_pos=TTLocalizer.OPCodesResultPanelTextPos, text_align=TextNode.ACenter,
                                       text_scale=TTLocalizer.OPCodesResultPanelTextScale,
                                       text_wordwrap=TTLocalizer.OPCodesResultPanelTextWordWrap,
                                       pos=(-0.42, 0, -0.0567))
        self.resultPanel.hide()
        closeButtonGui = loader.loadModel('phase_3/models/gui/dialog_box_buttons_gui')
        self.closeButton = DirectButton(parent=self.resultPanel, pos=(0.296, 0, -0.466), relief=None, state=DGG.NORMAL,
                                        image=(
                                        closeButtonGui.find('**/CloseBtn_UP'), closeButtonGui.find('**/CloseBtn_DN'),
                                        closeButtonGui.find('**/CloseBtn_Rllvr')), image_scale=(1, 1, 1),
                                        command=self.__hideResultPanel)
        closeButtonGui.removeNode()
        cdrGui.removeNode()
        submitButtonGui.removeNode()
        return

    def enter(self):
        self.show()
        localAvatar.chatMgr.fsm.request('otherDialog')
        self.codeInput['focus'] = 1
        self.codeInput.enterText('')
        self.__enableCodeEntry()

    def exit(self):
        self.resultPanel.hide()
        self.hide()
        localAvatar.chatMgr.fsm.request('mainMenu')

    def unload(self):
        self.instructionPanel.destroy()
        self.instructionPanel = None
        self.codeBox.destroy()
        self.codeBox = None
        self.flippyFrame.destroy()
        self.flippyFrame = None
        self.codeInput.destroy()
        self.codeInput = None
        self.submitButton.destroy()
        self.submitButton = None
        self.resultPanel.destroy()
        self.resultPanel = None
        self.closeButton.destroy()
        self.closeButton = None
        del self.successSfx
        del self.failureSfx
        return

    def __submitCode(self, input=None):
        ChatManager.ChatManager.__init__(self, cr, localAvatar)
        self.defaultToWhiteList = config.GetBool('white-list-is-default', 1)
        self.chatInputSpeedChat = TTChatInputSpeedChat(self)
        if input == None:
            input = self.codeInput.get()
        self.codeInput['focus'] = 1
        if input == '':
            return
        messenger.send('wakeup')
        if hasattr(base, 'codeRedemptionMgr'):
            base.codeRedemptionMgr.redeemCode(input, self.__getCodeResult)
        self.codeInput.enterText('~')
        self.__disableCodeEntry()
        return

    def __getCodeResult(self, result, awardMgrResult):
        self.notify.debug('result = %s' % result)
        self.notify.debug('awardMgrResult = %s' % awardMgrResult)
        print result, awardMgrResult
        self.__enableCodeEntry()
        if result == 0:
            self.resultPanel['image'] = self.resultPanelSuccessGui
            self.resultPanel['text'] = TTLocalizer.CdrResultSuccess
        elif result == 1:
            self.resultPanel['image'] = self.resultPanelFailureGui
            self.resultPanel['text'] = TTLocalizer.CdrResultInvalidCode
        elif result == 2:
            self.resultPanel['image'] = self.resultPanelFailureGui
            self.resultPanel['text'] = TTLocalizer.CdrResultExpiredCode
        elif result == 3:
            self.resultPanel['image'] = self.resultPanelFailureGui
            self.resultPanel['text'] = TTLocalizer.CdrResultIneligible
        elif result == 4:
            self.resultPanel['image'] = self.resultPanelErrorGui
            if awardMgrResult == 0:
                self.resultPanel['text'] = TTLocalizer.CdrResultSuccess
            elif awardMgrResult == 1 or awardMgrResult == 2 or awardMgrResult == 15 or awardMgrResult == 16:
                self.resultPanel['text'] = TTLocalizer.CdrResultUnknownError
            elif awardMgrResult == 3 or awardMgrResult == 4:
                self.resultPanel['text'] = TTLocalizer.CdrResultMailboxFull
            elif awardMgrResult == 5 or awardMgrResult == 10:
                self.resultPanel['text'] = TTLocalizer.CdrResultAlreadyInMailbox
            elif awardMgrResult == 6 or awardMgrResult == 7 or awardMgrResult == 11:
                self.resultPanel['text'] = TTLocalizer.CdrResultAlreadyInQueue
            elif awardMgrResult == 8:
                self.resultPanel['text'] = TTLocalizer.CdrResultAlreadyInCloset
            elif awardMgrResult == 9:
                self.resultPanel['text'] = TTLocalizer.CdrResultAlreadyBeingWorn
            elif awardMgrResult == 12 or awardMgrResult == 13 or awardMgrResult == 14:
                self.resultPanel['text'] = TTLocalizer.CdrResultAlreadyReceived
        elif result == 5:
            self.resultPanel['text'] = TTLocalizer.CdrResultTooManyFails
            self.__disableCodeEntry()
        elif result == 6:
            self.resultPanel['text'] = TTLocalizer.CdrResultServiceUnavailable
            self.__disableCodeEntry()
        if result == 0:
            self.successSfx.play()
        else:
            self.failureSfx.play()
        self.resultPanel.show()

    def __hideResultPanel(self):
        self.resultPanel.hide()

    def __disableCodeEntry(self):
        self.codeInput['state'] = DGG.DISABLED
        self.submitButton['state'] = DGG.DISABLED

    def __enableCodeEntry(self):
        self.codeInput['state'] = DGG.NORMAL
        self.codeInput['focus'] = 1
        self.submitButton['state'] = DGG.NORMAL
