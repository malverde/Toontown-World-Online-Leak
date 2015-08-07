#Embedded file name: toontown.tutorial.DistributedBattleTutorialAI
from direct.directnotify import DirectNotifyGlobal
from toontown.battle.DistributedBattleAI import DistributedBattleAI

class DistributedBattleTutorialAI(DistributedBattleAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBattleTutorialAI')
