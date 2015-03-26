from pandac.PandaModules import *
from toontown.battle import BattleProps
from toontown.toonbase import ToontownGlobals
from toontown.toonbase.ToontownBattleGlobals import *
from direct.directnotify import DirectNotifyGlobal
import string
from toontown.suit import Suit
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from toontown.toonbase import TTLocalizer
from direct.task.Task import Task

class TownBattleCogPanel(DirectFrame):
    notify = DirectNotifyGlobal.directNotify.newCategory('TownBattleCogPanel')
    healthColors = (Vec4(0, 1, 0, 1),# 0 Green
     Vec4(0.5, 1, 0, 1),#1 Green-Yellow
     Vec4(0.75, 1, 0, 1),#2 Yellow-Green
     Vec4(1, 1, 0, 1),#3 Yellow
     Vec4(1, 0.866, 0, 1),#4 Yellow-Orange
     Vec4(1, 0.6, 0, 1),#5 Orange-Yellow
     Vec4(1, 0.5, 0, 1),#6 Orange
     Vec4(1, 0.25, 0, 1.0),#7 Red-Orange
     Vec4(1, 0, 0, 1),#8 Red
     Vec4(0.3, 0.3, 0.3, 1))#9 Grey
    healthGlowColors = (Vec4(0.25, 1, 0.25, 0.5),#Green
     Vec4(0.5, 1, 0.25, .5),#1 Green-Yellow
     Vec4(0.75, 1, 0.25, .5),#2 Yellow-Green
     Vec4(1, 1, 0.25, 0.5),#Yellow 
     Vec4(1, 0.866, 0.25, .5),#4 Yellow-Orange
     Vec4(1, 0.6, 0.25, .5),#5 Orange-Yellow
     Vec4(1, 0.5, 0.25, 0.5),#6 Orange
     Vec4(1, 0.25, 0.25, 0.5),#7 Red-Orange    
     Vec4(1, 0.25, 0.25, 0.5),#8 Red     
     Vec4(0.3, 0.3, 0.3, 0))#9 Grey
    
    def __init__(self, id):
        gui = loader.loadModel('phase_3.5/models/gui/battle_gui')
        DirectFrame.__init__(self, relief=None, image=gui.find('**/ToonBtl_Status_BG'), image_color=Vec4(0.5, 0.5, 0.5, 0.7))
        self.setScale(0.8)
        self.initialiseoptions(TownBattleCogPanel)
        self.levelText = DirectLabel(parent=self, text='', pos=(-0.06, 0, -0.075), text_scale=0.055)
        self.healthBar = None
        self.healthBarGlow = None
        self.hpChangeEvent = None
        self.blinkTask = None
        self.suit = None
        self.head = None
        self.maxHP = None
        self.currHP = None
        self.hpChangeEvent = None
        self.generateHealthBar()
        self.hide()
        gui.removeNode()
        return
        
    def setSuit(self, suit):
        if self.suit == suit:
            messenger.send(self.suit.uniqueName('hpChange'))
            return
        self.suit = suit
        self.setLevelText(self.suit.getActualLevel())
        if self.head:
            self.head.removeNode()
        self.setSuitHead(self.suit.getStyleName())
        self.setMaxHp(self.suit.getMaxHP())
        self.setHp(self.suit.getHP())
        self.hpChangeEvent = self.suit.uniqueName('hpChange')
        if self.blinkTask:
            taskMgr.remove(self.blinkTask)
            self.blinkTask = None
        self.accept(self.hpChangeEvent, self.updateHealthBar)
        self.updateHealthBar()
        self.healthBar.show()
        
    def getSuit(self, suit):
        return self.suit

    def setLevelText(self, level):
        self.levelText['text'] = 'Level '+ str(level)

    def setSuitHead(self, suitName):
        self.head = Suit.attachSuitHead(self, suitName)
        self.head.setX(0.1)
        self.head.setZ(0.01)

    def generateHealthBar(self):
        model = loader.loadModel('phase_3.5/models/gui/matching_game_gui')
        button = model.find('**/minnieCircle')
        model.removeNode()
        button.setScale(0.5)
        button.setH(180.0)
        button.setColor(self.healthColors[0])
        button.reparentTo(self)
        button.setX(-0.08)
        button.setZ(0.02)
        self.healthBar = button
        glow = BattleProps.globalPropPool.getProp('glow')
        glow.reparentTo(self.healthBar)
        glow.setScale(0.28)
        glow.setPos(-0.005, 0.01, 0.015)
        glow.setColor(self.healthGlowColors[0])
        button.flattenLight()
        self.healthBarGlow = glow
        self.healthBar.hide()
        self.healthCondition = 0 

    def updateHealthBar(self):
        if not self.suit:
            return
        self.setHp(self.suit.getHP())
        health = float(self.currHP) / float(self.maxHP)
        if health > 0.95:
            condition = 0
        elif health > 0.9:
            condition = 1
        elif health > 0.8:
            condition = 2
        elif health > 0.7:
            condition = 3#Yellow
        elif health > 0.6:
            condition = 4            
        elif health > 0.5:
            condition = 5           
        elif health > 0.3:
            condition = 6#Orange
        elif health > 0.15:
            condition = 7
        elif health > 0.05:
            condition = 8#Red           
        elif health > 0.0:
            condition = 9#Blinking Red
        else:
            condition = 10
        if self.healthCondition != condition:
            if condition == 9:
                self.blinkTask = self.uniqueName('blink-task')                
                blinkTask = Task.loop(Task(self.__blinkRed), Task.pause(0.75), Task(self.__blinkGray), Task.pause(0.1))
                taskMgr.add(blinkTask, self.blinkTask)
            elif condition == 10:
                if self.healthCondition == 9:
                    self.blinkTask = self.uniqueName('blink-task')    
                    taskMgr.remove(self.blinkTask)
                    self.blinkTask = None
                blinkTask = Task.loop(Task(self.__blinkRed), Task.pause(0.25), Task(self.__blinkGray), Task.pause(0.1))
                taskMgr.add(blinkTask, self.blinkTask)
            else:
                if self.blinkTask:
                    taskMgr.remove(self.blinkTask)
                    self.blinkTask = None
                self.healthBar.setColor(self.healthColors[condition], 1)
                self.healthBarGlow.setColor(self.healthGlowColors[condition], 1)
            self.healthCondition = condition

    def __blinkRed(self, task):
        if not self.blinkTask or not self.healthBar:
            return Task.done  
        self.healthBar.setColor(self.healthColors[8], 1)
        self.healthBarGlow.setColor(self.healthGlowColors[8], 1)
        if self.healthCondition == 7:
            self.healthBar.setScale(1.17)
        return Task.done

    def __blinkGray(self, task):
        if not self.blinkTask or not self.healthBar:
            return Task.done
        self.healthBar.setColor(self.healthColors[9], 1)
        self.healthBarGlow.setColor(self.healthGlowColors[9], 1)
        if self.healthCondition == 10:
            self.healthBar.setScale(1.0)
        return Task.done

    def removeHealthBar(self):
        if self.healthCondition == 9 or self.healthCondition == 10:
            if self.blinkTask:
                taskMgr.remove(self.blinkTask)
                self.blinkTask = None    
        if self.healthBar:
            self.healthBar.removeNode()
            self.healthBar = None
        self.healthCondition = 0
        return
        
    def getDisplayedCurrHp(self):
        return self.currHP
        
    def getDisplayedMaxHp(self):
        return self.maxHP   

    def setMaxHp(self, hp):
        self.maxHP = hp

    def setHp(self, hp):
        self.currHP = hp

    def show(self):
        DirectFrame.show(self)
        
    def cleanup(self):
        self.ignoreAll()
        self.removeHealthBar()
        if self.head is not None:
            self.head.removeNode()
        del self.head
        self.levelText.destroy()
        del self.levelText
        del self.healthBar
        if self.healthBarGlow is not None:
            self.healthBarGlow.removeNode()
        del self.healthBarGlow
        del self.suit
        del self.maxHP
        del self.currHP
        DirectFrame.destroy(self)
