from toontown.achievements import Achievements

class AchievementsManagerAI():
    def __init__(self, air):
        self.air = air

        self.vpLaffPlayers = []
        self.vpSoloPlayers = []

    def toonMadeFriend(self, avId):
        av = self.air.doId2do.get(avId)
        if not av:
            return

        possibleAchievements = Achievements.getAchievementsOfType(Achievements.FriendAchievement)

        for achievementId in possibleAchievements:
            if not achievementId in av.getAchievements():
                if Achievements.AchievementsDict[achievementId].hasComplete(av):
                    av.addAchievement(achievementId)

    def toonPlayedMinigame(self, av):
        possibleAchievements = Achievements.getAchievementsOfType(Achievements.TrolleyAchievement)

        for achievementId in possibleAchievements:
            if not achievementId in av.getAchievements():
                if Achievements.AchievementsDict[achievementId].hasComplete(av):
                    av.addAchievement(achievementId)

    def toonsStartedVP(self, toons):
        print toons

        for avId in toons:
            av = self.air.doId2do.get(int(avId))
            if not av:
                continue

            if av.getHp() == 1:
                print '1 Laff!'
                self.vpLaffPlayers.append(int(avId))

        if len(toons) == 1:
            print 'SOLO! %s'%(int(avId))
            self.vpSoloPlayers.append(int(toons[0]))

    def toonsFinishedVP(self, toons):
        possibleAchievements = Achievements.getAchievementsOfType(Achievements.VPAchievement)

        for avId in toons:
            av = self.air.doId2do.get(int(avId))
            if not av:
                continue

            for achievementId in possibleAchievements:
                if not achievementId in av.getAchievements():
                    solo = avId in self.vpSoloPlayers
                    laff = avId in self.vpLaffPlayers

                    if Achievements.AchievementsDict[achievementId].hasComplete(laff, solo):
                        av.addAchievement(achievementId)

            while avId in self.vpSoloPlayers:
                self.vpSoloPlayers.remove(avId)

            while avId in self.vpLaffPlayers:
                self.vpLaffPlayers.remove(avId)

    def toonGotQuest(self, avId):
        av = self.air.doId2do.get(avId)
        if not av:
            return
