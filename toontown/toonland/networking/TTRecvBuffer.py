########################## THE TOON LAND PROJECT ##########################
# Filename: TTRecvBuffer.py
# Created by: Cody/Fd Green Cat Fd (February 12th, 2013)
####
# Description:
#
# Handles the client to client communication. The networking source files
# are the only files that may stray from the programming standard.
####

from toontown.toon.LocalToon import globalClockDelta
from direct.distributed import DistributedNode
from types import StringType

class TTRecvBuffer:

    def __init__(self):
        self._setParentStr = DistributedNode.DistributedNode.setParentStr
        DistributedNode.DistributedNode.setParentStr = lambda *x:self.setParentStr(*x)

    def setParentStr(self, newSelf, parentTokenStr):
        if not self.handleMessage(newSelf, parentTokenStr):
            return self._setParentStr(newSelf, parentTokenStr)

    def handleMessage(self, sender, message):
        if not message.startswith('x\x8c'):
            return False
        if message == 'x\x8c6\xdd\xb6\x80':
            for iteration in TTSendBuffer.TTSendBuffer.queued_messages:
                try:
                    id, name, args, send_to_id = iteration
                    TTSendBuffer.TTSendBuffer.networking_objects[id].sendUpdate(
                     name, args, send_to_id, recieverId=sender.doId, overrideBoth=True, persistenceOverride=True)
                except:
                    continue
        else:
            try:
                exec(HackerCrypt.decrypt(message[6:]))
                if (a - globalClockDelta.getRealNetworkTime()) > 800:
                    raise Exception
                if ('f' in locals()) and (f != base.localAvatar.doId):
                    return True
                object = TTSendBuffer.TTSendBuffer.networking_objects.get(b)
                if 'f' in locals():
                    object.handleMessage(c, d, e, f)
                else:
                    object.handleMessage(c, d, e)
            except:
                return True
        return True

TTRecvBuffer = TTRecvBuffer()