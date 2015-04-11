from pandac.PandaModules import NodePath, TextNode, Vec4

from direct.gui.DirectWaitBar import DirectWaitBar
from direct.gui import DirectGuiGlobals

from toontown.suit import SuitDNA
from toontown.coghq import CogDisguiseGlobals
from toontown.shtiker import DisguisePage
from toontown.toonbase import TTLocalizer
from toontown.toonbase import ToontownGlobals


class CogMenuBar(NodePath):
    DEPT_INDEX = {
        's': 3,
        'm': 2,
        'l': 1,
        'c': 0
    }

    ICON_NODES = [
        '**/CorpIcon',
        '**/LegalIcon',
        '**/MoneyIcon',
        '**/SalesIcon'
    ]

    ICON_COLORS = [
        Vec4(0.863, 0.776, 0.769, 1.0),
        Vec4(0.749, 0.776, 0.824, 1.0),
        Vec4(0.749, 0.769, 0.749, 1.0),
        Vec4(0.843, 0.745, 0.745, 1.0)
    ]

    def __init__(self, cogMenu, dept):
        NodePath.__init__(self, 'CogMenuBar-%s' % dept)

        self.dept = dept
        self.deptIndex = self.DEPT_INDEX[dept]

        icons = loader.loadModel('phase_3/models/gui/cog_icons')
        self.icon = icons.find(self.ICON_NODES[self.deptIndex]).copyTo(self)
        self.icon.setColor(self.ICON_COLORS[self.deptIndex])
        self.icon.setScale(0.07)
        self.icon.setX(-0.25)
        icons.removeNode()

        self.progressBar = DirectWaitBar(parent=self, relief=DirectGuiGlobals.SUNKEN,
                                         frameSize=(-1, 1, -0.15, 0.15),
                                         borderWidth=(0.02, 0.02),
                                         scale=0.20,
                                         frameColor=(DisguisePage.DeptColors[self.deptIndex][0] * 0.7,
                                                     DisguisePage.DeptColors[self.deptIndex][1] * 0.7,
                                                     DisguisePage.DeptColors[self.deptIndex][2] * 0.7,
                                                     1),
                                         barColor=(DisguisePage.DeptColors[self.deptIndex][0],
                                                   DisguisePage.DeptColors[self.deptIndex][1],
                                                   DisguisePage.DeptColors[self.deptIndex][2],
                                                   1),
                                         text='0/0 ' + TTLocalizer.RewardPanelMeritBarLabels[self.deptIndex],
                                         text_scale=TTLocalizer.RPmeritBarLabels, text_fg=(0, 0, 0, 1),
                                         text_align=TextNode.ALeft, text_pos=(-0.96, -0.05))

        self.reparentTo(cogMenu)

    def update(self):
        if not CogDisguiseGlobals.isSuitComplete(base.localAvatar.cogParts, self.deptIndex):
            self.progressBar['text'] = '%s %s' % (
                CogDisguiseGlobals.getPartCountAsString(base.localAvatar.cogParts, self.deptIndex),
                TTLocalizer.DisguiseParts)

            self.progressBar['range'] = CogDisguiseGlobals.PartsPerSuit[self.deptIndex]
            self.progressBar['value'] = CogDisguiseGlobals.getPartCount(base.localAvatar.cogParts, self.deptIndex)
            return

        promoStatus = base.localAvatar.promotionStatus[self.deptIndex]

        if promoStatus != ToontownGlobals.PendingPromotion:
            totalMerits = CogDisguiseGlobals.getTotalMerits(base.localAvatar, self.deptIndex)
            merits = base.localAvatar.cogMerits[self.deptIndex]

            self.progressBar['range'] = totalMerits
            self.progressBar['value'] = merits

            self.progressBar['text'] = '%s/%s %s' % (
            merits, totalMerits, TTLocalizer.RewardPanelMeritBarLabels[self.deptIndex])
        else:
            self.progressBar['range'] = 1
            self.progressBar['value'] = 1

            maxSuitLevel = (SuitDNA.levelsPerSuit - 1) + (SuitDNA.suitsPerDept - 1)
            if base.localAvatar.cogLevels[self.deptIndex] == maxSuitLevel:
                self.progressBar['text'] = TTLocalizer.RewardPanelMeritsMaxed
            else:
                self.progressBar['text'] = TTLocalizer.RewardPanelPromotionPending

    def cleanup(self):
        self.icon.removeNode()
        self.progressBar.destroy()
        self.removeNode()