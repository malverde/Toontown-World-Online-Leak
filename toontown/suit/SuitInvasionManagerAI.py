import SuitDNA
from otp.ai.MagicWordGlobal import *
from direct.task import Task
from toontown.toonbase import ToontownGlobals
from random import random, randint, choice
import datetime
from direct.directnotify import DirectNotifyGlobal

# TODO: NewsManagerAI to properly announce invasions starting, invasions
# ending, and invasions currently in progress.
# All numbers/values in here are hard-coded. Maybe we should move them to
# ToontownGlobals or something?

class SuitInvasionManagerAI:
    """
    This is a very basic AI class to handle Suit Invasions in Toontown.
    This class doesn't need to do much, besides telling the suit planners
    when an invasion starts and stops.
    """

    notify = DirectNotifyGlobal.directNotify.newCategory('SuitInvasionManagerAI')

    def __init__(self, air):
        self.air = air
        self.invading = 0
        self.specialSuit = 0
        self.suitName = None
        self.numSuits = 0
        self.spawnedSuits = 0
        self.suitDeptIndex = None
        self.suitTypeIndex = None
        self.flags = 0


        if config.GetBool('want-mega-invasions', False): # TODO - config for this
            # Mega invasion configuration.
            self.randomInvasionProbability = config.GetFloat('mega-invasion-probability', 0.4)
            self.megaInvasionCog = config.GetString('mega-invasion-cog-type', '')
            if not self.megaInvasionCog:
                raise AttributeError("No mega invasion cog specified, but mega invasions are on!")
            if self.megaInvasionCog not in SuitDNA.suitHeadTypes:
                raise AttributeError("Invalid cog type specified for mega invasion!")
            # Start ticking.
            taskMgr.doMethodLater(randint(1800, 5400), self.__randomInvasionTick, 'random-invasion-tick')

        elif config.GetBool('want-random-invasions', True):
            # Random invasion configuration.
            self.randomInvasionProbability = config.GetFloat('random-invasion-probability', 0.3)
            # Start ticking.
            taskMgr.doMethodLater(randint(1800, 5400), self.__randomInvasionTick, 'random-invasion-tick')

    def __randomInvasionTick(self, task=None):
        """
        Each hour, have a tick to check if we want to start an invasion in
        the current district. This works by having a random invasion
        probability, and each tick it will generate a random float between
        0 and 1, and then if it's less than or equal to the probablity, it
        will spawn the invasion.

        An invasion will not be started if there is an invasion already
        on-going.
        """
        # Generate a new tick delay.
        task.delayTime = randint(1800, 5400)
        if self.getInvading():
            # We're already running an invasion. Don't start a new one.
            self.notify.debug('Invasion tested but already running invasion!')
            return task.again
        if random() <= self.randomInvasionProbability:
            # We want an invasion!
            self.notify.debug('Invasion probability hit! Starting invasion.')
            # We want to test if we get a mega invasion or a normal invasion.
            # Take the mega invasion probability and test it. If we get lucky
            # a second time, spawn a mega invasion, otherwise spawn a normal
            # invasion.
            if config.GetBool('want-mega-invasions', False) and random() <= self.randomInvasionProbability:
                # N.B.: randomInvasionProbability = mega invasion probability.
                suitName = self.megaInvasionCog
                numSuits = randint(2000, 15000)
                specialSuit = random.choice([0, 0, 0, 1, 2])
            else:
                suitName = choice(SuitDNA.suitHeadTypes)
                numSuits = randint(1500, 5000)
                specialSuit = False
            self.startInvasion(suitName, numSuits, specialSuit)
        return task.again


    def getInvading(self):
        return self.invading

    def getInvadingCog(self):
        return (self.suitDeptIndex, self.suitTypeIndex, self.flags)

    def startInvasion(self, suitDeptIndex=None, suitTypeIndex=None, flags=0,
                      type=INVASION_TYPE_NORMAL):
        if self.invading:
            # An invasion is currently in progress; ignore this request.
            return False

        if (suitDeptIndex is None) and (suitTypeIndex is None) and (not flags):
            # This invasion is no-op.
            return False

        if flags and ((suitDeptIndex is not None) or (suitTypeIndex is not None)):
            # For invasion flags to be present, it must be a generic invasion.
            return False

        if (suitDeptIndex is None) and (suitTypeIndex is not None):
            # It's impossible to determine the invading Cog.
            return False

        if flags not in (0, IFV2, IFSkelecog, IFWaiter):
            # The provided flag combination is not possible.
            return False

        if (suitDeptIndex is not None) and (suitDeptIndex >= len(SuitDNA.suitDepts)):
            # Invalid suit department.
            return False

        if (suitTypeIndex is not None) and (suitTypeIndex >= SuitDNA.suitsPerDept):
            # Invalid suit type.
            return False

        if type not in (INVASION_TYPE_NORMAL, INVASION_TYPE_MEGA):
            # Invalid invasion type.
            return False

        # Looks like we're all good. Begin the invasion:
        self.invading = True
        self.start = int(time.time())
        self.suitDeptIndex = suitDeptIndex
        self.suitTypeIndex = suitTypeIndex
        self.flags = flags

        # How many suits do we want?
        if type == INVASION_TYPE_NORMAL:
            self.total = 1000
        elif type == INVASION_TYPE_MEGA:
            self.total = 0xFFFFFFFF
        self.remaining = self.total

        self.flySuits()
        self.notifyInvasionStarted()

        # Update the invasion tracker on the districts page in the Shticker Book:
        if self.suitDeptIndex is not None:
            self.air.districtStats.b_setInvasionStatus(self.suitDeptIndex + 1)
        else:
            self.air.districtStats.b_setInvasionStatus(5)

        # If this is a normal invasion, and the players take too long to defeat
        # all of the Cogs, we'll want the invasion to timeout:
        if type == INVASION_TYPE_NORMAL:
            timeout = config.GetInt('invasion-timeout', 1800)
            taskMgr.doMethodLater(timeout, self.stopInvasion, 'invasionTimeout')

        self.sendInvasionStatus()
        return True

    def stopInvasion(self, task=None):
        if not self.invading:
            # We are not currently invading.
            return False

        # Stop the invasion timeout task:
        taskMgr.remove('invasionTimeout')

        # Update the invasion tracker on the districts page in the Shticker Book:
        self.air.districtStats.b_setInvasionStatus(0)

        # Revert what was done when the invasion started:
        self.notifyInvasionEnded()
        self.invading = False
        self.start = 0
        self.suitDeptIndex = None
        self.suitTypeIndex = None
        self.flags = 0
        self.total = 0
        self.remaining = 0
        self.flySuits()

        self.sendInvasionStatus()
        return True

    def getSuitName(self):
        if self.suitDeptIndex is not None:
            if self.suitTypeIndex is not None:
                return SuitDNA.getSuitName(self.suitDeptIndex, self.suitTypeIndex)
            else:
                return SuitDNA.suitDepts[self.suitDeptIndex]
        else:
            return SuitDNA.suitHeadTypes[0]

    def notifyInvasionStarted(self):
        msgType = ToontownGlobals.SuitInvasionBegin
        if self.flags & IFSkelecog:
            msgType = ToontownGlobals.SkelecogInvasionBegin
        elif self.flags & IFWaiter:
            msgType = ToontownGlobals.WaiterInvasionBegin
        elif self.flags & IFV2:
            msgType = ToontownGlobals.V2InvasionBegin
        self.air.newsManager.sendUpdate(
            'setInvasionStatus',
            [msgType, self.getSuitName(), self.total, self.flags])

    def notifyInvasionEnded(self):
        msgType = ToontownGlobals.SuitInvasionEnd
        if self.flags & IFSkelecog:
            msgType = ToontownGlobals.SkelecogInvasionEnd
        elif self.flags & IFWaiter:
            msgType = ToontownGlobals.WaiterInvasionEnd
        elif self.flags & IFV2:
            msgType = ToontownGlobals.V2InvasionEnd
        self.air.newsManager.sendUpdate(
            'setInvasionStatus', [msgType, self.getSuitName(), 0, self.flags])

    def notifyInvasionUpdate(self):
        self.air.newsManager.sendUpdate(
            'setInvasionStatus',
            [ToontownGlobals.SuitInvasionUpdate, self.getSuitName(),
             self.remaining, self.flags])

    def notifyInvasionBulletin(self, avId):
        msgType = ToontownGlobals.SuitInvasionBulletin
        if self.flags & IFSkelecog:
            msgType = ToontownGlobals.SkelecogInvasionBulletin
        elif self.flags & IFWaiter:
            msgType = ToontownGlobals.WaiterInvasionBulletin
        elif self.flags & IFV2:
            msgType = ToontownGlobals.V2InvasionBulletin
        self.air.newsManager.sendUpdateToAvatarId(
            avId, 'setInvasionStatus',
            [msgType, self.getSuitName(), self.remaining, self.flags])

    def flySuits(self):
        for suitPlanner in self.air.suitPlanners.values():
            suitPlanner.flySuits()

    def handleSuitDefeated(self):
        self.remaining -= 1
        if self.remaining == 0:
            self.stopInvasion()
        elif self.remaining == (self.total/2):
            self.notifyInvasionUpdate()
        self.sendInvasionStatus()

    def handleStartInvasion(self, shardId, *args):
        if shardId == self.air.ourChannel:
            self.startInvasion(*args)

    def handleStopInvasion(self, shardId):
        if shardId == self.air.ourChannel:
            self.stopInvasion()

    def sendInvasionStatus(self):
        if self.invading:
            if self.suitDeptIndex is not None:
                if self.suitTypeIndex is not None:
                    type = SuitBattleGlobals.SuitAttributes[self.getSuitName()]['name']
                else:
                    type = SuitDNA.getDeptFullname(self.getSuitName())
            else:
                type = None
            status = {
                'invasion': {
                    'type': type,
                    'flags': self.flags,
                    'remaining': self.remaining,
                    'total': self.total,
                    'start': self.start
                }
            }
        else:
            status = {'invasion': None}
        self.air.netMessenger.send('shardStatus', [self.air.ourChannel, status])

@magicWord(types=[str, str, int, int], category=CATEGORY_OVERRIDE)
def invasion(cmd, name='f', num=1000, specialSuit = 0):
    """ Spawn an invasion on the current AI if one doesn't exist. """
    invMgr = simbase.air.suitInvasionManager
    if cmd == 'start':
        if invMgr.getInvading():
            return "There is already an invasion on the current AI!"
        if not name in SuitDNA.suitHeadTypes:
            return "This cog does not exist!"
        invMgr.startInvasion(name, num, specialSuit)
    elif cmd == 'stop':
        if not invMgr.getInvading():
            return "There is no invasion on the current AI!"
        invMgr.stopInvasion()
    else:
        return "You didn't enter a valid command! Commands are ~invasion start or stop."
