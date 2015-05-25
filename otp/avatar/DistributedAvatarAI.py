from otp.otpbase import OTPGlobals
from direct.fsm import ClassicFSM
from direct.fsm import State
from direct.distributed import DistributedNodeAI
from direct.task import Task
from otp.ai.MagicWordGlobal import *

class DistributedPlayerAI(DistributedAvatarAI.DistributedAvatarAI, PlayerBase.PlayerBase, ClsendTracker):
 
     def __init__(self, air):
         DistributedAvatarAI.DistributedAvatarAI.__init__(self, air)
         PlayerBase.PlayerBase.__init__(self)
         ClsendTracker.__init__(self)
         self.friendsList = []
         self.DISLname = ''
         self.DISLid = 0
         self.adminAccess = 0
 
class DistributedAvatarAI(DistributedNodeAI.DistributedNodeAI):

    def __init__(self, air):
        DistributedNodeAI.DistributedNodeAI.__init__(self, air)
        self.hp = 0
        self.maxHp = 0

    def b_setName(self, name):
        self.setName(name)
        self.d_setName(name)

    def d_setName(self, name):
        self.sendUpdate('setName', [name])

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def b_setMaxHp(self, maxHp):
        self.d_setMaxHp(maxHp)
        self.setMaxHp(maxHp)

    def d_setMaxHp(self, maxHp):
        self.sendUpdate('setMaxHp', [maxHp])

    def setMaxHp(self, maxHp):
        self.maxHp = maxHp

    def getMaxHp(self):
        return self.maxHp

    def b_setHp(self, hp):
        self.d_setHp(hp)
        self.setHp(hp)

    def d_setHp(self, hp):
        self.sendUpdate('setHp', [hp])

    def setHp(self, hp):
        self.hp = hp

    def getHp(self):
        return self.hp

    def b_setLocationName(self, locationName):
        self.d_setLocationName(locationName)
        self.setLocationName(locationName)

    def d_setLocationName(self, locationName):
        pass

    def setLocationName(self, locationName):
        self.locationName = locationName

    def getLocationName(self):
        return self.locationName

    def b_setActivity(self, activity):
        self.d_setActivity(activity)
        self.setActivity(activity)

    def d_setActivity(self, activity):
        pass

    def setActivity(self, activity):
        self.activity = activity

    def getActivity(self):
        return self.activity

    def toonUp(self, num):
        if self.hp >= self.maxHp:
            return
        self.hp = min(self.hp + num, self.maxHp)
        self.b_setHp(self.hp)

    def getRadius(self):
        return OTPGlobals.AvatarDefaultRadius

    def checkAvOnShard(self, avId):
        senderId = self.air.getAvatarIdFromSender()
        onShard = False
        if simbase.air.doId2do.get(avId):
            onShard = True
        self.sendUpdateToAvatarId(senderId, 'confirmAvOnShard', [avId, onShard])

@magicWord(category=CATEGORY_OVERRIDE, types=[str]) # This needs a better category.
def gwhis(text):
    """Send a whisper to the whole district, prefixed with 'ADMIN Name:'."""
    text = 'ADMIN ' + spellbook.getInvoker().getName() + ': ' + text # Prepend text with Invoker's toon name.
    for doId in simbase.air.doId2do:
        if str(doId)[:2] == '10': # Non-NPC?
            do = simbase.air.doId2do.get(doId)
        if isinstance(do, DistributedPlayerAI): # Toon?
            do.d_setSystemMessage(0, text)
