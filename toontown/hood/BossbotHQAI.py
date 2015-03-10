from toontown.building import DistributedBBElevatorAI
from toontown.building import FADoorCodes
from toontown.building.DistributedBoardingPartyAI import DistributedBoardingPartyAI
from toontown.coghq import DistributedCogKartAI
from toontown.hood import CogHQAI
from toontown.suit import DistributedBossbotBossAI
from toontown.suit import DistributedSuitPlannerAI
from toontown.toonbase import ToontownGlobals


class BossbotHQAI(CogHQAI.CogHQAI):
    def __init__(self, air):
        CogHQAI.CogHQAI.__init__(
            self, air, ToontownGlobals.BossbotHQ, ToontownGlobals.BossbotLobby,
            FADoorCodes.BB_DISGUISE_INCOMPLETE,
            DistributedBBElevatorAI.DistributedBBElevatorAI,
            DistributedBossbotBossAI.DistributedBossbotBossAI)

        self.cogKarts = []
        self.courseBoardingParty = None
        self.suitPlanners = []

        self.startup()

    def startup(self):
        CogHQAI.CogHQAI.startup(self)

        self.createCogKarts()
        if simbase.config.GetBool('want-boarding-groups', True):
            self.createCourseBoardingParty()
        if simbase.config.GetBool('want-suit-planners', True):
            self.createSuitPlanners()

    def createCogKarts(self):
        posList = (
            (154.762, 37.169, 0), (141.403, -81.887, 0),
            (-48.44, 15.308, 0)
        )
        hprList = ((110.815, 0, 0), (61.231, 0, 0), (-105.481, 0, 0))
        mins = ToontownGlobals.FactoryLaffMinimums[3]
        for cogCourse in xrange(len(posList)):
            pos = posList[cogCourse]
            hpr = hprList[cogCourse]
            cogKart = DistributedCogKartAI.DistributedCogKartAI(
                self.air, cogCourse,
                pos[0], pos[1], pos[2], hpr[0], hpr[1], hpr[2],
                self.air.countryClubMgr, minLaff=mins[cogCourse])
            cogKart.generateWithRequired(self.zoneId)
            self.cogKarts.append(cogKart)

    def createCourseBoardingParty(self):
        cogKartIdList = []
        for cogKart in self.cogKarts:
            cogKartIdList.append(cogKart.doId)
        self.courseBoardingParty = DistributedBoardingPartyAI(self.air, cogKartIdList, 4)
        self.courseBoardingParty.generateWithRequired(self.zoneId)

    def createSuitPlanners(self):
        suitPlanner = DistributedSuitPlannerAI.DistributedSuitPlannerAI(self.air, self.zoneId)
        suitPlanner.generateWithRequired(self.zoneId)
        suitPlanner.d_setZoneId(self.zoneId)
        suitPlanner.initTasks()
        self.suitPlanners.append(suitPlanner)
        self.air.suitPlanners[self.zoneId] = suitPlanner
