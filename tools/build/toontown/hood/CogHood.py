from direct.fsm import ClassicFSM, State
from toontown.toonbase import ToontownGlobals
from toontown.hood.Hood import Hood


class CogHood(Hood):
    notify = directNotify.newCategory('CogHood')

    ID = None
    LOADER_CLASS = None
    SKY_FILE = 'phase_9/models/cogHQ/cog_sky'
    TITLE_COLOR = (0.5, 0.5, 0.5, 1.0)

    def __init__(self, parentFSM, doneEvent, dnaStore, hoodId):
        Hood.__init__(self, parentFSM, doneEvent, dnaStore, hoodId)

        self.fsm = ClassicFSM.ClassicFSM('Hood', [State.State('start', self.enterStart, self.exitStart, ['cogHQLoader']),
         State.State('cogHQLoader', self.enterCogHQLoader, self.exitCogHQLoader, ['quietZone']),
         State.State('quietZone', self.enterQuietZone, self.exitQuietZone, ['cogHQLoader']),
         State.State('final', self.enterFinal, self.exitFinal, [])], 'start', 'final')
        self.fsm.enterInitialState()

        # Until Hood is cleaned up, we will need to define some variables:

        self.id = self.ID
        self.storageDNAFile = None
        self.skyFile = self.SKY_FILE
        self.titleColor = self.TITLE_COLOR

    def load(self):
        Hood.load(self)

        skyInner = self.sky.find('**/InnerGroup')
        skyMiddle = self.sky.find('**/MiddleGroup')
        skyOuter = self.sky.find('**/OutterSky')

        if not skyOuter.isEmpty():
            skyOuter.setBin('background', 0)
        if not skyMiddle.isEmpty():
            skyMiddle.setDepthWrite(0)
            skyMiddle.setBin('background', 10)
        if not skyInner.isEmpty():
            skyInner.setDepthWrite(0)
            skyInner.setBin('background', 20)

        self.parentFSM.getStateNamed(self.__class__.__name__).addChild(self.fsm)

    def unload(self):
        self.parentFSM.getStateNamed(self.__class__.__name__).removeChild(self.fsm)

        Hood.unload(self)

    def loadLoader(self, requestStatus):
        loaderName = requestStatus['loader']
        if loaderName == 'cogHQLoader':
            self.loader = self.LOADER_CLASS(self, self.fsm.getStateNamed('cogHQLoader'), self.loaderDoneEvent)
            self.loader.load(requestStatus['zoneId'])

    def enterCogHQLoader(self, requestStatus):
        self.accept(self.loaderDoneEvent, self.handleCogHQLoaderDone)
        self.loader.enter(requestStatus)

    def exitCogHQLoader(self):
        self.ignore(self.loaderDoneEvent)
        self.loader.exit()
        self.loader.unload()
        del self.loader

    def handleCogHQLoaderDone(self):
        doneStatus = self.loader.getDoneStatus()
        if self.isSameHood(doneStatus):
            self.fsm.request('quietZone', [doneStatus])
        else:
            self.doneStatus = doneStatus
            messenger.send(self.doneEvent)

    def exit(self):
        base.localAvatar.setCameraFov(ToontownGlobals.DefaultCameraFov)
        base.camLens.setNearFar(ToontownGlobals.DefaultCameraNear, ToontownGlobals.DefaultCameraFar)

        Hood.exit(self)
