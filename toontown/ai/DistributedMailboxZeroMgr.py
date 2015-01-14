<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> parent of 4ac8727... fixed credits and added zander and zander's picture he took
from direct.directnotify import DirectNotifyGlobal
from direct.distributed import DistributedObject
from toontown.ai import DistributedPhaseEventMgr

class DistributedMailboxZeroMgr(DistributedPhaseEventMgr.DistributedPhaseEventMgr):
    neverDisable = 1
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedMailboxZeroMgr')

    def __init__(self, cr):
        DistributedPhaseEventMgr.DistributedPhaseEventMgr.__init__(self, cr)
        cr.mailboxZeroMgr = self

    def announceGenerate(self):
        DistributedPhaseEventMgr.DistributedPhaseEventMgr.announceGenerate(self)
        messenger.send('mailboxZeroIsRunning', [self.isRunning])

    def delete(self):
        self.notify.debug('deleting mailboxzeromgr')
        messenger.send('mailboxZeroIsRunning', [False])
        DistributedPhaseEventMgr.DistributedPhaseEventMgr.delete(self)
        if hasattr(self.cr, 'mailboxZeroMgr'):
            del self.cr.mailboxZeroMgr

    def setCurPhase(self, newPhase):
        DistributedPhaseEventMgr.DistributedPhaseEventMgr.setCurPhase(self, newPhase)
        messenger.send('mailboxZeroPhase', [newPhase])

    def setIsRunning(self, isRunning):
        DistributedPhaseEventMgr.DistributedPhaseEventMgr.setIsRunning(self, isRunning)
        messenger.send('mailboxZeroIsRunning', [isRunning])
<<<<<<< HEAD
=======
from direct.directnotify import DirectNotifyGlobal
from direct.distributed import DistributedObject
from toontown.ai import DistributedPhaseEventMgr

class DistributedMailboxZeroMgr(DistributedPhaseEventMgr.DistributedPhaseEventMgr):
    neverDisable = 1
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedMailboxZeroMgr')

    def __init__(self, cr):
        DistributedPhaseEventMgr.DistributedPhaseEventMgr.__init__(self, cr)
        cr.mailboxZeroMgr = self

    def announceGenerate(self):
        DistributedPhaseEventMgr.DistributedPhaseEventMgr.announceGenerate(self)
        messenger.send('mailboxZeroIsRunning', [self.isRunning])

    def delete(self):
        self.notify.debug('deleting mailboxzeromgr')
        messenger.send('mailboxZeroIsRunning', [False])
        DistributedPhaseEventMgr.DistributedPhaseEventMgr.delete(self)
        if hasattr(self.cr, 'mailboxZeroMgr'):
            del self.cr.mailboxZeroMgr

    def setCurPhase(self, newPhase):
        DistributedPhaseEventMgr.DistributedPhaseEventMgr.setCurPhase(self, newPhase)
        messenger.send('mailboxZeroPhase', [newPhase])

    def setIsRunning(self, isRunning):
        DistributedPhaseEventMgr.DistributedPhaseEventMgr.setIsRunning(self, isRunning)
        messenger.send('mailboxZeroIsRunning', [isRunning])
>>>>>>> 30847815294dd00139dc93e7849d6bffd935eca9
=======
>>>>>>> parent of 4ac8727... fixed credits and added zander and zander's picture he took
