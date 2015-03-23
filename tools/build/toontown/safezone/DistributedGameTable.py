import math

from direct.distributed import DistributedObject
from direct.fsm import ClassicFSM, State
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from toontown.distributed.DelayDelete import *
from toontown.safezone import PicnicGameGlobals
from toontown.safezone.PicnicGameSelectMenu import PicnicGameSelectMenu
from toontown.safezone.PicnicGameTutorial import *
from toontown.toonbase import TTLocalizer
from toontown.toonbase import ToontownGlobals
from toontown.toonbase.ToontownTimer import ToontownTimer


class DistributedGameTable(DistributedObject.DistributedObject):
    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)

        self.tableModelPath = 'phase_6/models/golf/game_table.bam'
        self.numSeats = 6
        self.__toonTracks = {}
        self.gameMenu = None
        self.game = None
        self.gameDoId = 0
        self.timerFunc = None
        self.gameWantTimer = False
        self.cameraBoardTrack = None
        self.tutorial = None
        self.fsm = ClassicFSM.ClassicFSM(
            'DistributedGameTable',
            [
                State.State(
                    'off', self.enterOff, self.exitOff,
                    ['chooseMode', 'observing']
                ),
                State.State(
                    'chooseMode', self.enterChooseMode, self.exitChooseMode,
                    ['sitting', 'off', 'observing']
                ),
                State.State(
                    'sitting', self.enterSitting, self.exitSitting,
                    ['off']
                ),
                State.State(
                    'observing', self.enterObserving, self.exitObserving,
                    ['off']
                )
            ], 'off', 'off')
        self.fsm.enterInitialState()

    def generate(self):
        DistributedObject.DistributedObject.generate(self)

        self.picnicTableNode = render.attachNewNode('gameTable')
        self.picnicTable = loader.loadModel(self.tableModelPath)
        self.picnicTable.reparentTo(self.picnicTableNode)
        self.loader = self.cr.playGame.hood.loader
        self.picnicTableNode.reparentTo(self.loader.geom)

    def announceGenerate(self):
        DistributedObject.DistributedObject.announceGenerate(self)

        self.tableCloth = self.picnicTable.find('**/basket_locator')
        cn = CollisionNode('tableCloth_sphere')
        self.tableClothSphereNode = self.tableCloth.attachNewNode(cn)
        cs = CollisionSphere(0, 0, -2, 5.5)
        self.tableClothSphereNode.node().addSolid(cs)

        self.seats = []
        self.jumpOffsets = []
        self.picnicTableSphereNodes = []
        for i in xrange(self.numSeats):
            self.seats.append(self.picnicTable.find('**/*seat' + str(i+1)))
            self.jumpOffsets.append(self.picnicTable.find('**/*jumpOut' + str(i+1)))
            cn = CollisionNode('picnicTable_sphere_%d_%d' % (self.doId, i))
            self.picnicTableSphereNodes.append(self.seats[i].attachNewNode(cn))
            cs = CollisionSphere(0, 0, 0, 2)
            self.picnicTableSphereNodes[i].node().addSolid(cs)

        self.clockNode = ToontownTimer()
        self.clockNode.setPos(1.16, 0, -0.83)
        self.clockNode.setScale(0.3)
        self.clockNode.hide()

        self.buttonModels = loader.loadModel('phase_3.5/models/gui/inventory_gui.bam')
        self.upButton = self.buttonModels.find('**//InventoryButtonUp')
        self.downButton = self.buttonModels.find('**/InventoryButtonDown')
        self.rolloverButton = self.buttonModels.find('**/InventoryButtonRollover')

        self.joinButton = None
        self.observeButton = None
        self.exitButton = None
        self.tutorialButton = None

        angle = self.picnicTable.getH()
        angle -= 90
        radAngle = math.radians(angle)
        unitVec = Vec3(math.cos(radAngle), math.sin(radAngle), 0)
        unitVec *= 30.0
        self.endPos = self.picnicTable.getPos() + unitVec

        self.enableCollisions()

    def disable(self):
        DistributedObject.DistributedObject.disable(self)
        self.fsm.request('off')
        self.clearToonTracks()
        # TODO: Disable choice buttons.
        # TODO: Stop sleep tracking.
        self.destroyGameMenu()
        self.disableCollisions()
        del self.gameMenu
        if self.cameraBoardTrack:
            self.cameraBoardTrack.finish()
        del self.cameraBoardTrack
        del self.tableClothSphereNode
        del self.tableCloth
        del self.seats
        del self.jumpOffsets
        del self.picnicTableSphereNodes
        del self.clockNode
        self.buttonModels.removeNode()
        del self.buttonModels
        del self.endPos
        del self.loader
        self.picnicTable.removeNode()
        self.picnicTableNode.removeNode()

    def delete(self):
        DistributedObject.DistributedObject.delete(self)

        del self.fsm

    def enableCollisions(self):
        for i in xrange(self.numSeats):
            event = 'enterpicnicTable_sphere_%d_%d' % (self.doId, i)
            self.accept(event, self.handleEnterPicnicTableSphere, [i])
            self.picnicTableSphereNodes[i].setCollideMask(ToontownGlobals.WallBitmask)
        self.tableClothSphereNode.setCollideMask(ToontownGlobals.WallBitmask)

    def disableCollisions(self):
        for i in xrange(self.numSeats):
            self.ignore('enterpicnicTable_sphere_%d_%d' % (self.doId, i))
        for i in xrange(self.numSeats):
            self.picnicTableSphereNodes[i].setCollideMask(BitMask32(0))
        self.tableClothSphereNode.setCollideMask(BitMask32(0))

    def handleEnterPicnicTableSphere(self, i, collEntry):
        self.fsm.request('chooseMode')

    def enterOff(self):
        base.setCellsActive(base.leftCells + base.bottomCells, 0)

    def exitOff(self):
        base.setCellsActive(base.bottomCells, 0)

    def enterChooseMode(self):
        self.enableChoiceButtons()

    def exitChooseMode(self):
        self.disableChoiceButtons()

    def enterObserving(self):
        pass

    def exitObserving(self):
        pass

    def enterSitting(self):
        pass

    def exitSitting(self):
        self.destroyGameMenu()

    def destroyGameMenu(self):
        if self.gameMenu:
            self.gameMenu.removeButtons()
            self.gameMenu.picnicFunction = None
            self.gameMenu = None

    def setPosHpr(self, x, y, z, h, p, r):
        self.picnicTable.setPosHpr(x, y, z, h, p, r)

    def storeToonTrack(self, avId, track):
        self.clearToonTrack(avId)
        self.__toonTracks[avId] = track

    def clearToonTrack(self, avId):
        oldTrack = self.__toonTracks.get(avId)
        if oldTrack:
            oldTrack.pause()
            cleanupDelayDeletes(oldTrack)

    def clearToonTracks(self):
        for avId in self.__toonTracks:
            self.clearToonTrack(avId)

    def showTimer(self):
        self.clockNode.stop()
        self.clockNode.countdown(self.timeLeft, self.timerFunc)
        self.clockNode.show()

    def setTimer(self, timerEnd):
        self.clockNode.stop()
        time = globalClockDelta.networkToLocalTime(timerEnd)
        self.timeLeft = int(time - globalClock.getRealTime())
        if self.gameWantTimer and (self.game is not None):
            self.showTimer()

    def setTimerFunc(self, function):
        self.timerFunc = function

    def allowWalk(self):
        base.cr.playGame.getPlace().setState('walk')

    def disallowWalk(self):
        base.cr.playGame.getPlace().setState('stopped')

    def enableChoiceButtons(self):
        if (not self.game) or (not self.game.playing):
            self.joinButton = DirectButton(
                relief=None, text=TTLocalizer.PicnicTableJoinButton,
                text_fg=(1, 1, 0.65, 1), text_pos=(0, -0.23), text_scale=0.8,
                image=(self.upButton, self.downButton, self.rolloverButton),
                image_color=(1, 0, 0, 1), image_scale=(20, 1, 11),
                pos=(0, 0, 0.8), scale=0.15,
                command=lambda self=self: self.joinButtonPushed())
        else:
            self.observeButton = DirectButton(
                relief=None, text=TTLocalizer.PicnicTableObserveButton,
                text_fg=(1, 1, 0.65, 1), text_pos=(0, -0.23), text_scale=0.8,
                image=(self.upButton, self.downButton, self.rolloverButton),
                image_color=(1, 0, 0, 1), image_scale=(20, 1, 11),
                pos=(0, 0, 0.6), scale=0.15,
                command=lambda self=self: self.observeButtonPushed())
        self.exitButton = DirectButton(
            relief=None, text=TTLocalizer.PicnicTableCancelButton,
            text_fg=(1, 1, 0.65, 1), text_pos=(0, -0.23), text_scale=0.8,
            image=(self.upButton, self.downButton, self.rolloverButton),
            image_color=(1, 0, 0, 1), image_scale=(20, 1, 11), pos=(1, 0, 0.6),
            scale=0.15, command=lambda self=self: self.cancelButtonPushed())
        self.tutorialButton = DirectButton(
            relief=None, text=TTLocalizer.PicnicTableTutorial,
            text_fg=(1, 1, 0.65, 1), text_pos=(-0.05, -0.13), text_scale=0.55,
            image=(self.upButton, self.downButton, self.rolloverButton),
            image_color=(1, 0, 0, 1), image_scale=(20, 1, 11), pos=(-1, 0, 0.6),
            scale=0.15, command=lambda self=self: self.tutorialButtonPushed())
        self.disallowWalk()

    def disableChoiceButtons(self):
        if self.joinButton:
            self.joinButton.destroy()
            self.joinButton = None
        if self.observeButton:
            self.observeButton.destroy()
            self.observeButton = None
        if self.exitButton:
            self.exitButton.destroy()
            self.exitButton = None
        if self.tutorialButton:
            self.tutorialButton.destroy()
            self.tutorialButton = None

    def joinButtonPushed(self):
        pass

    def observeButtonPushed(self):
        pass

    def cancelButtonPushed(self):
        self.allowWalk()
        self.fsm.request('off')

    def tutorialButtonPushed(self):
        self.disableChoiceButtons()
        self.gameMenu = PicnicGameSelectMenu(
            self.tutorialFunction, PicnicGameGlobals.TutorialMenu)

    def tutorialFunction(self, gameIndex):
        if gameIndex == PicnicGameGlobals.CheckersGameIndex:
            self.tutorial = CheckersTutorial(self.tutorialDone)
        elif gameIndex == PicnicGameGlobals.ChineseCheckersGameIndex:
            self.tutorial = ChineseCheckersTutorial(self.tutorialDone)
        else:
            self.cancelButtonPushed()
        self.destroyGameMenu()

    def tutorialDone(self):
        self.fsm.request('off')
        self.tutorial = None
