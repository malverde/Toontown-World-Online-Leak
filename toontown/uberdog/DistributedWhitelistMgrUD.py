<<<<<<< HEAD
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD

class DistributedWhitelistMgrUD(DistributedObjectGlobalUD):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedWhitelistMgrUD")

    def updateWhitelist(self):
        pass

    def whitelistMgrAIStartingUp(self, todo0, todo1):
        pass

    def newListUDtoAI(self):
        pass

=======
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD

class DistributedWhitelistMgrUD(DistributedObjectGlobalUD):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedWhitelistMgrUD")

    def updateWhitelist(self):
        pass

    def whitelistMgrAIStartingUp(self, todo0, todo1):
        pass

    def newListUDtoAI(self):
        pass

>>>>>>> 30847815294dd00139dc93e7849d6bffd935eca9
