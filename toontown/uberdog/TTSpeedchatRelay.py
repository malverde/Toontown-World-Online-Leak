<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> parent of 4ac8727... fixed credits and added zander and zander's picture he took
from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal
from direct.directnotify.DirectNotifyGlobal import directNotify
from otp.otpbase import OTPGlobals
from otp.uberdog.SpeedchatRelay import SpeedchatRelay
from otp.uberdog import SpeedchatRelayGlobals

class TTSpeedchatRelay(SpeedchatRelay):

    def __init__(self, cr):
        SpeedchatRelay.__init__(self, cr)

    def sendSpeedchatToonTask(self, receiverId, taskId, toNpcId, toonProgress, msgIndex):
        self.sendSpeedchatToRelay(receiverId, SpeedchatRelayGlobals.TOONTOWN_QUEST, [taskId,
         toNpcId,
         toonProgress,
         msgIndex])
<<<<<<< HEAD
=======
from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal
from direct.directnotify.DirectNotifyGlobal import directNotify
from otp.otpbase import OTPGlobals
from otp.uberdog.SpeedchatRelay import SpeedchatRelay
from otp.uberdog import SpeedchatRelayGlobals

class TTSpeedchatRelay(SpeedchatRelay):

    def __init__(self, cr):
        SpeedchatRelay.__init__(self, cr)

    def sendSpeedchatToonTask(self, receiverId, taskId, toNpcId, toonProgress, msgIndex):
        self.sendSpeedchatToRelay(receiverId, SpeedchatRelayGlobals.TOONTOWN_QUEST, [taskId,
         toNpcId,
         toonProgress,
         msgIndex])
>>>>>>> 30847815294dd00139dc93e7849d6bffd935eca9
=======
>>>>>>> parent of 4ac8727... fixed credits and added zander and zander's picture he took
