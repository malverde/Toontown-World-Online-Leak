from direct.directnotify import DirectNotifyGlobal
from toontown.uberdog.ClientServicesManagerUD import executeHttpRequest
import datetime
from direct.fsm.FSM import FSM
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.MsgTypes import *
from otp.ai.MagicWordGlobal import *
from direct.showbase.DirectObject import DirectObject

class BanFSM(FSM):

    def __init__(self, air, avId, comment, duration):
        FSM.__init__(self, 'banFSM-%s' % avId)
        self.air = air
        self.avId = avId

        # Needed variables for the actual banning.
        self.comment = comment
        self.duration = duration
        self.DISLid = None
        self.accountId = None
        self.avName = None

    def performBan(self, bannedUntil):
        executeHttpRequest('accounts/ban/', Id=self.accountId, Release=bannedUntil,
                           Reason=self.comment)

    def ejectPlayer(self):
        av = self.air.doId2do.get(self.avId)
        if not av:
            return

        # Send the client a 'CLIENTAGENT_EJECT' with the players name.
        datagram.addServerHeader(
                av.GetPuppetConnectionChannel(self.avId),
                self.air.ourChannel, CLIENTAGENT_EJECT)
        datagram.addUint16(152)
        datagram.addString(self.avName)
        simbase.air.send(datagram)

    def dbCallback(self, dclass, fields):
        if dclass != self.air.dclassesByName['AccountAI']:
            return

        self.accountId = fields.get('ACCOUNT_ID')

        if not self.accountId:
            return

        date = datetime.date.today()
        if simbase.config.GetBool('want-bans', True):
            if self.duration == 0:
                bannedUntil = "0000-00-00" # Terminated.
            else:
                bannedUntil = date + datetime.timedelta(days=self.duration)

            self.duration = None
            self.performBan(bannedUntil)

    def getAvatarDetails(self):
        av = self.air.doId2do.get(self.avId)
        if not av:
            return

        self.DISLid = av.getDISLid()
        self.avName = av.getName()

    def log(self):
        simbase.air.writeServerEvent('account_ban', self.avId, '%s|%s' % (self.accountId, self.comment))

    def cleanup(self):
        self.air = None
        self.avId = None

        self.DISLid = None
        self.avName = None
        self.accountId = None
        self.comment = None
        self.duration = None
        self = None

    def enterStart(self):
        self.getAvatarDetails()
        self.air.dbInterface.queryObject(self.air.dbId, self.DISLid,
                                         self.dbCallback)
        self.ejectPlayer()

    def exitStart(self):
        self.log()
        self.cleanup()

    def enterOff(self):
        pass

    def exitOff(self):
        pass

class BanManagerAI(DirectObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('BanManagerAI')

    def __init__(self, air):
        self.air = air
        self.banFSMs = {}

    def ban(self, avId, duration, comment):
        self.banFSMs[avId] = BanFSM(self.air, avId, comment, duration)
        self.banFSMs[avId].request('Start')

        self.acceptOnce(self.air.getAvatarExitEvent(avId), self.banDone, [avId])

    def banDone(self, avId):
        self.banFSMs[avId].request('Off')
        self.banFSMs[avId] = None

@magicWord(category=CATEGORY_MODERATOR)
def kick():
    """
    Kick the target from the game server.
    """
    target = spellbook.getTarget()
    if target == spellbook.getInvoker():
        return "You can't kick yourself!"
    datagram = PyDatagram()
    datagram.addServerHeader(
        target.GetPuppetConnectionChannel(target.doId),
        simbase.air.ourChannel, CLIENTAGENT_EJECT)
    datagram.addUint16(155)
    datagram.addString('You were kicked by a moderator!')
    simbase.air.send(datagram)
    return "Kicked %s from the game server!" % target.getName()

@magicWord(category=CATEGORY_MODERATOR, types=[str, int])
def ban(reason, duration):
    """
    Ban the target from the game server.
    """
    target = spellbook.getTarget()
    if target == spellbook.getInvoker():
        return "You can't ban yourself!"
    if reason not in ('hacking','language','other'):
        return "'%s' is not a valid reason." % reason
    simbase.air.banManager.ban(target.doId, duration, reason)
    return "Banned %s from the game server!" % target.getName()