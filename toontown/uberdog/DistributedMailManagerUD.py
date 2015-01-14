<<<<<<< HEAD
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectUD import DistributedObjectUD

class DistributedMailManagerUD(DistributedObjectUD):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedMailManagerUD")

    def sendSimpleMail(self, todo0, todo1, todo2):
        pass

    def setNumMailItems(self, todo0, todo1):
        pass

=======
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectUD import DistributedObjectUD

class DistributedMailManagerUD(DistributedObjectUD):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedMailManagerUD")

    def sendSimpleMail(self, todo0, todo1, todo2):
        pass

    def setNumMailItems(self, todo0, todo1):
        pass

>>>>>>> 30847815294dd00139dc93e7849d6bffd935eca9
