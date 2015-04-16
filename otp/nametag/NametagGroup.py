# Embedded file name: otp\nametag\NametagGroup.py
from pandac.PandaModules import *
from NametagConstants import *
from Nametag3d import *
from Nametag2d import *

class NametagGroup:
    CCNormal = CCNormal
    CCNoChat = CCNoChat
    CCNonPlayer = CCNonPlayer
    CCSuit = CCSuit
    CCToonBuilding = CCToonBuilding
    CCSuitBuilding = CCSuitBuilding
    CCHouseBuilding = CCHouseBuilding
    CCSpeedChat = CCSpeedChat
    CCFreeChat = CCFreeChat
    CHAT_TIMEOUT_MAX = 12.0
    CHAT_TIMEOUT_MIN = 4.0
    CHAT_TIMEOUT_PROP = 0.5

    def __init__(self):
        self.nametag2d = Nametag2d()
        self.nametag3d = Nametag3d()
        self.icon = PandaNode('icon')
        self.chatTimeoutTask = None
        self.font = None
        self.speechFont = None
        self.name = ''
        self.displayName = ''
        self.wordWrap = None
        self.qtColor = VBase4(1, 1, 1, 1)
        self.colorCode = CCNormal
        self.avatar = None
        self.active = True
        self.chatPages = []
        self.chatPage = 0
        self.chatFlags = 0
        self.objectCode = None
        self.manager = None
        self.nametags = []
        self.addNametag(self.nametag2d)
        self.addNametag(self.nametag3d)
        self.visible3d = True
        self.tickTask = taskMgr.add(self.__tickTask, self.getUniqueId(), sort=45)
        self.stompTask = None
        self.stompText = None
        self.stompFlags = 0
        return

    def destroy(self):
        taskMgr.remove(self.tickTask)
        if self.manager is not None:
            self.unmanage(self.manager)
        for nametag in list(self.nametags):
            self.removeNametag(nametag)

        if self.stompTask:
            self.stompTask.remove()
        return

    def getNametag2d(self):
        return self.nametag2d

    def getNametag3d(self):
        return self.nametag3d

    def getNameIcon(self):
        return self.icon

    def getNumChatPages(self):
        if not self.chatFlags & (CFSpeech | CFThought):
            return 0
        return len(self.chatPages)

    def setPageNumber(self, page):
        self.chatPage = page
        self.updateTags()

    def getChatStomp(self):
        return bool(self.stompTask)

    def getChat(self):
        if self.chatPage >= len(self.chatPages):
            return ''
        else:
            return self.chatPages[self.chatPage]

    def getStompText(self):
        return self.stompText

    def getStompDelay(self):
        return 0.2

    def getUniqueId(self):
        return 'Nametag-%d' % id(self)

    def hasButton(self):
        return bool(self.getButtons())

    def getButtons(self):
        if self.getNumChatPages() < 2:
            if self.chatFlags & CFQuitButton:
                return NametagGlobals.quitButtons
            elif self.chatFlags & CFPageButton:
                return NametagGlobals.pageButtons
            else:
                return None
        elif self.chatPage == self.getNumChatPages() - 1:
            if not self.chatFlags & CFNoQuitButton:
                return NametagGlobals.quitButtons
            else:
                return None
        else:
            if self.chatFlags & CFPageButton:
                return NametagGlobals.pageButtons
            return None
        return None

    def setActive(self, active):
        self.active = active

    def isActive(self):
        return self.active

    def setAvatar(self, avatar):
        self.avatar = avatar

    def setFont(self, font):
        self.font = font
        self.updateTags()

    def setSpeechFont(self, font):
        self.speechFont = font
        self.updateTags()

    def setWordwrap(self, wrap):
        self.wordWrap = wrap
        self.updateTags()

    def setColorCode(self, cc):
        self.colorCode = cc
        self.updateTags()

    def setName(self, name):
        self.name = name
        self.updateTags()

    def setDisplayName(self, name):
        self.displayName = name
        self.updateTags()

    def setQtColor(self, color):
        self.qtColor = color
        self.updateTags()

    def setChat(self, chatString, chatFlags):
        if not self.chatFlags & CFSpeech:
            self._setChat(chatString, chatFlags)
        else:
            self.clearChat()
            self.stompText = chatString
            self.stompFlags = chatFlags
            self.stompTask = taskMgr.doMethodLater(self.getStompDelay(), self.__updateStomp, 'ChatStomp-' + self.getUniqueId())

    def _setChat(self, chatString, chatFlags):
        if chatString:
            self.chatPages = chatString.split('\x07')
            self.chatFlags = chatFlags
        else:
            self.chatPages = []
            self.chatFlags = 0
        self.setPageNumber(0)
        self._stopChatTimeout()
        if chatFlags & CFTimeout:
            self._startChatTimeout()

    def __updateStomp(self, task):
        self._setChat(self.stompText, self.stompFlags)
        self.stompTask = None
        return

    def setContents(self, contents):
        for tag in self.nametags:
            tag.setContents(contents)

    def setObjectCode(self, objectCode):
        self.objectCode = objectCode

    def getObjectCode(self):
        return self.objectCode

    def _startChatTimeout(self):
        length = len(self.getChat())
        timeout = min(max(length * self.CHAT_TIMEOUT_PROP, self.CHAT_TIMEOUT_MIN), self.CHAT_TIMEOUT_MAX)
        self.chatTimeoutTask = taskMgr.doMethodLater(timeout, self.__doChatTimeout, 'ChatTimeout-' + self.getUniqueId())

    def __doChatTimeout(self, task):
        self._setChat('', 0)
        return task.done

    def _stopChatTimeout(self):
        if self.chatTimeoutTask:
            taskMgr.remove(self.chatTimeoutTask)

    def clearShadow(self):
        pass

    def clearChat(self):
        self._setChat('', 0)
        if self.stompTask:
            self.stompTask.remove()

    def updateNametag(self, tag):
        tag.font = self.font
        tag.speechFont = self.speechFont
        tag.name = self.name
        tag.wordWrap = self.wordWrap or DEFAULT_WORDWRAPS[self.colorCode]
        tag.displayName = self.displayName or self.name
        tag.qtColor = self.qtColor
        tag.colorCode = self.colorCode
        tag.chatString = self.getChat()
        tag.buttons = self.getButtons()
        tag.chatFlags = self.chatFlags
        tag.avatar = self.avatar
        tag.icon = self.icon
        tag.update()

    def __testVisible3D(self):
        for nametag in self.nametags:
            if not isinstance(nametag, Nametag3d):
                continue
            if nametag.isOnScreen():
                return True

        return False

    def __tickTask(self, task):
        for nametag in self.nametags:
            nametag.tick()
            if NametagGlobals.masterNametagsActive and self.active or self.hasButton():
                nametag.setClickRegionEvent(self.getUniqueId())
            else:
                nametag.setClickRegionEvent(None)

        if NametagGlobals.onscreenChatForced and self.chatFlags & CFSpeech:
            visible3d = False
        elif not NametagGlobals.masterArrowsOn and not self.chatFlags:
            visible3d = True
        else:
            visible3d = self.__testVisible3D()
        if visible3d ^ self.visible3d:
            self.visible3d = visible3d
            for nametag in self.nametags:
                if isinstance(nametag, MarginPopup):
                    nametag.setVisible(not visible3d)

        return task.cont

    def updateTags(self):
        for nametag in self.nametags:
            self.updateNametag(nametag)

    def addNametag(self, nametag):
        self.nametags.append(nametag)
        self.updateNametag(nametag)
        if self.manager is not None and isinstance(nametag, MarginPopup):
            nametag.manage(manager)
        return

    def removeNametag(self, nametag):
        self.nametags.remove(nametag)
        if self.manager is not None and isinstance(nametag, MarginPopup):
            nametag.unmanage(manager)
        nametag.destroy()
        return

    def manage(self, manager):
        self.manager = manager
        for tag in self.nametags:
            if isinstance(tag, MarginPopup):
                tag.manage(manager)

    def unmanage(self, manager):
        self.manager = None
        for tag in self.nametags:
            if isinstance(tag, MarginPopup):
                tag.unmanage(manager)
                tag.destroy()

        return