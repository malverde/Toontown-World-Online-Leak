from direct.actor.Actor import Actor
from direct.directnotify import DirectNotifyGlobal
from direct.distributed import ClockDelta
from direct.showbase.PythonUtil import recordCreationStack
from pandac.PandaModules import *
import random

from otp.ai import MagicWordManager
from otp.ai.MagicWordGlobal import *
from otp.avatar.ShadowCaster import ShadowCaster
from otp.otpbase import OTPGlobals
from otp.otpbase import OTPLocalizer
from otp.otpbase import OTPRender
from toontown.chat.ChatGlobals import *
from toontown.nametag import NametagGlobals
from toontown.nametag.NametagGroup import NametagGroup


teleportNotify = DirectNotifyGlobal.directNotify.newCategory('Teleport')
teleportNotify.showTime = True
if config.GetBool('want-teleport-debug', 1):
    teleportNotify.setDebug(1)

def reconsiderAllUnderstandable():
    for av in Avatar.ActiveAvatars:
        av.considerUnderstandable()


class Avatar(Actor, ShadowCaster):
    notify = directNotify.newCategory('Avatar')
    ActiveAvatars = []
    ManagesNametagAmbientLightChanged = False

    def __init__(self, other = None):
        self.name = ''
        try:
            self.Avatar_initialized
            return
        except:
            self.Avatar_initialized = 1

        Actor.__init__(self, None, None, other, flattenable=0, setFinal=1)
        ShadowCaster.__init__(self)
        self.__font = OTPGlobals.getInterfaceFont()
        self.soundChatBubble = None
        self.avatarType = ''
        self.nametagNodePath = None
        self.__nameVisible = 1
        self.nametag = NametagGroup()
        self.nametag.setAvatar(self)
        interfaceFont = OTPGlobals.getInterfaceFont()
        self.nametag.setFont(interfaceFont)
        self.nametag.setChatFont(interfaceFont)
        self.nametag3d = self.attachNewNode('nametag3d')
        self.nametag3d.setTag('cam', 'nametag')
        self.nametag3d.setLightOff()
        if self.ManagesNametagAmbientLightChanged:
            self.acceptNametagAmbientLightChange()
        OTPRender.renderReflection(False, self.nametag3d, 'otp_avatar_nametag', None)
        self.getGeomNode().showThrough(OTPRender.ShadowCameraBitmask)
        self.nametag3d.hide(OTPRender.ShadowCameraBitmask)
        self.collTube = None
        self.battleTube = None
        self.scale = 1.0
        self.nametagScale = 1.0
        self.height = 0.0
        self.battleTubeHeight = 0.0
        self.battleTubeRadius = 0.0
        self.style = None
        self.commonChatFlags = 0
        self.understandable = 1
        self.setPlayerType(NametagGlobals.CCNormal)
        self.ghostMode = 0
        self.__chatParagraph = None
        self.__chatMessage = None
        self.__chatFlags = 0
        self.__chatPageNumber = None
        self.__chatAddressee = None
        self.__chatDialogueList = []
        self.__chatSet = 0
        self.__chatLocal = 0
        self.__chatQuitButton = False
        self.__currentDialogue = None
        self.whitelistChatFlags = 0

    def delete(self):
        try:
            self.Avatar_deleted
        except:
            self.deleteNametag3d()
            Actor.cleanup(self)
            if self.ManagesNametagAmbientLightChanged:
                self.ignoreNametagAmbientLightChange()
            self.Avatar_deleted = 1
            del self.__font
            del self.style
            del self.soundChatBubble
            self.nametag.destroy()
            del self.nametag
            self.nametag3d.removeNode()
            ShadowCaster.delete(self)
            Actor.delete(self)

    def acceptNametagAmbientLightChange(self):
        self.accept('nametagAmbientLightChanged', self.nametagAmbientLightChanged)

    def ignoreNametagAmbientLightChange(self):
        self.ignore('nametagAmbientLightChanged')

    def isLocal(self):
        return 0

    def isPet(self):
        return False

    def isProxy(self):
        return False

    def setPlayerType(self, playerType):
        self.playerType = playerType
        if not hasattr(self, 'nametag'):
            self.notify.warning('no nametag attributed, but would have been used.')
            return
        if self.isUnderstandable():
            nametagColor = NametagGlobals.NametagColors[self.playerType]
            self.nametag.setNametagColor(nametagColor)
            chatColor = NametagGlobals.ChatColors[self.playerType]
            self.nametag.setChatColor(chatColor)
        else:
            nametagColor = NametagGlobals.NametagColors[NametagGlobals.CCNoChat]
            self.nametag.setNametagColor(nametagColor)
            chatColor = NametagGlobals.ChatColors[NametagGlobals.CCNoChat]
            self.nametag.setChatColor(chatColor)
        self.nametag.updateAll()

    def setCommonChatFlags(self, commonChatFlags):
        self.commonChatFlags = commonChatFlags
        self.considerUnderstandable()
        if self == base.localAvatar:
            reconsiderAllUnderstandable()

    def setWhitelistChatFlags(self, whitelistChatFlags):
        self.whitelistChatFlags = whitelistChatFlags
        self.considerUnderstandable()
        if self == base.localAvatar:
            reconsiderAllUnderstandable()

    def considerUnderstandable(self):
        if self.playerType in (NametagGlobals.CCNormal, NametagGlobals.CCFreeChat, NametagGlobals.CCSpeedChat):
            self.setPlayerType(NametagGlobals.CCSpeedChat)
        if hasattr(base, 'localAvatar') and (self == base.localAvatar):
            self.understandable = 1
            self.setPlayerType(NametagGlobals.CCFreeChat)
        elif self.playerType == NametagGlobals.CCSuit:
            self.understandable = 1
            self.setPlayerType(NametagGlobals.CCSuit)
        elif self.playerType not in (NametagGlobals.CCNormal, NametagGlobals.CCFreeChat, NametagGlobals.CCSpeedChat):
            self.understandable = 1
            self.setPlayerType(NametagGlobals.CCNoChat)
        elif hasattr(base, 'localAvatar') and self.commonChatFlags & base.localAvatar.commonChatFlags & OTPGlobals.CommonChat:
            self.understandable = 1
            self.setPlayerType(NametagGlobals.CCFreeChat)
        elif self.commonChatFlags & OTPGlobals.SuperChat:
            self.understandable = 1
            self.setPlayerType(NametagGlobals.CCFreeChat)
        elif hasattr(base, 'localAvatar') and base.localAvatar.commonChatFlags & OTPGlobals.SuperChat:
            self.understandable = 1
            self.setPlayerType(NametagGlobals.CCFreeChat)
        elif base.cr.getFriendFlags(self.doId) & OTPGlobals.FriendChat:
            self.understandable = 1
            self.setPlayerType(NametagGlobals.CCFreeChat)
        elif base.cr.playerFriendsManager.findPlayerIdFromAvId(self.doId) is not None:
            playerInfo = base.cr.playerFriendsManager.findPlayerInfoFromAvId(self.doId)
            if playerInfo.openChatFriendshipYesNo:
                self.understandable = 1
                nametagColor = NametagGlobals.NametagColors[NametagGlobals.CCFreeChat]
                self.nametag.setNametagColor(nametagColor)
                chatColor = NametagGlobals.ChatColors[NametagGlobals.CCFreeChat]
                self.nametag.setChatColor(chatColor)
                self.nametag.updateAll()
            elif playerInfo.isUnderstandable():
                self.understandable = 1
            else:
                self.understandable = 0
        elif hasattr(base, 'localAvatar') and self.whitelistChatFlags & base.localAvatar.whitelistChatFlags:
            self.understandable = 1
        else:
            self.understandable = 0
        if not hasattr(self, 'nametag'):
            self.notify.warning('no nametag attributed, but would have been used')
        else:
            nametagColor = NametagGlobals.NametagColors[self.playerType]
            self.nametag.setNametagColor(nametagColor)
            chatColor = NametagGlobals.ChatColors[self.playerType]
            self.nametag.setChatColor(chatColor)
            self.nametag.updateAll()

    def isUnderstandable(self):
        return self.understandable

    def setDNAString(self, dnaString):
        pass

    def setDNA(self, dna):
        pass

    def getAvatarScale(self):
        return self.scale

    def setAvatarScale(self, scale):
        if self.scale != scale:
            self.scale = scale
            self.getGeomNode().setScale(scale)
            self.setHeight(self.height)

    def getNametagScale(self):
        return self.nametagScale

    def setNametagScale(self, scale):
        self.nametagScale = scale
        self.nametag3d.setScale(scale)

    def adjustNametag3d(self, parentScale = 1.0):
        self.nametag3d.setPos(0, 0, self.height + 0.5)

    def getHeight(self):
        return self.height

    def setHeight(self, height):
        self.height = height
        self.adjustNametag3d()
        if self.collTube:
            self.collTube.setPointB(0, 0, height - self.getRadius())
            if self.collNodePath:
                self.collNodePath.forceRecomputeBounds()
        if self.battleTube:
            self.battleTube.setPointB(0, 0, height - self.getRadius())

    def getRadius(self):
        return OTPGlobals.AvatarDefaultRadius

    def getName(self):
        return self.name

    def getType(self):
        return self.avatarType

    def setName(self, name):
        if hasattr(self, 'isDisguised'):
            if self.isDisguised:
                return
        self.name = name
        if hasattr(self, 'nametag'):
            self.nametag.setText(name)

    def setDisplayName(self, str):
        if hasattr(self, 'isDisguised'):
            if self.isDisguised:
                return
        self.nametag.setText(str)

    def getFont(self):
        return self.__font

    def setFont(self, font):
        self.__font = font
        self.nametag.setFont(font)
        self.nametag.setChatFont(font)

    def getStyle(self):
        return self.style

    def setStyle(self, style):
        self.style = style

    def getDialogueArray(self):
        return None

    def playCurrentDialogue(self, dialogue, chatFlags, interrupt = 1):
        if interrupt and self.__currentDialogue is not None:
            self.__currentDialogue.stop()
        self.__currentDialogue = dialogue
        if dialogue:
            base.playSfx(dialogue, node=self)
        elif chatFlags & CFSpeech != 0 and self.nametag.getNumChatPages() > 0:
            self.playDialogueForString(self.nametag.getChatText())
            if self.soundChatBubble != None:
                base.playSfx(self.soundChatBubble, node=self)

    def playDialogueForString(self, chatString):
        searchString = chatString.lower()
        if searchString.find(OTPLocalizer.DialogSpecial) >= 0:
            type = 'special'
        elif searchString.find(OTPLocalizer.DialogExclamation) >= 0:
            type = 'exclamation'
        elif searchString.find(OTPLocalizer.DialogQuestion) >= 0:
            type = 'question'
        elif random.randint(0, 1):
            type = 'statementA'
        else:
            type = 'statementB'
        stringLength = len(chatString)
        if stringLength <= OTPLocalizer.DialogLength1:
            length = 1
        elif stringLength <= OTPLocalizer.DialogLength2:
            length = 2
        elif stringLength <= OTPLocalizer.DialogLength3:
            length = 3
        else:
            length = 4
        self.playDialogue(type, length)

    def playDialogue(self, type, length):
        dialogueArray = self.getDialogueArray()
        if dialogueArray == None:
            return
        sfxIndex = None
        if type == 'statementA' or type == 'statementB':
            if length == 1:
                sfxIndex = 0
            elif length == 2:
                sfxIndex = 1
            elif length >= 3:
                sfxIndex = 2
        elif type == 'question':
            sfxIndex = 3
        elif type == 'exclamation':
            sfxIndex = 4
        elif type == 'special':
            sfxIndex = 5
        else:
            notify.error('unrecognized dialogue type: ', type)
        if sfxIndex != None and sfxIndex < len(dialogueArray) and dialogueArray[sfxIndex] != None:
            base.playSfx(dialogueArray[sfxIndex], node=self)
        return

    def getDialogueSfx(self, type, length):
        retval = None
        dialogueArray = self.getDialogueArray()
        if dialogueArray == None:
            return
        sfxIndex = None
        if type == 'statementA' or type == 'statementB':
            if length == 1:
                sfxIndex = 0
            elif length == 2:
                sfxIndex = 1
            elif length >= 3:
                sfxIndex = 2
        elif type == 'question':
            sfxIndex = 3
        elif type == 'exclamation':
            sfxIndex = 4
        elif type == 'special':
            sfxIndex = 5
        else:
            notify.error('unrecognized dialogue type: ', type)
        if sfxIndex != None and sfxIndex < len(dialogueArray) and dialogueArray[sfxIndex] != None:
            retval = dialogueArray[sfxIndex]
        return retval

    def setChatAbsolute(self, chatString, chatFlags, dialogue=None, interrupt=1):
        self.clearChat()

        if chatFlags & CFQuicktalker:
            self.nametag.setChatType(NametagGlobals.SPEEDCHAT)
        else:
            self.nametag.setChatType(NametagGlobals.CHAT)

        if chatFlags & CFThought:
            self.nametag.setChatBalloonType(NametagGlobals.THOUGHT_BALLOON)
        else:
            self.nametag.setChatBalloonType(NametagGlobals.CHAT_BALLOON)

        if chatFlags & CFPageButton:
            self.nametag.setChatButton(NametagGlobals.pageButton)
        else:
            self.nametag.setChatButton(NametagGlobals.noButton)

        if chatFlags & CFReversed:
            self.nametag.setChatReversed(True)
        else:
            self.nametag.setChatReversed(False)

        self.nametag.setChatText(chatString, timeout=(chatFlags & CFTimeout))
        self.playCurrentDialogue(dialogue, chatFlags, interrupt)

    def setChatMuted(self, chatString, chatFlags, dialogue = None, interrupt = 1, quiet = 0):
        pass

    def displayTalk(self, chatString):
        if not base.cr.avatarFriendsManager.checkIgnored(self.doId):
            self.clearChat()
            self.nametag.setChatType(NametagGlobals.CHAT)
            self.nametag.setChatButton(NametagGlobals.noButton)
            if base.talkAssistant.isThought(chatString):
                chatString = base.talkAssistant.removeThoughtPrefix(chatString)
                self.nametag.setChatBalloonType(NametagGlobals.THOUGHT_BALLOON)
                self.nametag.setChatText(chatString)
            else:
                self.nametag.setChatBalloonType(NametagGlobals.CHAT_BALLOON)
                self.nametag.setChatText(chatString, timeout=True)

    def clearChat(self):
        self.nametag.clearChatText()

    def isInView(self):
        pos = self.getPos(camera)
        eyePos = Point3(pos[0], pos[1], pos[2] + self.getHeight())
        return base.camNode.isInView(eyePos)

    def getNameVisible(self):
        return self.__nameVisible

    def setNameVisible(self, bool):
        self.__nameVisible = bool
        if bool:
            self.showName()
        if not bool:
            self.hideName()

    def hideName(self):
        nametag3d = self.nametag.getNametag3d()
        nametag3d.hideNametag()
        nametag3d.showChat()
        nametag3d.showThought()
        nametag3d.update()

    def showName(self):
        if self.__nameVisible and (not self.ghostMode):
            nametag3d = self.nametag.getNametag3d()
            nametag3d.showNametag()
            nametag3d.showChat()
            nametag3d.showThought()
            nametag3d.update()

    def hideNametag2d(self):
        nametag2d = self.nametag.getNametag2d()
        nametag2d.hideNametag()
        nametag2d.hideChat()
        nametag2d.update()

    def showNametag2d(self):
        nametag2d = self.nametag.getNametag2d()
        if not self.ghostMode:
            nametag2d.showNametag()
            nametag2d.showChat()
        else:
            nametag2d.hideNametag()
            nametag2d.hideChat()
        nametag2d.update()

    def hideNametag3d(self):
        nametag3d = self.nametag.getNametag3d()
        nametag3d.hideNametag()
        nametag3d.hideChat()
        nametag3d.hideThought()
        nametag3d.update()

    def showNametag3d(self):
        nametag3d = self.nametag.getNametag3d()
        if self.__nameVisible and (not self.ghostMode):
            nametag3d.showNametag()
            nametag3d.showChat()
            nametag3d.showThought()
        else:
            nametag3d.hideNametag()
            nametag3d.hideChat()
            nametag3d.hideThought()
        nametag3d.update()

    def setPickable(self, flag):
        self.nametag.setActive(flag)

    def clickedNametag(self):
        MagicWordManager.lastClickedNametag = self
        if self.nametag.getChatText() and self.nametag.hasChatButton():
            self.advancePageNumber()
        elif self.nametag.getActive():
            messenger.send('clickedNametag', [self])

    def setPageChat(self, addressee, paragraph, message, quitButton,
                    extraChatFlags=None, dialogueList=[], pageButton=True):
        self.__chatAddressee = addressee
        self.__chatPageNumber = None
        self.__chatParagraph = paragraph
        self.__chatMessage = message
        self.__chatFlags = CFSpeech
        if extraChatFlags is not None:
            self.__chatFlags |= extraChatFlags
        self.__chatDialogueList = dialogueList
        self.__chatSet = 0
        self.__chatLocal = 0
        self.__updatePageChat()
        if addressee == base.localAvatar.doId:
            if pageButton:
                self.__chatFlags |= CFPageButton
            self.__chatQuitButton = quitButton
            self.b_setPageNumber(self.__chatParagraph, 0)

    def setLocalPageChat(self, message, quitButton, extraChatFlags=None,
                         dialogueList=[]):
        self.__chatAddressee = base.localAvatar.doId
        self.__chatPageNumber = None
        self.__chatParagraph = None
        self.__chatMessage = message
        self.__chatFlags = CFSpeech
        if extraChatFlags is not None:
            self.__chatFlags |= extraChatFlags
        self.__chatDialogueList = dialogueList
        self.__chatSet = 1
        self.__chatLocal = 1
        self.__chatFlags |= CFPageButton
        self.__chatQuitButton = quitButton
        if len(dialogueList) > 0:
            dialogue = dialogueList[0]
        else:
            dialogue = None
        self.clearChat()
        self.setChatAbsolute(message, self.__chatFlags, dialogue)
        self.setPageNumber(None, 0)

    def setPageNumber(self, paragraph, pageNumber, timestamp=None):
        if timestamp is None:
            elapsed = 0.0
        else:
            elapsed = ClockDelta.globalClockDelta.localElapsedTime(timestamp)
        self.__chatPageNumber = [paragraph, pageNumber]
        self.__updatePageChat()
        if hasattr(self, 'uniqueName'):
            if pageNumber >= 0:
                messenger.send(self.uniqueName('nextChatPage'), [pageNumber, elapsed])
            else:
                messenger.send(self.uniqueName('doneChatPage'), [elapsed])
        elif pageNumber >= 0:
            messenger.send('nextChatPage', [pageNumber, elapsed])
        else:
            messenger.send('doneChatPage', [elapsed])

    def advancePageNumber(self):
        if (self.__chatAddressee == base.localAvatar.doId) and (
            self.__chatPageNumber is not None) and (
            self.__chatPageNumber[0] == self.__chatParagraph):
            pageNumber = self.__chatPageNumber[1]
            if pageNumber >= 0:
                pageNumber += 1
                if pageNumber >= self.nametag.getNumChatPages():
                    pageNumber = -1
                if self.__chatQuitButton:
                    if pageNumber == self.nametag.getNumChatPages() - 1:
                        self.nametag.setChatButton(NametagGlobals.quitButton)
                if self.__chatLocal:
                    self.setPageNumber(self.__chatParagraph, pageNumber)
                else:
                    self.b_setPageNumber(self.__chatParagraph, pageNumber)

    def __updatePageChat(self):
        if (self.__chatPageNumber is not None) and (
            self.__chatPageNumber[0] == self.__chatParagraph):
            pageNumber = self.__chatPageNumber[1]
            if pageNumber >= 0:
                if not self.__chatSet:
                    if len(self.__chatDialogueList) > 0:
                        dialogue = self.__chatDialogueList[0]
                    else:
                        dialogue = None
                    self.setChatAbsolute(self.__chatMessage, self.__chatFlags, dialogue)
                    self.__chatSet = 1
                if pageNumber < self.nametag.getNumChatPages():
                    if (self.__chatAddressee == base.localAvatar.doId) and self.__chatQuitButton:
                        if pageNumber == self.nametag.getNumChatPages() - 1:
                            self.nametag.setChatButton(NametagGlobals.quitButton)
                    self.nametag.setChatPageIndex(pageNumber)
                    if pageNumber > 0:
                        if len(self.__chatDialogueList) > pageNumber:
                            dialogue = self.__chatDialogueList[pageNumber]
                        else:
                            dialogue = None
                        self.playCurrentDialogue(dialogue, self.__chatFlags)
                else:
                    self.clearChat()
            else:
                self.clearChat()

    def getAirborneHeight(self):
        height = self.getPos(self.shadowPlacer.shadowNodePath)
        return height.getZ() + 0.025

    def initializeNametag3d(self):
        self.deleteNametag3d()
        nametagNode = self.nametag.getNametag3d()
        self.nametagNodePath = self.nametag3d.attachNewNode(nametagNode)
        iconNodePath = self.nametag.getIcon()
        for cJoint in self.getNametagJoints():
            cJoint.clearNetTransforms()
            cJoint.addNetTransform(nametagNode)

    def nametagAmbientLightChanged(self, newlight):
        self.nametag3d.setLightOff()
        if newlight:
            self.nametag3d.setLight(newlight)

    def deleteNametag3d(self):
        if self.nametagNodePath:
            self.nametagNodePath.removeNode()
            self.nametagNodePath = None

    def initializeBodyCollisions(self, collIdStr):
        self.collTube = CollisionTube(0, 0, 0.5, 0, 0, self.height - self.getRadius(), self.getRadius())
        self.collNode = CollisionNode(collIdStr)
        self.collNode.addSolid(self.collTube)
        self.collNodePath = self.attachNewNode(self.collNode)
        if self.ghostMode:
            self.collNode.setCollideMask(OTPGlobals.GhostBitmask)
        else:
            self.collNode.setCollideMask(OTPGlobals.WallBitmask)

    def stashBodyCollisions(self):
        if hasattr(self, 'collNodePath'):
            self.collNodePath.stash()

    def unstashBodyCollisions(self):
        if hasattr(self, 'collNodePath'):
            self.collNodePath.unstash()

    def disableBodyCollisions(self):
        if hasattr(self, 'collNodePath'):
            self.collNodePath.removeNode()
            del self.collNodePath
        self.collTube = None
        return

    def addActive(self):
        if base.wantNametags:
            try:
                Avatar.ActiveAvatars.remove(self)
            except ValueError:
                pass

            Avatar.ActiveAvatars.append(self)
            self.nametag.manage(base.marginManager)
            self.accept(self.nametag.getUniqueName(), self.clickedNametag)

    def removeActive(self):
        if base.wantNametags:
            try:
                Avatar.ActiveAvatars.remove(self)
            except ValueError:
                pass

            self.nametag.unmanage(base.marginManager)
            self.ignore(self.nametag.getUniqueName())

    def loop(self, animName, restart = 1, partName = None, fromFrame = None, toFrame = None):
        return Actor.loop(self, animName, restart, partName, fromFrame, toFrame)


@magicWord(category=CATEGORY_COMMUNITY_MANAGER)
def target():
    """
    Returns the current Spellbook target.
    """
    target = spellbook.getTarget()
    return '%s ac:%d toon:%d [%d]' % (target.getName(), target.DISLid, target.doId, target.getAdminAccess())
