from toontown.toonbase import ToontownGlobals

ANY_LAFF = 138
ANY_LEVEL = 13
ANY_TYPE = 1
COG = 0
V2COG = 1
SKELECOG = 2

class FriendAchievement():

    def __init__(self, neededFriends=1):
        self.neededFriends = neededFriends

    def hasComplete(self, av):
        avatarsFriends = av.getFriendsList()

        if len(avatarsFriends) >= self.neededFriends:
            return 1

        return 0

class TrolleyAchievement():

    def hasComplete(self, av):
        return 1

class SuitsAchievement():

    def __init__(self, neededSuits=1, neededType=ANY_TYPE, revive=0, skele=0):
        self.neededSuits = neededSuits
        self.neededType = neededType
        self.needRevive = revive
        self.needSkele = skele

    def hasComplete(self, av):
        avatarsRadar = av.getCogCount()

        #ToontownGlobals.cog

        return 0

class EstateAchievement():

    def hasComplete(self, av):
        return 1

class VPAchievement():

    def __init__(self, neededLaff=ANY_LAFF, solo=False):
        self.neededLaff = neededLaff
        self.solo = solo

    def hasComplete(self, laff, solo):
        complete = 1

        if self.neededLaff != ANY_LAFF:
            if laff:
                complete = 1
            else:
                complete = 0

        if self.solo:
            if solo:
                complete = 1
            else:
                complete = 0

        return complete

class CFOAchievement():

    def __init__(self, neededLaff=ANY_LAFF, solo=False):
        self.neededLaff = neededLaff
        self.solo = solo

    def hasComplete(self, laff, solo):
        complete = 1

        if self.neededLaff != ANY_LAFF:
            if laff:
                complete = 1
            else:
                complete = 0

        if self.solo:
            if solo:
                complete = 1
            else:
                complete = 0

        return complete

class CJAchievement():

    def __init__(self, neededLaff=ANY_LAFF, solo=False):
        self.neededLaff = neededLaff
        self.solo = solo

    def hasComplete(self, laff, solo):
        complete = 1

        if self.neededLaff != ANY_LAFF:
            if laff:
                complete = 1
            else:
                complete = 0

        if self.solo:
            if solo:
                complete = 1
            else:
                complete = 0

        return complete

class CEOAchievement():

    def __init__(self, neededLaff=ANY_LAFF, solo=False):
        self.neededLaff = neededLaff
        self.solo = solo

    def hasComplete(self, laff, solo):
        complete = 1

        if self.neededLaff != ANY_LAFF:
            if laff:
                complete = 1
            else:
                complete = 0

        if self.solo:
            if solo:
                complete = 1
            else:
                complete = 0

        return complete

AchievementsDict = (FriendAchievement(),
                    FriendAchievement(neededFriends=10),
                    FriendAchievement(neededFriends=50),
                    TrolleyAchievement(),
                    EstateAchievement(),
                    VPAchievement(),
                    VPAchievement(neededLaff=1),
                    VPAchievement(solo=True),
                    VPAchievement(neededLaff=1, solo=True),
                    CFOAchievement(),
                    CFOAchievement(neededLaff=1),
                    CFOAchievement(solo=True),
                    CFOAchievement(neededLaff=1, solo=True),
                    CJAchievement(),
                    CJAchievement(neededLaff=1),
                    CJAchievement(solo=True),
                    CJAchievement(neededLaff=1, solo=True),
                    CEOAchievement(),
                    CEOAchievement(neededLaff=1),
                    CEOAchievement(solo=True),
                    CEOAchievement(neededLaff=1, solo=True))

type2AchievementIds = {FriendAchievement: [0, 1, 2],
                       TrolleyAchievement: [3],
                       EstateAchievement: [4],
                       VPAchievement: [5, 6, 7, 8]}

def getAchievementsOfType(type):
    return type2AchievementIds.get(type)
