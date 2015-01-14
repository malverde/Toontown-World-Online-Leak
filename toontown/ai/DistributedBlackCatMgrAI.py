<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> parent of 4ac8727... fixed credits and added zander and zander's picture he took
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from toontown.toon.ToonDNA import ToonDNA

class DistributedBlackCatMgrAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedBlackCatMgrAI")

    def requestBlackCatTransformation(self):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)
        if not av: return

        if av.dna.getAnimal() == 'cat' and av.dna.headColor != 0x1a:
            newDNA = ToonDNA()
            newDNA.makeFromNetString(av.getDNAString())
            newDNA.headColor = 0x1a
            newDNA.armColor = 0x1a
            newDNA.legColor = 0x1a
            taskMgr.doMethodLater(1.0, lambda task: av.b_setDNAString(newDNA.makeNetString()), 'transform-%d' % avId)

            self.sendUpdate('doBlackCatTransformation', [avId])
<<<<<<< HEAD
=======
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from toontown.toon.ToonDNA import ToonDNA

class DistributedBlackCatMgrAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedBlackCatMgrAI")

    def requestBlackCatTransformation(self):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)
        if not av: return

        if av.dna.getAnimal() == 'cat' and av.dna.headColor != 0x1a:
            newDNA = ToonDNA()
            newDNA.makeFromNetString(av.getDNAString())
            newDNA.headColor = 0x1a
            newDNA.armColor = 0x1a
            newDNA.legColor = 0x1a
            taskMgr.doMethodLater(1.0, lambda task: av.b_setDNAString(newDNA.makeNetString()), 'transform-%d' % avId)

            self.sendUpdate('doBlackCatTransformation', [avId])
>>>>>>> 30847815294dd00139dc93e7849d6bffd935eca9
=======
>>>>>>> parent of 4ac8727... fixed credits and added zander and zander's picture he took
