from toontown.safezone.GZSafeZoneLoader import GZSafeZoneLoader
from toontown.toonbase import ToontownGlobals
from toontown.hood.ToonHood import ToonHood


class GZHood(ToonHood):
    notify = directNotify.newCategory('GZHood')

    ID = ToontownGlobals.GolfZone
    SAFEZONELOADER_CLASS = GZSafeZoneLoader
    STORAGE_DNA = 'phase_6/dna/storage_GZ.pdna'
    SKY_FILE = 'phase_3.5/models/props/TT_sky'
    SPOOKY_SKY_FILE = 'phase_3.5/models/props/BR_sky'
    TITLE_COLOR = (1.0, 0.5, 0.4, 1.0)

    def enter(self, requestStatus):
        ToonHood.enter(self, requestStatus)

        base.localAvatar.chatMgr.chatInputSpeedChat.addGolfMenu()
        base.camLens.setNearFar(ToontownGlobals.SpeedwayCameraNear, ToontownGlobals.SpeedwayCameraFar)

    def exit(self):
        base.camLens.setNearFar(ToontownGlobals.DefaultCameraNear, ToontownGlobals.DefaultCameraFar)
        base.localAvatar.chatMgr.chatInputSpeedChat.removeGolfMenu()

        ToonHood.exit(self)
