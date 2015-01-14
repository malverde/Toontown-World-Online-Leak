<<<<<<< HEAD
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectGlobalAI import DistributedObjectGlobalAI

class DistributedSecurityMgrAI(DistributedObjectGlobalAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedSecurityMgrAI")

    def requestAccountId(self, todo0, todo1, todo2):
        pass

    def requestAccountIdResponse(self, todo0, todo1):
        pass

=======
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectGlobalAI import DistributedObjectGlobalAI

class DistributedSecurityMgrAI(DistributedObjectGlobalAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedSecurityMgrAI")

    def requestAccountId(self, todo0, todo1, todo2):
        pass

    def requestAccountIdResponse(self, todo0, todo1):
        pass

>>>>>>> 30847815294dd00139dc93e7849d6bffd935eca9
