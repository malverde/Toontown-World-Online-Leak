# Embedded file name: otp\margins\ClickablePopup.py
from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
from otp.nametag import NametagGlobals

class ClickablePopup(PandaNode, DirectObject):
    CS_NORMAL = 0
    CS_CLICK = 1
    CS_HOVER = 2
    CS_DISABLED = 3

    def __init__(self, cam = None):
        PandaNode.__init__(self, 'popup')
        DirectObject.__init__(self)
        self.__mwn = NametagGlobals.mouseWatcher
        self.__name = 'clickregion-%d' % id(self)
        self.__cam = cam
        self.__region = MouseWatcherRegion(self.__name, 0, 0, 0, 0)
        self.__mwn.addRegion(self.__region)
        self.__disabled = False
        self.__clicked = False
        self.__hovered = False
        self.__onscreen = False
        self.__clickState = 0
        self.__clickArgs = []
        self.__clickEvent = ''
        self.accept(self.__getEvent(self.__mwn.getEnterPattern()), self.__mouseEnter)
        self.accept(self.__getEvent(self.__mwn.getLeavePattern()), self.__mouseLeave)
        self.accept(self.__getEvent(self.__mwn.getButtonDownPattern()), self.__buttonDown)
        self.accept(self.__getEvent(self.__mwn.getButtonUpPattern()), self.__buttonUp)

    def destroy(self):
        self.__mwn.removeRegion(self.__region)
        self.ignoreAll()

    def setClickRegionEvent(self, event, clickArgs = []):
        if event is None:
            self.__disabled = True
            self.__region.setActive(False)
            self.__updateClickState()
        else:
            self.__clickEvent = event
            self.__clickArgs = clickArgs
            self.__disabled = False
            self.__region.setActive(True)
            self.__updateClickState()
        return

    def getClickState(self):
        return self.__clickState

    def clickStateChanged(self):
        pass

    def __getEvent(self, pattern):
        return pattern.replace('%r', self.__name)

    def __mouseEnter(self, region, extra):
        self.__hovered = True
        self.__updateClickState()

    def __mouseLeave(self, region, extra):
        self.__hovered = False
        self.__updateClickState()

    def __buttonDown(self, region, button):
        if button == 'mouse1':
            self.__clicked = True
            self.__updateClickState()

    def __buttonUp(self, region, button):
        if button == 'mouse1':
            self.__clicked = False
            self.__updateClickState()

    def __updateClickState(self):
        if self.__disabled:
            state = self.CS_DISABLED
        elif self.__clicked:
            state = self.CS_CLICK
        elif self.__hovered:
            state = self.CS_HOVER
        else:
            state = self.CS_NORMAL
        if self.__clickState == state:
            return
        oldState = self.__clickState
        self.__clickState = state
        if oldState == self.CS_NORMAL and state == self.CS_HOVER:
            base.playSfx(NametagGlobals.rolloverSound)
        elif state == self.CS_CLICK:
            base.playSfx(NametagGlobals.clickSound)
        elif oldState == self.CS_CLICK and state == self.CS_HOVER:
            messenger.send(self.__clickEvent, self.__clickArgs)
        self.clickStateChanged()

    def updateClickRegion(self, left, right, bottom, top, offset = 0):
        transform = NodePath.anyPath(self).getNetTransform()
        if self.__cam:
            camTransform = self.__cam.getNetTransform()
            transform = camTransform.invertCompose(transform)
        transform = transform.setQuat(Quat())
        mat = transform.getMat()
        cTopLeft = mat.xformPoint(Point3(left, 0, top))
        cBottomRight = mat.xformPoint(Point3(right, 0, bottom))
        if offset:
            mid = mat.xformPoint(Point3(0, 0, 0))
            length = mid.length()
            shift = mid * (length - offset) / length - mid
            cTopLeft += shift
            cBottomRight += shift
        if self.__cam:
            lens = self.__cam.node().getLens()
            sTopLeft = Point2()
            sBottomRight = Point2()
            if not (lens.project(Point3(cTopLeft), sTopLeft) and lens.project(Point3(cBottomRight), sBottomRight)):
                self.__region.setActive(False)
                self.__onscreen = False
                return
        else:
            sTopLeft = Point2(cTopLeft[0], cTopLeft[2])
            sBottomRight = Point2(cBottomRight[0], cBottomRight[2])
        sLeft, sTop = sTopLeft
        sRight, sBottom = sBottomRight
        self.__region.setFrame(sLeft, sRight, sBottom, sTop)
        self.__region.setActive(not self.__disabled)
        self.__onscreen = True

    def stashClickRegion(self):
        self.__region.setActive(False)
        self.__onscreen = False

    def isOnScreen(self):
        return self.__onscreen