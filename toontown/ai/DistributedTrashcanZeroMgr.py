<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> parent of 4ac8727... fixed credits and added zander and zander's picture he took
from direct.directnotify import DirectNotifyGlobal
from direct.distributed import DistributedObject
from toontown.ai import DistributedPhaseEventMgr

class DistributedTrashcanZeroMgr(DistributedPhaseEventMgr.DistributedPhaseEventMgr):
    neverDisable = 1
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedTrashcanZeroMgr')

    def __init__(self, cr):
        DistributedPhaseEventMgr.DistributedPhaseEventMgr.__init__(self, cr)
        cr.trashcanZeroMgr = self

    def announceGenerate(self):
        DistributedPhaseEventMgr.DistributedPhaseEventMgr.announceGenerate(self)
        messenger.send('trashcanZeroIsRunning', [self.isRunning])

    def delete(self):
        self.notify.debug('deleting trashcanzeromgr')
        messenger.send('trashcanZeroIsRunning', [False])
        DistributedPhaseEventMgr.DistributedPhaseEventMgr.delete(self)
        if hasattr(self.cr, 'trashcanZeroMgr'):
            del self.cr.trashcanZeroMgr

    def setCurPhase(self, newPhase):
        DistributedPhaseEventMgr.DistributedPhaseEventMgr.setCurPhase(self, newPhase)
        messenger.send('trashcanZeroPhase', [newPhase])

    def setIsRunning(self, isRunning):
        DistributedPhaseEventMgr.DistributedPhaseEventMgr.setIsRunning(self, isRunning)
        messenger.send('trashcanZeroIsRunning', [isRunning])
<<<<<<< HEAD
=======
from direct.directnotify import DirectNotifyGlobal
from direct.distributed import DistributedObject
from toontown.ai import DistributedPhaseEventMgr

class DistributedTrashcanZeroMgr(DistributedPhaseEventMgr.DistributedPhaseEventMgr):
    neverDisable = 1
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedTrashcanZeroMgr')

    def __init__(self, cr):
        DistributedPhaseEventMgr.DistributedPhaseEventMgr.__init__(self, cr)
        cr.trashcanZeroMgr = self

    def announceGenerate(self):
        DistributedPhaseEventMgr.DistributedPhaseEventMgr.announceGenerate(self)
        messenger.send('trashcanZeroIsRunning', [self.isRunning])

    def delete(self):
        self.notify.debug('deleting trashcanzeromgr')
        messenger.send('trashcanZeroIsRunning', [False])
        DistributedPhaseEventMgr.DistributedPhaseEventMgr.delete(self)
        if hasattr(self.cr, 'trashcanZeroMgr'):
            del self.cr.trashcanZeroMgr

    def setCurPhase(self, newPhase):
        DistributedPhaseEventMgr.DistributedPhaseEventMgr.setCurPhase(self, newPhase)
        messenger.send('trashcanZeroPhase', [newPhase])

    def setIsRunning(self, isRunning):
        DistributedPhaseEventMgr.DistributedPhaseEventMgr.setIsRunning(self, isRunning)
        messenger.send('trashcanZeroIsRunning', [isRunning])
>>>>>>> 30847815294dd00139dc93e7849d6bffd935eca9
=======
>>>>>>> parent of 4ac8727... fixed credits and added zander and zander's picture he took
