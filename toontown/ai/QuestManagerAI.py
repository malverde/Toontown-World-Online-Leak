from toontown.toon.DistributedNPCSpecialQuestGiverAI import DistributedNPCSpecialQuestGiverAI
from toontown.building import FADoorCodes
from otp.ai.MagicWordGlobal import *
from toontown.hood import ZoneUtil
from toontown.quest import Quests


QuestIdIndex = 0
QuestFromNpcIdIndex = 1
QuestToNpcIdIndex = 2
QuestRewardIdIndex = 3
QuestProgressIndex = 4


class QuestManagerAI:
    notify = directNotify.newCategory('QuestManagerAI')

    def __init__(self, air):
        self.air = air

    def requestInteract(self, avId, npc):
        # Get the avatar.
        av = self.air.doId2do.get(avId)
        if not av:
            return

        avQuestPocketSize = av.getQuestCarryLimit()
        avQuests = av.getQuests()

        needTrackTask = False
        fakeTier = 0

        avTrackProgress = av.getTrackProgress()
        if avTrackProgress[0] == -1:
            avQuestTier = av.getRewardTier()
            if avQuestTier < Quests.DG_TIER and avQuestTier > Quests.DD_TIER:
                fakeTier = Quests.DD_TIER
                needTrackTask = True
            elif avQuestTier < Quests.BR_TIER and avQuestTier > Quests.MM_TIER:
                fakeTier = Quests.MM_TIER
                needTrackTask = True
            elif avQuestTier < Quests.DL_TIER and avQuestTier > Quests.BR_TIER:
                fakeTier = Quests.BR_TIER
                needTrackTask = True

        # Iterate through their quests.
        for i in xrange(0, len(avQuests), 5):
            questDesc = avQuests[i:i + 5]
            questId, fromNpcId, toNpcId, rewardId, toonProgress = questDesc
            questClass = Quests.getQuest(questId)
            if questClass:
                completeStatus = questClass.getCompletionStatus(av, questDesc, npc)
            else:
                continue

            # If the quest is a DeliverGagQuest, add the gags.
            if isinstance(questClass, Quests.DeliverGagQuest):
                # Check if it's the required NPC.
                if npc.npcId == toNpcId:
                    # Add progress.
                    questList = []
                    progress = questClass.removeGags(av)

                    for i in xrange(0, len(avQuests), 5):
                        questDesc = avQuests[i:i + 5]
                        if questDesc[QuestIdIndex] == questId:
                            questDesc[QuestProgressIndex] += progress
                            if questDesc[QuestProgressIndex] >= questClass.getNumGags():
                                completeStatus = Quests.COMPLETE
                        questList.append(questDesc)
                    av.b_setQuests(questList)

                    if completeStatus != Quests.COMPLETE:
                        continue

            # If they've completed a quest.
            if completeStatus == Quests.COMPLETE:
                # ToonUp the toon to max health.
                av.toonUp(av.maxHp)

                # If it's a TrackChoiceQuest then present their track choices.
                if isinstance(questClass, Quests.TrackChoiceQuest):
                    npc.presentTrackChoice(avId, questId, questClass.getChoices())
                    break
                # If there is another part to this quest then give them that.
                if Quests.getNextQuest(questId, npc, av)[0] != Quests.NA:
                    self.nextQuest(av, npc, questId)
                    if avId in self.air.tutorialManager.avId2fsm:
                        self.air.tutorialManager.avId2fsm[avId].demand('Tunnel')
                    break
                else:
                    # The toon has completed this quest. Give them a reward!
                    npc.completeQuest(avId, questId, rewardId)
                    self.completeQuest(av, questId)
                break
        else:
            # They haven't completed any quests so we have to give them choices.
            # If they've got a full pouch then reject them.
            if (len(avQuests) == avQuestPocketSize*5):
                npc.rejectAvatar(avId)
                return
            elif isinstance(npc, DistributedNPCSpecialQuestGiverAI):
                # Don't display choices. Force a choice.
                self.tutorialQuestChoice(avId, npc)
                return
            else:
                #Present quest choices.
                if needTrackTask:
                    choices = self.npcGiveTrackChoice(av, fakeTier)
                else:
                    choices = self.avatarQuestChoice(av, npc)
                if choices != []:
                    npc.presentQuestChoice(avId, choices)
                else:
                    npc.rejectAvatar(avId)

    def npcGiveTrackChoice(self, av, tier):
        trackQuest = Quests.chooseTrackChoiceQuest(tier, av)
        return [(trackQuest, 400, Quests.ToonHQ)]

    def avatarQuestChoice(self, av, npc):
        # Get the best quests for an avatar/npc.
        return Quests.chooseBestQuests(av.getRewardTier(), npc, av)

    def avatarChoseQuest(self, avId, npc, questId, rewardId, toNpcId):
        # Get the avatar.
        av = self.air.doId2do.get(avId)
        if not av:
            return

        # Get the npcIds
        fromNpcId = npc.npcId
        if toNpcId == 0:
            toNpcId = Quests.getQuestToNpcId(questId)

        # Add the quest to the avatars list.
        transformedRewardId = Quests.transformReward(rewardId, av)
        av.addQuest([questId, fromNpcId, toNpcId, rewardId, 0], transformedRewardId)

        # Remove the tasks for timeout.
        taskMgr.remove(npc.uniqueName('clearMovie'))

        # Assign the quest.
        npc.assignQuest(avId, questId, rewardId, toNpcId)

    def avatarChoseTrack(self, avId, npc, pendingTrackQuest, trackId):
        # Get the avatar.
        av = self.air.doId2do.get(avId)
        if not av:
            return

        # Remove the tasks for timeout.
        taskMgr.remove(npc.uniqueName('clearMovie'))

        # Show the completion movie and remove the task.
        npc.completeQuest(avId, pendingTrackQuest, Quests.getRewardIdFromTrackId(trackId))
        self.completeQuest(av, pendingTrackQuest)

        # Set their track their working on.
        av.b_setTrackProgress(trackId, 0)

    def avatarCancelled(self, npcId):
        # Get the NPC.
        npc = self.air.doId2do.get(npcId)
        if not npc:
            return

        # Remove the task for timeout.
        taskMgr.remove(npc.uniqueName('clearMovie'))

    def nextQuest(self, av, npc, questId):
        # Get the next QuestId and toNpcId.
        nextQuestId, toNpcId = Quests.getNextQuest(questId, npc, av)

        # Get the avatars current quests.
        avQuests = av.getQuests()
        questList = []

        # Iterate through their current quests.
        for i in xrange(0, len(avQuests), 5):
            questDesc = avQuests[i:i + 5]

            if questDesc[QuestIdIndex] == questId:
                questDesc[QuestIdIndex] = nextQuestId
                questDesc[QuestToNpcIdIndex] = toNpcId
                questDesc[QuestProgressIndex] = 0
            questList.append(questDesc)

        # Show the quest movie and set their quests.
        npc.incompleteQuest(av.doId, nextQuestId, Quests.QUEST, toNpcId)
        av.b_setQuests(questList)

    def completeQuest(self, av, completeQuestId):
        #Get the avatars current quests.
        avQuests = av.getQuests()

        # Iterate through their current quests.
        for i in xrange(0, len(avQuests), 5):
            questDesc = avQuests[i:i + 5]
            questId, fromNpcId, toNpcId, rewardId, toonProgress = questDesc
            questClass = Quests.getQuest(questId)

            if questId == completeQuestId:
                av.removeQuest(questId)
                self.giveReward(av, questId, rewardId)
                self.avatarConsiderProgressTier(av)
                break

    def giveReward(self, av, questId, rewardId):
        # Give the reward.
        rewardClass = Quests.getReward(rewardId)
        if rewardClass is None:
            self.notify.warning('rewardClass was None for rewardId: %s.' % rewardId)
        else:
            rewardClass.sendRewardAI(av)

        # Add the rewardId to the avatars rewardHistory.
        rewardTier, rewardHistory = av.getRewardHistory()
        transformedRewardId = Quests.transformReward(rewardId, av)
        if transformedRewardId != rewardId:
            rewardHistory.append(rewardId)

        av.b_setRewardHistory(rewardTier, rewardHistory)

    def avatarConsiderProgressTier(self, av):
        # Get the avatars current tier.
        currentTier = av.getRewardTier()

        # Check if they have all required rewards.
        if Quests.avatarHasAllRequiredRewards(av, currentTier):
            if currentTier != Quests.ELDER_TIER:
                currentTier += 1
            av.b_setRewardHistory(currentTier, [])

    def tutorialQuestChoice(self, avId, npc):
        # Get the avatar.
        av = self.air.doId2do.get(avId)
        if not av:
            return

        # Get the possible quest choices and force the player to choose it.
        choices = self.avatarQuestChoice(av, npc)
        quest = choices[0]

        self.avatarChoseQuest(avId, npc, quest[0], quest[1], 0)

        # Are we in the tutorial speaking to Tutorial Tom?
        if avId in self.air.tutorialManager.avId2fsm:
            if av.getRewardHistory()[0] == 0:
                self.air.tutorialManager.avId2fsm[avId].demand('Battle')

    def toonRodeTrolleyFirstTime(self, av):
        # Toon played a minigame.
        self.toonPlayedMinigame(av, [])

    def toonPlayedMinigame(self, av, toons):
        # Get the avatars current quests.
        avQuests = av.getQuests()
        questList = []

        # Iterate through their current quests.
        for i in xrange(0, len(avQuests), 5):
            questDesc = avQuests[i : i + 5]
            questClass = Quests.getQuest(questDesc[QuestIdIndex])
            if isinstance(questClass, Quests.TrolleyQuest):
                questDesc[QuestProgressIndex] = 1
            questList.append(questDesc)

        av.b_setQuests(questList)

    def toonMadeFriend(self, avId):
        # Get the avatar.
        av = self.air.doId2do.get(avId)
        if not av:
            return

        # Get the avatars current quests.
        avQuests = av.getQuests()
        questList = []

        # Iterate through their current quests.
        for i in xrange(0, len(avQuests), 5):
            questDesc = avQuests[i : i + 5]
            questClass = Quests.getQuest(questDesc[QuestIdIndex])
            if isinstance(questClass, Quests.FriendQuest):
                questDesc[QuestProgressIndex] = 1
            questList.append(questDesc)

        av.b_setQuests(questList)

    def toonUsedPhone(self, avId):
        # Get the avatar.
        av = self.air.doId2do.get(avId)
        if not av:
            return

        # Get the avatars current quests.
        avQuests = av.getQuests()
        questList = []

        # Iterate through their current quests.
        for i in xrange(0, len(avQuests), 5):
            questDesc = avQuests[i : i + 5]
            questClass = Quests.getQuest(questDesc[QuestIdIndex])
            if isinstance(questClass, Quests.PhoneQuest):
                questDesc[QuestProgressIndex] += 1
            questList.append(questDesc)

        av.b_setQuests(questList)

    def toonCaughtFishingItem(self, av):
        # Get the avatars current quests.
        avQuests = av.getQuests()
        fishingItem = -1
        questList = []

        # Iterate through their current quests.
        for i in xrange(0, len(avQuests), 5):
            questDesc = avQuests[i : i + 5]
            questClass = Quests.getQuest(questDesc[QuestIdIndex])
            if fishingItem != -1:
                questList.append(questDesc)
                continue
            if isinstance(questClass, Quests.RecoverItemQuest):
                if not hasattr(questClass, 'getItem'):
                    questList.append(questDesc)
                    continue
                if questClass.getHolder() == Quests.AnyFish:
                    if not questClass.getCompletionStatus(av, questDesc) == Quests.COMPLETE:
                        baseChance = questClass.getPercentChance()
                        amountRemaining = questClass.getNumItems() - questDesc[QuestProgressIndex]
                        chance = Quests.calcRecoverChance(amountRemaining, baseChance)
                        if chance >= baseChance:
                            questDesc[QuestProgressIndex] += 1
                            fishingItem = questClass.getItem()
            questList.append(questDesc)

        av.b_setQuests(questList)
        return fishingItem

    def hasTailorClothingTicket(self, av, npc):
        # Get the avatars current quests.
        avQuests = av.getQuests()

        # Iterate through their current quests.
        for i in xrange(0, len(avQuests), 5):
            questDesc = avQuests[i : i + 5]
            questClass = Quests.getQuest(questDesc[QuestIdIndex])
            if isinstance(questClass, Quests.DeliverItemQuest):
                if questClass.getCompletionStatus(av, questDesc, npc) == Quests.COMPLETE:
                    # They have a clothing ticket.
                    return 1
        return 0

    def removeClothingTicket(self, av, npc):
        # Get the avatars current quests.
        avQuests = av.getQuests()

        # Iterate through their current quests.
        for i in xrange(0, len(avQuests), 5):
            questDesc = avQuests[i : i + 5]
            questClass = Quests.getQuest(questDesc[QuestIdIndex])
            if isinstance(questClass, Quests.DeliverItemQuest):
                if questClass.getCompletionStatus(av, questDesc, npc) == Quests.COMPLETE:
                    av.removeQuest(questDesc[QuestIdIndex])
                    break

    def recoverItems(self, av, suitsKilled, taskZoneId):
        # Get the avatars current quests.
        avQuests = av.getQuests()
        questList = []
        recoveredItems = []
        unrecoveredItems = []
        taskZoneId = ZoneUtil.getBranchZone(taskZoneId)

        # Iterate through the avatars current quests.
        for i in xrange(0, len(avQuests), 5):
            questDesc = avQuests[i : i + 5]
            questClass = Quests.getQuest(questDesc[QuestIdIndex])

            # Check if the Quest isnt already complete
            if questClass.getCompletionStatus(av, questDesc) == Quests.INCOMPLETE:

                # Check if we are dealing with a RecoverItemQuest
                if isinstance(questClass, Quests.RecoverItemQuest):

                    # Iterate through all the Cogs that were killed in the battle
                    for suit in suitsKilled:

                        # Because the RecoveItemQuest class doesn't have a
                        # function to see if a Cog counts. We need to manually
                        # check if the Cog is valid for the Quest
                        if (questClass.getHolder() == Quests.Any) or \
                            (questClass.getHolderType() == 'type' and \
                            questClass.getHolder() == suit['type']) or \
                            (questClass.getHolderType() == 'track' and \
                            questClass.getHolder() == suit['track']) or \
                            (questClass.getHolderType() == 'level' and \
                            questClass.getHolder() <= suit['level']):

                            # It looks like the Cog was valid. Lets see if they
                            # found what they were looking for.
                            baseChance = questClass.getPercentChance()
                            amountRemaining = questClass.getNumItems() - questDesc[QuestProgressIndex]
                            chance = Quests.calcRecoverChance(amountRemaining, baseChance)

                            # They found it! Give them their reward!
                            if chance >= baseChance:
                                questDesc[QuestProgressIndex] += 1
                                recoveredItems.append(questClass.getItem())

                            # Better luck next time :(
                            else:
                                unrecoveredItems.append(questClass.getItem())

            questList.append(questDesc)

        av.b_setQuests(questList)

        return (recoveredItems, unrecoveredItems)

    def toonKilledBuilding(self, av, type, difficulty, floors, zoneId, activeToons):
        # Get the avatars current quests.
        avQuests = av.getQuests()
        questList = []
        zoneId = ZoneUtil.getBranchZone(zoneId)

        # Iterate through the avatars current quests.
        for i in xrange(0, len(avQuests), 5):
            questDesc = avQuests[i : i + 5]
            questClass = Quests.getQuest(questDesc[QuestIdIndex])
            if questClass.getCompletionStatus(av, questDesc) == Quests.INCOMPLETE:
                if isinstance(questClass, Quests.BuildingQuest):
                    if questClass.isLocationMatch(zoneId):
                        if questClass.doesBuildingTypeCount(type):
                            if questClass.doesBuildingCount(av, activeToons):
                                if floors >= questClass.getNumFloors():
                                    questDesc[QuestProgressIndex] += 1
            questList.append(questDesc)

        av.b_setQuests(questList)

    def toonDefeatedFactory(self, av, factoryId, activeVictors):
        # Get the avatars current quests.
        avQuests = av.getQuests()
        questList = []

        # Iterate through the avatars current quests.
        for i in xrange(0, len(avQuests), 5):
            questDesc = avQuests[i : i + 5]
            questClass = Quests.getQuest(questDesc[QuestIdIndex])
            if isinstance(questClass, Quests.FactoryQuest):
                if questClass.doesFactoryCount(av, factoryId, activeVictors):
                    questDesc[QuestProgressIndex] += 1
            questList.append(questDesc)

        av.b_setQuests(questList)

    def toonDefeatedMint(self, av, mintId, activeVictors):
        # Get the avatars current quests.
        avQuests = av.getQuests()
        questList = []

        # Iterate through the avatars current quests.
        for i in xrange(0, len(avQuests), 5):
            questDesc = avQuests[i : i + 5]
            questClass = Quests.getQuest(questDesc[QuestIdIndex])
            if isinstance(questClass, Quests.MintQuest):
                if questClass.doesMintCount(av, mintId, activeVictors):
                    questDesc[QuestProgressIndex] += 1
            questList.append(questDesc)

        av.b_setQuests(questList)

    def toonDefeatedStage(self, av, stageId, activeVictors):
        pass

    def toonKilledCogs(self, av, suitsKilled, zoneId, activeToonList):
        # Get the avatar's current quests.
        avQuests = av.getQuests()
        questList = []

        # Make a list of the activeToonDoIds
        activeToonDoIds = [toon.doId for toon in activeToonList if not None]

        # Iterate through the avatar's current quests.
        for i in xrange(0, len(avQuests), 5):
            questDesc = avQuests[i : i + 5]
            questClass = Quests.getQuest(questDesc[QuestIdIndex])

            # Check if they are doing a cog quest
            if isinstance(questClass, Quests.CogQuest):

                # Check if the cog counts...
                for suit in suitsKilled:
                    if questClass.doesCogCount(av.doId, suit, zoneId, activeToonDoIds):

                        # Looks like the cog counts!
                        if questClass.getCompletionStatus(av, questDesc) != Quests.COMPLETE:
                            questDesc[QuestProgressIndex] += 1

            # Add the quest to the questList
            questList.append(questDesc)

        # Update the avatar's quests
        av.b_setQuests(questList)


@magicWord(category=CATEGORY_PROGRAMMER, types=[str, int, int])
def quests(command, arg0=0, arg1=0):
    target = spellbook.getTarget()
    currQuests = target.getQuests()
    currentQuestIds = []

    for i in xrange(0, len(currQuests), 5):
        currentQuestIds.append(currQuests[i])

    pocketSize = target.getQuestCarryLimit()
    carrying = len(currQuests) / 5
    canCarry = False

    if (carrying < pocketSize):
        canCarry = True

    if command == 'clear':
        target.b_setQuests([])
        return 'Cleared quests'
    elif command == 'clearHistory':
        target.d_setQuestHistory([])
        return 'Cleared quests history'
    elif command == 'add':
        if arg0:
            if canCarry:
                if arg0 in Quests.QuestDict.keys():
                    return 'Added QuestID %s'%(arg0)
                else:
                    return 'Invalid QuestID %s'%(arg0)
            else:
                return 'Cannot take anymore quests'
        else:
            return 'add needs 1 argument.'
    elif command == 'remove':
        if arg0:
            if arg0 in currentQuestIds:
                target.removeQuest(arg0)
                return 'Removed QuestID %s'%(arg0)
            elif arg0 < pocketSize and arg0 > 0:
                if len(currentQuestIds) <= arg0:
                    questIdToRemove = currentQuestIds[arg0 - 1]
                    target.removeQuest(questIdToRemove)
                    return 'Removed quest from slot %s'%(arg0)
                else:
                    return 'Invalid quest slot'
            else:
                return 'Cannot remove quest %s'%(arg0)
        else:
            return 'remove needs 1 argument.'
    elif command == 'list':
        if arg0:
            if arg0 > 0 and arg0 <= pocketSize:
                start = (arg0 -1) * 5
                questDesc = currQuests[start : start + 5]
                return 'QuestDesc in slot %s: %s.'%(arg0, questDesc)
            else:
                return 'Invalid quest slot %s.'%(arg0)
        else:
            return 'CurrentQuests: %s'%(currentQuestIds)
    elif command == 'bagSize':
        if arg0 > 0 and arg0 < 5:
            target.b_setQuestCarryLimit(arg0)
            return 'Set carry limit to %s'%(arg0)
        else:
            return 'Argument 0 must be between 1 and 4.'
    elif command == 'progress':
        if arg0 and arg1:
            if arg0 > 0 and arg0 <= pocketSize:
                questList = []
                wantedQuestId = currentQuestIds[arg0 - 1]

                for i in xrange(0, len(currQuests), 5):
                    questDesc = currQuests[i : i + 5]

                    if questDesc[0] == wantedQuestId:
                        questDesc[4] = arg1

                    questList.append(questDesc)

                target.b_setQuests(questList)
                return 'Set quest slot %s progress to %s'%(arg0, arg1)
            elif arg0 in Quests.QuestDict.keys():
                if arg0 in currentQuestIds:
                    questList = []

                    for i in xrange(0, len(currQuests), 5):
                        questDesc = currQuests[i : i + 5]

                        if questDesc[0] == arg0:
                            questDesc[4] = arg1

                        questList.append(questDesc)

                    target.b_setQuests(questList)
                    return 'Set QuestID %s progress to %s'%(arg0, arg1)
                else:
                    return 'Cannot progress QuestID: %s.'%(arg0)
            else:
                return 'Invalid quest or slot id'
        else:
            return 'progress needs 2 arguments.'
    elif command == 'tier':
        if arg0:
            target.b_setRewardHistory(arg0, target.getRewardHistory()[1])
            return 'Set tier to %s'%(arg0)
        else:
            return 'tier needs 1 argument.'
    else:
        return 'Invalid first argument.'
