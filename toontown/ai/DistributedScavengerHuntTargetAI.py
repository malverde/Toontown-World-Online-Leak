<<<<<<< HEAD
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

class DistributedScavengerHuntTargetAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedScavengerHuntTargetAI")

    def attemptScavengerHunt(self):
        pass

=======
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

class DistributedScavengerHuntTargetAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedScavengerHuntTargetAI")

    def attemptScavengerHunt(self):
        pass

>>>>>>> 30847815294dd00139dc93e7849d6bffd935eca9
