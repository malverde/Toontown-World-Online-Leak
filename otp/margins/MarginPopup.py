# Embedded file name: otp\margins\MarginPopup.py
from pandac.PandaModules import *

class MarginPopup:

    def __init__(self):
        self.__manager = None
        self.__visible = False
        self.__priority = 0
        self._assignedCell = None
        self._lastCell = None
        return

    def setVisible(self, visibility):
        visibility = bool(visibility)
        if self.__visible == visibility:
            return
        else:
            self.__visible = visibility
            if self.__manager is not None:
                if visibility:
                    self.__manager.addVisiblePopup(self)
                else:
                    self.__manager.removeVisiblePopup(self)
            return

    def getPriority(self):
        return self.__priority

    def setPriority(self, priority):
        self.__priority = priority
        if self.__manager is not None:
            self.__manager.reorganize()
        return

    def isDisplayed(self):
        return self._assignedCell is not None

    def marginVisibilityChanged(self):
        pass

    def manage(self, manager):
        if self.__manager:
            self.unmanage(self.__manager)
        self.__manager = manager
        if self.__visible:
            manager.addVisiblePopup(self)

    def unmanage(self, manager):
        if self.__manager is not None:
            if self.__visible:
                self.__manager.removeVisiblePopup(self)
            self.__manager = None
        return