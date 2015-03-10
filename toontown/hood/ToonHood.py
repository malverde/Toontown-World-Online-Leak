from pandac.PandaModules import *
from toontown.toonbase.ToonBaseGlobal import *
from toontown.toonbase.ToontownGlobals import *
from toontown.distributed.ToontownMsgTypes import *
from direct.fsm import ClassicFSM, State
from toontown.minigame import Purchase
from otp.avatar import DistributedAvatar
from toontown.hood.Hood import Hood
from toontown.building import SuitInterior
from toontown.cogdominium import CogdoInterior
from toontown.toon.Toon import teleportDebug
from toontown.hood import SkyUtil


class ToonHood(Hood):
    notify = directNotify.newCategory('ToonHood')

    ID = None
    TOWNLOADER_CLASS = None
    SAFEZONELOADER_CLASS = None
    STORAGE_DNA = None
    SKY_FILE = None
    SPOOKY_SKY_FILE = None
    TITLE_COLOR = None

    HOLIDAY_DNA = {}

    def __init__(self, parentFSM, doneEvent, dnaStore, hoodId):
        Hood.__init__(self, parentFSM, doneEvent, dnaStore, hoodId)

        self.suitInteriorDoneEvent = 'suitInteriorDone'
        self.minigameDoneEvent = 'minigameDone'
        self.whiteFogColor = Vec4(0.8, 0.8, 0.8, 1)

        self.fsm = ClassicFSM.ClassicFSM('Hood', [State.State('start', self.enterStart, self.exitStart, ['townLoader', 'safeZoneLoader']),
         State.State('townLoader', self.enterTownLoader, self.exitTownLoader, ['quietZone',
          'safeZoneLoader',
          'suitInterior',
          'cogdoInterior']),
         State.State('safeZoneLoader', self.enterSafeZoneLoader, self.exitSafeZoneLoader, ['quietZone',
          'suitInterior',
          'cogdoInterior',
          'townLoader',
          'minigame']),
         State.State('purchase', self.enterPurchase, self.exitPurchase, ['quietZone', 'minigame', 'safeZoneLoader']),
         State.State('suitInterior', self.enterSuitInterior, self.exitSuitInterior, ['quietZone', 'townLoader', 'safeZoneLoader']),
         State.State('cogdoInterior', self.enterCogdoInterior, self.exitCogdoInterior, ['quietZone', 'townLoader', 'safeZoneLoader']),
         State.State('minigame', self.enterMinigame, self.exitMinigame, ['purchase']),
         State.State('quietZone', self.enterQuietZone, self.exitQuietZone, ['safeZoneLoader',
          'townLoader',
          'suitInterior',
          'cogdoInterior',
          'minigame']),
         State.State('final', self.enterFinal, self.exitFinal, [])], 'start', 'final')
        self.fsm.enterInitialState()

        # Load content pack ambience settings:
        ambience = contentPacksMgr.getAmbience('general')

        color = ambience.get('underwater-color')
        if color is not None:
            try:
                self.underwaterColor = Vec4(color['r'], color['g'], color['b'], color['a'])
            except Exception, e:
                raise ContentPackError(e)
        else:
            self.underwaterColor = None

        # Until we cleanup Hood, we will need to define some variables
        self.id = self.ID
        self.storageDNAFile = self.STORAGE_DNA
        self.holidayStorageDNADict = self.HOLIDAY_DNA
        self.skyFile = self.SKY_FILE
        self.spookySkyFile = self.SPOOKY_SKY_FILE
        self.titleColor = self.TITLE_COLOR

    def load(self):
        Hood.load(self)

        self.parentFSM.getStateNamed(self.__class__.__name__).addChild(self.fsm)

    def unload(self):
        self.parentFSM.getStateNamed(self.__class__.__name__).removeChild(self.fsm)

        Hood.unload(self)

    def loadLoader(self, requestStatus):
        loaderName = requestStatus['loader']
        if loaderName == 'safeZoneLoader':
            self.loader = self.SAFEZONELOADER_CLASS(self, self.fsm.getStateNamed('safeZoneLoader'), self.loaderDoneEvent)
            self.loader.load()
        elif loaderName == 'townLoader':
            self.loader = self.TOWNLOADER_CLASS(self, self.fsm.getStateNamed('townLoader'), self.loaderDoneEvent)
            self.loader.load(requestStatus['zoneId'])

    def enterTownLoader(self, requestStatus):
        teleportDebug(requestStatus, 'ToonHood.enterTownLoader, status=%s' % (requestStatus,))
        self.accept(self.loaderDoneEvent, self.handleTownLoaderDone)
        self.loader.enter(requestStatus)
        self.spawnTitleText(requestStatus['zoneId'])

    def exitTownLoader(self):
        taskMgr.remove('titleText')
        self.hideTitleText()
        self.ignore(self.loaderDoneEvent)
        self.loader.exit()
        self.loader.unload()
        del self.loader

    def handleTownLoaderDone(self):
        doneStatus = self.loader.getDoneStatus()
        teleportDebug(doneStatus, 'handleTownLoaderDone, doneStatus=%s' % (doneStatus,))
        if self.isSameHood(doneStatus):
            teleportDebug(doneStatus, 'same hood')
            self.fsm.request('quietZone', [doneStatus])
        else:
            teleportDebug(doneStatus, 'different hood')
            self.doneStatus = doneStatus
            messenger.send(self.doneEvent)

    def enterPurchase(self, pointsAwarded, playerMoney, playerIds, playerStates, remain, metagameRound = -1, votesArray = None):
        messenger.send('enterSafeZone')
        DistributedAvatar.DistributedAvatar.HpTextEnabled = 0
        base.localAvatar.laffMeter.start()
        self.purchaseDoneEvent = 'purchaseDone'
        self.accept(self.purchaseDoneEvent, self.handlePurchaseDone)
        self.purchase = Purchase.Purchase(base.localAvatar, pointsAwarded, playerMoney, playerIds, playerStates, remain, self.purchaseDoneEvent, metagameRound, votesArray)
        self.purchase.load()
        self.purchase.enter()

    def exitPurchase(self):
        messenger.send('exitSafeZone')
        DistributedAvatar.DistributedAvatar.HpTextEnabled = 1
        base.localAvatar.laffMeter.stop()
        self.ignore(self.purchaseDoneEvent)
        self.purchase.exit()
        self.purchase.unload()
        del self.purchase

    def handlePurchaseDone(self):
        doneStatus = self.purchase.getDoneStatus()
        if doneStatus['where'] == 'playground':
            self.fsm.request('quietZone', [{'loader': 'safeZoneLoader',
              'where': 'playground',
              'how': 'teleportIn',
              'hoodId': self.hoodId,
              'zoneId': self.hoodId,
              'shardId': None,
              'avId': -1}])
        elif doneStatus['loader'] == 'minigame':
            self.fsm.request('minigame')
        else:
            self.notify.error('handlePurchaseDone: unknown mode')
        return

    def enterSuitInterior(self, requestStatus = None):
        self.placeDoneEvent = 'suit-interior-done'
        self.acceptOnce(self.placeDoneEvent, self.handleSuitInteriorDone)
        self.place = SuitInterior.SuitInterior(self, self.fsm, self.placeDoneEvent)
        self.place.load()
        self.place.enter(requestStatus)
        base.cr.playGame.setPlace(self.place)

    def exitSuitInterior(self):
        self.ignore(self.placeDoneEvent)
        del self.placeDoneEvent
        self.place.exit()
        self.place.unload()
        self.place = None
        base.cr.playGame.setPlace(self.place)

    def handleSuitInteriorDone(self):
        doneStatus = self.place.getDoneStatus()
        if self.isSameHood(doneStatus):
            self.fsm.request('quietZone', [doneStatus])
        else:
            self.doneStatus = doneStatus
            messenger.send(self.doneEvent)

    def enterCogdoInterior(self, requestStatus = None):
        self.placeDoneEvent = 'cogdo-interior-done'
        self.acceptOnce(self.placeDoneEvent, self.handleCogdoInteriorDone)
        self.place = CogdoInterior.CogdoInterior(self, self.fsm, self.placeDoneEvent)
        self.place.load()
        self.place.enter(requestStatus)
        base.cr.playGame.setPlace(self.place)

    def exitCogdoInterior(self):
        self.ignore(self.placeDoneEvent)
        del self.placeDoneEvent
        self.place.exit()
        self.place.unload()
        self.place = None
        base.cr.playGame.setPlace(self.place)

    def handleCogdoInteriorDone(self):
        doneStatus = self.place.getDoneStatus()
        if self.isSameHood(doneStatus):
            self.fsm.request('quietZone', [doneStatus])
        else:
            self.doneStatus = doneStatus
            messenger.send(self.doneEvent)

    def enterMinigame(self, ignoredParameter = None):
        messenger.send('enterSafeZone')
        DistributedAvatar.DistributedAvatar.HpTextEnabled = 0
        base.localAvatar.laffMeter.start()
        base.cr.forbidCheesyEffects(1)
        self.acceptOnce(self.minigameDoneEvent, self.handleMinigameDone)

    def exitMinigame(self):
        messenger.send('exitSafeZone')
        DistributedAvatar.DistributedAvatar.HpTextEnabled = 1
        base.localAvatar.laffMeter.stop()
        base.cr.forbidCheesyEffects(0)
        self.ignore(self.minigameDoneEvent)
        minigameState = self.fsm.getStateNamed('minigame')
        for childFSM in minigameState.getChildren():
            minigameState.removeChild(childFSM)

    def handleMinigameDone(self):
        pass

    def skyTrack(self, task):
        return SkyUtil.cloudSkyTrack(task)

    def startSky(self):
        if not self.sky.getTag('sky') == 'Regular':
            self.endSpookySky()
        SkyUtil.startCloudSky(self)

    def startSpookySky(self):
        if hasattr(self, 'sky') and self.sky:
            self.stopSky()
        self.sky = loader.loadModel(self.spookySkyFile)
        self.sky.setTag('sky', 'Halloween')
        self.sky.setScale(1.0)
        self.sky.setDepthTest(0)
        self.sky.setDepthWrite(0)
        self.sky.setColor(0.5, 0.5, 0.5, 1)
        self.sky.setBin('background', 100)
        self.sky.setFogOff()
        self.sky.reparentTo(camera)
        self.sky.setTransparency(TransparencyAttrib.MDual, 1)
        fadeIn = self.sky.colorScaleInterval(1.5, Vec4(1, 1, 1, 1), startColorScale=Vec4(1, 1, 1, 0.25), blendType='easeInOut')
        fadeIn.start()
        self.sky.setZ(0.0)
        self.sky.setHpr(0.0, 0.0, 0.0)
        ce = CompassEffect.make(NodePath(), CompassEffect.PRot | CompassEffect.PZ)
        self.sky.node().setEffect(ce)

    def setUnderwaterFog(self):
        if base.wantFog:
            self.fog.setColor(self.underwaterColor)
            self.fog.setLinearRange(0.1, 100.0)
            render.setFog(self.fog)
            self.sky.setFog(self.fog)

    def setWhiteFog(self):
        if base.wantFog:
            self.fog.setColor(self.whiteFogColor)
            self.fog.setLinearRange(0.0, 400.0)
            render.clearFog()
            render.setFog(self.fog)
            self.sky.clearFog()
            self.sky.setFog(self.fog)

    def setNoFog(self):
        if base.wantFog:
            render.clearFog()
            self.sky.clearFog()
