from toontown.toonbase.ToonBaseGlobal import *
from pandac.PandaModules import *
from toontown.toonbase.ToontownGlobals import *
import random
from direct.task.Task import Task
from direct.distributed import DistributedObject
from direct.directnotify import DirectNotifyGlobal
import ToonInteriorColors
import cPickle
from toontown.toonbase import TTLocalizer
from toontown.dna.DNADoor import DNADoor

class DistributedHQInterior(DistributedObject.DistributedObject):

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        self.dnaStore = cr.playGame.dnaStore
        self.leaderAvIds = []
        self.leaderNames = []
        self.leaderScores = []
        self.numLeaders = 10
        self.tutorial = 0

    def generate(self):
        DistributedObject.DistributedObject.generate(self)
        self.interior = loader.loadModel('phase_3.5/models/modules/HQ_interior')
        self.interior.reparentTo(render)
        self.interior.find('**/cream').hide()
        self.interior.find('**/crashed_piano').hide()
        self.buildLeaderBoard()

    def announceGenerate(self):
        DistributedObject.DistributedObject.announceGenerate(self)
        self.setupDoors()
        self.interior.flattenMedium()
        emptyBoard = self.interior.find('**/empty_board')
        self.leaderBoard.reparentTo(emptyBoard.getChild(0))
        base.cr.hqLoaded = True
        messenger.send('hqInternalDone')

    def setTutorial(self, flag):
        if self.tutorial == flag:
            return
        self.tutorial = flag
        if self.tutorial:
            self.interior.find('**/periscope').hide()
            self.interior.find('**/speakers').hide()
        else:
            self.interior.find('**/periscope').show()
            self.interior.find('**/speakers').show()

    def setZoneIdAndBlock(self, zoneId, block):
        self.zoneId = zoneId
        self.block = block

    def buildLeaderBoard(self):
        self.leaderBoard = hidden.attachNewNode('leaderBoard')
        self.leaderBoard.setPosHprScale(0.1, 0, 4.5, 90, 0, 0, 0.9, 0.9, 0.9)
        z = 0
        row = self.buildTitleRow()
        row.reparentTo(self.leaderBoard)
        row.setPos(0, 0, z)
        z -= 1
        self.nameTextNodes = []
        self.scoreTextNodes = []
        self.trophyStars = []
        for i in range(self.numLeaders):
            row, nameText, scoreText, trophyStar = self.buildLeaderRow()
            self.nameTextNodes.append(nameText)
            self.scoreTextNodes.append(scoreText)
            self.trophyStars.append(trophyStar)
            row.reparentTo(self.leaderBoard)
            row.setPos(0, 0, z)
            z -= 1

    def updateLeaderBoard(self):
        taskMgr.remove(self.uniqueName('starSpinHQ'))
        for i in range(len(self.leaderNames)):
            name = self.leaderNames[i]
            score = self.leaderScores[i]
            self.nameTextNodes[i].setText(name)
            self.scoreTextNodes[i].setText(str(score))
            self.updateTrophyStar(self.trophyStars[i], score)

        for i in range(len(self.leaderNames), self.numLeaders):
            self.nameTextNodes[i].setText('-')
            self.scoreTextNodes[i].setText('-')
            self.trophyStars[i].hide()

    def buildTitleRow(self):
        row = hidden.attachNewNode('leaderRow')
        nameText = TextNode('titleRow')
        nameText.setFont(ToontownGlobals.getSignFont())
        nameText.setAlign(TextNode.ACenter)
        nameText.setTextColor(0.5, 0.75, 0.7, 1)
        nameText.setText(TTLocalizer.LeaderboardTitle)
        namePath = row.attachNewNode(nameText)
        namePath.setPos(0, 0, 0)
        return row
