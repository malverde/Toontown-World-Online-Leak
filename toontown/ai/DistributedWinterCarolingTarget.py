<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> parent of 4ac8727... fixed credits and added zander and zander's picture he took
from direct.directnotify import DirectNotifyGlobal
from direct.distributed import DistributedObject
from toontown.speedchat.TTSCIndexedTerminal import TTSCIndexedMsgEvent
import DistributedScavengerHuntTarget

class DistributedWinterCarolingTarget(DistributedScavengerHuntTarget.DistributedScavengerHuntTarget):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedWinterCarolingTarget')

    def __init__(self, cr):
        DistributedScavengerHuntTarget.DistributedScavengerHuntTarget.__init__(self, cr)

    def setupListenerDetails(self):
        self.triggered = False
        self.triggerDelay = 15
        self.accept(TTSCIndexedMsgEvent, self.phraseSaid)

    def phraseSaid(self, phraseId):
        self.notify.debug('Checking if phrase was said')
        helpPhrases = []
        for i in range(6):
            helpPhrases.append(30220 + i)

        def reset():
            self.triggered = False

        if phraseId in helpPhrases and not self.triggered:
            self.triggered = True
            self.attemptScavengerHunt()
            taskMgr.doMethodLater(self.triggerDelay, reset, 'ScavengerHunt-phrase-reset', extraArgs=[])
<<<<<<< HEAD
=======
from direct.directnotify import DirectNotifyGlobal
from direct.distributed import DistributedObject
from toontown.speedchat.TTSCIndexedTerminal import TTSCIndexedMsgEvent
import DistributedScavengerHuntTarget

class DistributedWinterCarolingTarget(DistributedScavengerHuntTarget.DistributedScavengerHuntTarget):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedWinterCarolingTarget')

    def __init__(self, cr):
        DistributedScavengerHuntTarget.DistributedScavengerHuntTarget.__init__(self, cr)

    def setupListenerDetails(self):
        self.triggered = False
        self.triggerDelay = 15
        self.accept(TTSCIndexedMsgEvent, self.phraseSaid)

    def phraseSaid(self, phraseId):
        self.notify.debug('Checking if phrase was said')
        helpPhrases = []
        for i in range(6):
            helpPhrases.append(30220 + i)

        def reset():
            self.triggered = False

        if phraseId in helpPhrases and not self.triggered:
            self.triggered = True
            self.attemptScavengerHunt()
            taskMgr.doMethodLater(self.triggerDelay, reset, 'ScavengerHunt-phrase-reset', extraArgs=[])
>>>>>>> 30847815294dd00139dc93e7849d6bffd935eca9
=======
>>>>>>> parent of 4ac8727... fixed credits and added zander and zander's picture he took
