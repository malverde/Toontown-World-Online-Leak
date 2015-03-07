from direct.directnotify.DirectNotifyGlobal import *
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.fsm.FSM import FSM

from toontown.ai import DistributedBlackCatMgrAI
from toontown.building import FADoorCodes
from toontown.building.HQBuildingAI import HQBuildingAI
from toontown.building.TutorialBuildingAI import TutorialBuildingAI
from toontown.quest import Quests
from toontown.suit.DistributedTutorialSuitAI import DistributedTutorialSuitAI
from toontown.toon import NPCToons
from toontown.toonbase import ToontownBattleGlobals
from toontown.toonbase import ToontownGlobals


class TutorialFSM(FSM):
    def __init__(self, air, zones, avId):
        FSM.__init__(self, 'TutorialFSM')

        self.air = air
        self.zones = zones
        self.avId = avId

        npcDesc = NPCToons.NPCToonDict.get(20000)
        self.tutorialTom = NPCToons.createNPC(self.air, 20000, npcDesc, self.zones['building'])
        self.tutorialTom.setTutorial(1)

        npcDesc = NPCToons.NPCToonDict.get(20002)
        self.hqHarry = NPCToons.createNPC(self.air, 20002, npcDesc, self.zones['hq'])
        self.hqHarry.setTutorial(1)
        self.hqHarry.setHq(1)

        self.building = TutorialBuildingAI(
            self.air, self.zones['street'], self.zones['building'], 2, self.tutorialTom.getDoId())
        self.hq = HQBuildingAI(self.air, self.zones['street'], self.zones['hq'], 1)

        self.forceTransition('Introduction')

    def enterIntroduction(self):
        self.building.insideDoor.setDoorLock(FADoorCodes.TALK_TO_TOM)

    def exitIntroduction(self):
        self.building.insideDoor.setDoorLock(FADoorCodes.UNLOCKED)

    def enterBattle(self):
        self.suit = DistributedTutorialSuitAI(self.air)
        self.suit.generateWithRequired(self.zones['street'])

        self.building.door.setDoorLock(FADoorCodes.DEFEAT_FLUNKY_TOM)
        self.hq.door0.setDoorLock(FADoorCodes.DEFEAT_FLUNKY_HQ)
        self.hq.door1.setDoorLock(FADoorCodes.DEFEAT_FLUNKY_HQ)

    def exitBattle(self):
        if self.suit:
            self.suit.requestDelete()

    def enterHQ(self):
        self.building.door.setDoorLock(FADoorCodes.TALK_TO_HQ)
        self.hq.door0.setDoorLock(FADoorCodes.UNLOCKED)
        self.hq.door1.setDoorLock(FADoorCodes.UNLOCKED)
        self.hq.insideDoor0.setDoorLock(FADoorCodes.TALK_TO_HQ)
        self.hq.insideDoor1.setDoorLock(FADoorCodes.TALK_TO_HQ)

    def enterTunnel(self):
        npcDesc = NPCToons.NPCToonDict.get(20001)
        self.flippy = NPCToons.createNPC(self.air, 20001, npcDesc, self.zones['street'], 0)

        if simbase.air.wantHalloween:
            self.BlackCatManager = DistributedBlackCatMgrAI.DistributedBlackCatMgrAI(self.air)
            self.BlackCatManager.generateWithRequired(self.zones['street'])

        self.hq.insideDoor0.setDoorLock(FADoorCodes.WRONG_DOOR_HQ)
        self.hq.insideDoor1.setDoorLock(FADoorCodes.UNLOCKED)
        self.hq.door0.setDoorLock(FADoorCodes.GO_TO_PLAYGROUND)
        self.hq.door1.setDoorLock(FADoorCodes.GO_TO_PLAYGROUND)
        self.building.door.setDoorLock(FADoorCodes.GO_TO_PLAYGROUND)

    def exitTunnel(self):
        self.flippy.requestDelete()

    def enterCleanup(self):
        self.building.cleanup()
        self.hq.cleanup()
        self.tutorialTom.requestDelete()
        self.hqHarry.requestDelete()

        self.air.deallocateZone(self.zones['street'])
        self.air.deallocateZone(self.zones['building'])
        self.air.deallocateZone(self.zones['hq'])

        del self.air.tutorialManager.avId2fsm[self.avId]


class TutorialManagerAI(DistributedObjectAI):
    notify = directNotify.newCategory('TutorialManagerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)

        self.avId2fsm = {}

    def requestTutorial(self):
        avId = self.air.getAvatarIdFromSender()

        zones = {}
        zones['street'] = self.air.allocateZone()
        zones['building'] = self.air.allocateZone()
        zones['hq'] = self.air.allocateZone()

        self.avId2fsm[avId] = TutorialFSM(self.air, zones, avId)

        self.acceptOnce(self.air.getAvatarExitEvent(avId), self.__handleUnexpectedExit, extraArgs=[avId])
        self.d_enterTutorial(avId, ToontownGlobals.Tutorial, zones['street'], zones['building'], zones['hq'])

    def rejectTutorial(self):
        pass

    def requestSkipTutorial(self):
        avId = self.air.getAvatarIdFromSender()
        self.d_skipTutorialResponse(avId, 1)


        def handleTutorialSkipped(av):
            av.b_setTutorialAck(1)
            av.b_setQuests([[110, 1, 1000, 100, 1]])
            av.b_setQuestHistory([101])
            av.b_setRewardHistory(1, [])


        # We must wait for the avatar to be generated:
        self.acceptOnce('generate-%d' % avId, handleTutorialSkipped)

    def d_skipTutorialResponse(self, avId, allOk):
        self.sendUpdateToAvatarId(avId, 'skipTutorialResponse', [allOk])

    def d_enterTutorial(self, avId, branchZone, streetZone, shopZone, hqZone):
        self.sendUpdateToAvatarId(avId, 'enterTutorial', [branchZone, streetZone, shopZone, hqZone])

    def allDone(self):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)
        if av is not None:
            av.b_setTutorialAck(1)
        self.ignore(self.air.getAvatarExitEvent(avId))
        fsm = self.avId2fsm.get(avId)
        if fsm is not None:
            fsm.demand('Cleanup')
        else:
            self.air.writeServerEvent('suspicious', avId, issue='Attempted to exit a non-existent tutorial.')

    def toonArrived(self):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)
        if av is None:
            return

        if av.getTutorialAck():
            self.avId2fsm[avId].demand('Cleanup')
            self.air.writeServerEvent('suspicious', avId, issue='Attempted to enter a tutorial when it should be impossible.')
            return

        # Prepare the player for the tutorial:
        av.b_setQuests([])
        av.b_setQuestHistory([])
        av.b_setRewardHistory(0, [])
        av.b_setHp(15)
        av.b_setMaxHp(15)

        av.inventory.zeroInv(killUber=True)
        av.inventory.addItem(ToontownBattleGlobals.THROW_TRACK, 0)
        av.inventory.addItem(ToontownBattleGlobals.SQUIRT_TRACK, 0)
        av.d_setInventory(av.inventory.makeNetString())

        av.experience.zeroOutExp()
        av.d_setExperience(av.experience.makeNetString())

    def __handleUnexpectedExit(self, avId):
        fsm = self.avId2fsm.get(avId)
        if fsm is not None:
            fsm.demand('Cleanup')
