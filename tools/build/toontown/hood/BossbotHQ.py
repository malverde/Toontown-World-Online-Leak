from toontown.coghq.BossbotCogHQLoader import BossbotCogHQLoader
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
from toontown.hood.CogHood import CogHood
from toontown.hood import ZoneUtil


class BossbotHQ(CogHood):
    notify = directNotify.newCategory('BossbotHQ')

    ID = ToontownGlobals.BossbotHQ
    LOADER_CLASS = BossbotCogHQLoader

    def load(self):
        CogHood.load(self)

        self.sky.hide()

    def enter(self, requestStatus):
        CogHood.enter(self, requestStatus)

        base.localAvatar.setCameraFov(ToontownGlobals.CogHQCameraFov)
        base.camLens.setNearFar(ToontownGlobals.BossbotHQCameraNear, ToontownGlobals.BossbotHQCameraFar)

    def spawnTitleText(self, zoneId, floorNum=None):
        if ZoneUtil.isMintInteriorZone(zoneId):
            text = '%s\n%s' % (ToontownGlobals.StreetNames[zoneId][-1], TTLocalizer.MintFloorTitle % (floorNum + 1))
            self.doSpawnTitleText(text)
        else:
            CogHood.spawnTitleText(self, zoneId)
