<<<<<<< HEAD
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

class DistributedMailManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedMailManagerAI")

    def sendSimpleMail(self, todo0, todo1, todo2):
        pass

    def setNumMailItems(self, todo0, todo1):
        pass

=======
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

class DistributedMailManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedMailManagerAI")

    def sendSimpleMail(self, todo0, todo1, todo2):
        pass

    def setNumMailItems(self, todo0, todo1):
        pass

>>>>>>> 30847815294dd00139dc93e7849d6bffd935eca9
