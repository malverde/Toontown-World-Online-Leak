from direct.directnotify import DirectNotifyGlobal
from direct.distributed import DistributedObjectAI
from direct.directutil import DistributedLargeBlobSenderAI
from SpecImports import *

class DistributedInGameEditorAI(DistributedObjectAI.DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedInGameEditorAI')

    def __init__(self, air, level, editorAvId, editUsername):
        DistributedObjectAI.DistributedObjectAI.__init__(self, air)
        self.editorAvId = editorAvId
        self.editUsername = editUsername
        self.level = level
        self.levelDoId = self.level.getDoId()
        self.generateWithRequired(level.zoneId)

    def generate(self):
        self.notify.debug('generate')
        DistributedObjectAI.DistributedObjectAI.generate(self)
        simbase.levelEditor = self
        self.acceptOnce(self.air.getAvatarExitEvent(self.editorAvId), self.setFinished)
        self.accept(self.level.getATTWibChangeEventName(), self.handleATTWibChange)

    def delete(self):
        self.notify.debug('delete')
        messenger.send(self.getDoneEvent())
        DistributedObjectAI.DistributedObjectAI.delete(self)
        self.ignoreAll()

    def getDoneEvent(self):
        return self.uniqueName('levelEditorDone')

    def getEditorAvId(self):
        return self.editorAvId

    def getEditUsername(self):
        return self.editUsername

    def getLevelDoId(self):
        return self.levelDoId

    def requestCurrentLevelSpec(self):
        print 'requestCurrentLevelSpec'
        spec = self.level.levelSpec
        specStr = repr(spec)
        largeBlob = DistributedLargeBlobSenderAI.DistributedLargeBlobSenderAI(self.air, self.zoneId, self.editorAvId, specStr, useDisk=config.GetBool('spec-by-disk', 1))
        self.sendUpdateToAvatarId(self.editorAvId, 'setSpecSenderDoId', [largeBlob.doId])

    def setEdit(self, entId, aTTWibName, valueStr, username):
        self.level.setATTWibChange(entId, aTTWibName, eval(valueStr), username)

    def handleATTWibChange(self, entId, aTTWib, value, username):
        self.sendUpdateToAvatarId(self.editorAvId, 'setATTWibChange', [entId,
         aTTWib,
         repr(value),
         username])

    def setFinished(self):
        self.requestDelete()
