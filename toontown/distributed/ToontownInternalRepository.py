from direct.distributed.AstronInternalRepository import AstronInternalRepository
from otp.distributed.OtpDoGlobals import *
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.MsgTypes import *
from panda3d.core import *
from direct.distributed.PyDatagram import PyDatagram
import traceback
import sys
import signal

ai_watchdog = ConfigVariableInt(
    'ai-watchdog', 15,
    'Specifies the maximum amount of time that a'
    ' frame may take before the process kills itself.')


class WatchdogError(Exception):
    pass


def watchdogExhausted(signum, frame):
    raise WatchdogError('The process has stalled!')


class ToontownInternalRepository(AstronInternalRepository):
    GameGlobalsId = OTP_DO_ID_TOONTOWN
    dbId = 4003

    def __init__(self, baseChannel, serverId=None, dcFileNames=None,
                 dcSuffix='AI', connectMethod=None, threadedNet=None):
        AstronInternalRepository.__init__(
            self,
            baseChannel,
            serverId,
            dcFileNames,
            dcSuffix,
            connectMethod,
            threadedNet)
        self._callbacks = {}

    def handleConnected(self):
        self.netMessenger.register(0, 'shardStatus')
        self.netMessenger.register(1, 'accountDisconnected')
        self.netMessenger.register(2, 'avatarOnline')
        self.netMessenger.register(3, 'avatarOffline')
        self.netMessenger.register(4, 'enableLogins')

    if hasattr(signal, 'alarm'):
        signal.signal(signal.SIGALRM, watchdogExhausted)
        self.__watchdog = taskMgr.add(self.__resetWatchdog, 'watchdog')
        

    def __resetWatchdog(self, task):
        signal.alarm(ai_watchdog.getValue())
        return task.cont

    def getAvatarIdFromSender(self):
        return int(self.getMsgSender() & 0xFFFFFFFF)

    def getAccountIdFromSender(self):
        return int((self.getMsgSender()>>32) & 0xFFFFFFFF)

    def setAllowClientSend(self, avId, dObj, fieldNameList=[]):
        dg = PyDatagram()
        dg.addServerHeader(
            dObj.GetPuppetConnectionChannel(avId),
            self.ourChannel,
            CLIENTAGENT_SET_FIELDS_SENDABLE)
        fieldIds = []
        for fieldName in fieldNameList:
            field = dObj.dclass.getFieldByName(fieldName)
            if field:
                fieldIds.append(field.getNumber())
        dg.addUint32(dObj.getDoId())
        dg.addUint16(len(fieldIds))
        for fieldId in fieldIds:
            dg.addUint16(fieldId)
        self.send(dg)

    def _isValidPlayerLocation(self, parentId, zoneId):
        if zoneId < 1000 and zoneId != 1:
            return False

        return True
        
    def readerPollOnce(self):
        try:
            return AstronInternalRepository.readerPollOnce(self)
        except SystemExit, KeyboardInterrupt:
        raise
        
        except Exception as e:
            if self.getAvatarIdFromSender() > 100000000:
                dg = PyDatagram()
                dg.addServerHeader(self.getMsgSender(), self.ourChannel, CLIENTAGENT_EJECT)
                dg.addUint16(153)
                dg.addString('You were disconnected to prevent a district reset.')
                self.send(dg)
            self.writeServerEvent('INTERNAL-EXCEPTION', self.getAvatarIdFromSender(), self.getAccountIdFromSender(), repr(e), traceback.format_exc())
            self.notify.warning('INTERNAL-EXCEPTION: %s (%s)' % (repr(e), self.getAvatarIdFromSender()))
            print traceback.format_exc()
            sys.exc_clear()
        return 1
