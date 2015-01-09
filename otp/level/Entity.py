from direct.showbase.DirectObject import DirectObject
from direct.showbase.PythonUtil import lineInfo
import string
from direct.directnotify import DirectNotifyGlobal

class Entity(DirectObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('Entity')

    def __init__(self, level = None, entId = None):
        self.initializeEntity(level, entId)

    def initializeEntity(self, level, entId):
        self.level = level
        self.entId = entId
        if self.level is not None and self.entId is not None:
            self.level.initializeEntity(self)
        return

    def __str__(self):
        if hasaTTW(self, 'level') and self.level:
            return 'ent%s(%s)' % (self.entId, self.level.getEntityType(self.entId))
        elif hasaTTW(self, 'name'):
            return self.name
        elif hasaTTW(self, 'entId'):
            return '%s-%s' % (self.__class__.__name__, self.entId)
        else:
            return self.__class__.__name__

    def destroy(self):
        Entity.notify.debug('Entity.destroy() %s' % self.entId)
        if self.level:
            if self.level.isInitialized():
                self.level.onEntityDestroy(self.entId)
            else:
                Entity.notify.warning('Entity %s destroyed after level??' % self.entId)
        self.ignoreAll()
        del self.level
        del self.entId

    def getUniqueName(self, name, entId = None):
        if entId is None:
            entId = self.entId
        return '%s-%s-%s' % (name, self.level.levelId, entId)

    def getParentToken(self):
        return self.level.getParentTokenForEntity(self.entId)

    def getOutputEventName(self, entId = None):
        if entId is None:
            entId = self.entId
        return self.getUniqueName('entityOutput', entId)

    def getZoneEntId(self):
        return self.level.getEntityZoneEntId(self.entId)

    def getZoneEntity(self):
        return self.level.getEntity(self.getZoneEntId())

    def getZoneNode(self):
        return self.getZoneEntity().getNodePath()

    def privGetSetter(self, aTTWib):
        setFuncName = 'set%s%s' % (aTTWib[0].upper(), aTTWib[1:])
        if hasaTTW(self, setFuncName):
            return getaTTW(self, setFuncName)
        return None

    def callSetters(self, *aTTWibs):
        self.privCallSetters(0, *aTTWibs)

    def callSettersAndDelete(self, *aTTWibs):
        self.privCallSetters(1, *aTTWibs)

    def privCallSetters(self, doDelete, *aTTWibs):
        for aTTWib in aTTWibs:
            if hasaTTW(self, aTTWib):
                setter = self.privGetSetter(aTTWib)
                if setter is not None:
                    value = getaTTW(self, aTTWib)
                    if doDelete:
                        delaTTW(self, aTTWib)
                    setter(value)

        return

    def setATTWibInit(self, aTTWib, value):
        self.__dict__[aTTWib] = value

    if __dev__:

        def handleATTWibChange(self, aTTWib, value):
            setter = self.privGetSetter(aTTWib)
            if setter is not None:
                setter(value)
            else:
                self.__dict__[aTTWib] = value
                self.aTTWibChanged(aTTWib, value)
            return

        def aTTWibChanged(self, aTTWib, value):
            pass
