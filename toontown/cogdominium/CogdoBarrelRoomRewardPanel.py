#Embedded file name: toontown.cogdominium.CogdoBarrelRoomRewardPanel
from panda3d.core import *
from direct.gui.DirectGui import *
from toontown.toon import DistributedToon
from toontown.toonbase import ToontownGlobals, TTLocalizer
from toontown.cogdominium import CogdoBarrelRoomConsts

class CogdoBarrelRoomRewardPanel(DirectFrame):

    def __init__(self):
        DirectFrame.__init__(self, relief=None, geom=DGG.getDefaultDialogGeom(), geom_color=ToontownGlobals.GlobalDialogColor, geom_scale=TTLocalizer.RPdirectFrame, pos=(0, 0, -0.587))
        self.initialiseoptions(CogdoBarrelRoomRewardPanel)
        self.avNameLabel = DirectLabel(parent=self, relief=None, pos=(0, 0, 0.3), text='Toon Ups', text_scale=0.08)
        self.rewardLines = []
        for i in xrange(CogdoBarrelRoomConsts.MaxToons):
            rewardLine = {'frame': DirectFrame(parent=self, relief=None, frameSize=(-0.5, 0.5, -0.045, 0.042),
                                               pos=(0, 0, 0.1 + -0.09 * i))}
            rewardLine['name'] = DirectLabel(parent=rewardLine['frame'], relief=None, text='', text_scale=TTLocalizer.RPtrackLabels, text_align=TextNode.ALeft, pos=(-0.4, 0, 0), text_pos=(0, -0.02))
            rewardLine['laff'] = DirectLabel(parent=rewardLine['frame'], relief=None, text='', text_scale=0.05, text_align=TextNode.ARight, pos=(0.4, 0, 0), text_pos=(0, -0.02))
            self.rewardLines.append(rewardLine)

    def setRewards(self):
        RewardLineIndex = 0
        for doId in base.cr.doId2do:
            toon = base.cr.doId2do.get(doId)
            if isinstance(toon, DistributedToon.DistributedToon):
                self.rewardLines[RewardLineIndex]['name'].setProp('text', toon.getName())
                self.rewardLines[RewardLineIndex]['laff'].setProp('text', '%s/%s' % (str(toon.hp), str(toon.maxHp)))
                if doId == base.localAvatar.getDoId():
                    self.rewardLines[RewardLineIndex]['frame'].setProp('relief', DGG.RIDGE)
                    self.rewardLines[RewardLineIndex]['frame'].setProp('borderWidth', (0.01, 0.01))
                    self.rewardLines[RewardLineIndex]['frame'].setProp('frameColor', (1, 1, 1, 0.5))
                RewardLineIndex += 1
