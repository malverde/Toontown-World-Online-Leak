<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> parent of 4ac8727... fixed credits and added zander and zander's picture he took
from direct.directnotify import DirectNotifyGlobal
from direct.distributed import DistributedObject
from direct.interval.IntervalGlobal import *
from otp.speedchat import SpeedChatGlobals
from toontown.toonbase import TTLocalizer

class DistributedPolarPlaceEffectMgr(DistributedObject.DistributedObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPolarPlaceEffectMgr')

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)

        def phraseSaid(phraseId):
            helpPhrase = 104
            if phraseId == helpPhrase:
                self.addPolarPlaceEffect()

        self.accept(SpeedChatGlobals.SCStaticTextMsgEvent, phraseSaid)

    def announceGenerate(self):
        DistributedObject.DistributedObject.announceGenerate(self)
        DistributedPolarPlaceEffectMgr.notify.debug('announceGenerate')

    def delete(self):
        self.ignore(SpeedChatGlobals.SCStaticTextMsgEvent)
        DistributedObject.DistributedObject.delete(self)

    def addPolarPlaceEffect(self):
        DistributedPolarPlaceEffectMgr.notify.debug('addResitanceEffect')
        av = base.localAvatar
        self.sendUpdate('addPolarPlaceEffect', [])
        msgTrack = Sequence(Func(av.setSystemMessage, 0, TTLocalizer.PolarPlaceEffect1), Wait(2), Func(av.setSystemMessage, 0, TTLocalizer.PolarPlaceEffect2), Wait(4), Func(av.setSystemMessage, 0, TTLocalizer.PolarPlaceEffect3))
        msgTrack.start()
<<<<<<< HEAD
=======
from direct.directnotify import DirectNotifyGlobal
from direct.distributed import DistributedObject
from direct.interval.IntervalGlobal import *
from otp.speedchat import SpeedChatGlobals
from toontown.toonbase import TTLocalizer

class DistributedPolarPlaceEffectMgr(DistributedObject.DistributedObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPolarPlaceEffectMgr')

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)

        def phraseSaid(phraseId):
            helpPhrase = 104
            if phraseId == helpPhrase:
                self.addPolarPlaceEffect()

        self.accept(SpeedChatGlobals.SCStaticTextMsgEvent, phraseSaid)

    def announceGenerate(self):
        DistributedObject.DistributedObject.announceGenerate(self)
        DistributedPolarPlaceEffectMgr.notify.debug('announceGenerate')

    def delete(self):
        self.ignore(SpeedChatGlobals.SCStaticTextMsgEvent)
        DistributedObject.DistributedObject.delete(self)

    def addPolarPlaceEffect(self):
        DistributedPolarPlaceEffectMgr.notify.debug('addResitanceEffect')
        av = base.localAvatar
        self.sendUpdate('addPolarPlaceEffect', [])
        msgTrack = Sequence(Func(av.setSystemMessage, 0, TTLocalizer.PolarPlaceEffect1), Wait(2), Func(av.setSystemMessage, 0, TTLocalizer.PolarPlaceEffect2), Wait(4), Func(av.setSystemMessage, 0, TTLocalizer.PolarPlaceEffect3))
        msgTrack.start()
>>>>>>> 30847815294dd00139dc93e7849d6bffd935eca9
=======
>>>>>>> parent of 4ac8727... fixed credits and added zander and zander's picture he took
