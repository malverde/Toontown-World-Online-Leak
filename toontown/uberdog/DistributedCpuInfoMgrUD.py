<<<<<<< HEAD
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD

class DistributedCpuInfoMgrUD(DistributedObjectGlobalUD):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedCpuInfoMgrUD")

    def setCpuInfoToUd(self, todo0, todo1, todo2, todo3):
        pass

=======
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD

class DistributedCpuInfoMgrUD(DistributedObjectGlobalUD):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedCpuInfoMgrUD")

    def setCpuInfoToUd(self, todo0, todo1, todo2, todo3):
        pass

>>>>>>> 30847815294dd00139dc93e7849d6bffd935eca9
