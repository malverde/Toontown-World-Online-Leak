from toontown.safezone.GSSafeZoneLoader import GSSafeZoneLoader
from toontown.toonbase import ToontownGlobals
from toontown.hood.ToonHood import ToonHood


class GSHood(ToonHood):
    notify = directNotify.newCategory('GSHood')

    ID = ToontownGlobals.GoofySpeedway
    SAFEZONELOADER_CLASS = GSSafeZoneLoader
    STORAGE_DNA = 'phase_6/dna/storage_GS.pdna'
    SKY_FILE = 'phase_3.5/models/props/TT_sky'
    SPOOKY_SKY_FILE = 'phase_3.5/models/props/BR_sky'
    TITLE_COLOR = (1.0, 0.5, 0.4, 1.0)

    HOLIDAY_DNA = {
      ToontownGlobals.CRASHED_LEADERBOARD: ['phase_6/dna/crashed_leaderboard_storage_GS.pdna']}

    def enter(self, requestStatus):
        ToonHood.enter(self, requestStatus)

        base.localAvatar.chatMgr.chatInputSpeedChat.addKartRacingMenu()
        base.camLens.setNearFar(ToontownGlobals.SpeedwayCameraNear, ToontownGlobals.SpeedwayCameraFar)

    def exit(self):
        base.camLens.setNearFar(ToontownGlobals.DefaultCameraNear, ToontownGlobals.DefaultCameraFar)
        base.localAvatar.chatMgr.chatInputSpeedChat.removeKartRacingMenu()

        ToonHood.exit(self)
