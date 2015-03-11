import toontown.minigame.MinigameCreatorAI
from toontown.distributed.ToontownInternalRepository import ToontownInternalRepository
from direct.distributed.PyDatagram import *
from otp.distributed.DistributedDirectoryAI import DistributedDirectoryAI
from otp.distributed.OtpDoGlobals import *

class ToontownUberRepository(ToontownInternalRepository):
    def __init__(self, baseChannel, serverId):
        ToontownInternalRepository.__init__(self, baseChannel, serverId, dcSuffix='UD')
        self.wantUD = config.GetBool('want-ud', True)

    def handleConnected(self):
        ToontownInternalRepository.handleConnected(self)
        if config.GetBool('want-ClientServicesManagerUD', self.wantUD):
            # Only generate the root object once, with the CSMUD.
            rootObj = DistributedDirectoryAI(self)
            rootObj.generateWithRequiredAndId(self.getGameDoId(), 0, 0)
        self.createGlobals()

    def createGlobals(self):
        """
        Create "global" objects.
        """

        self.csm = simbase.air.generateGlobalObject(OTP_DO_ID_CLIENT_SERVICES_MANAGER,
                                                    'ClientServicesManager')

        self.chatAgent = simbase.air.generateGlobalObject(OTP_DO_ID_CHAT_MANAGER,
                                                          'ChatAgent')

        self.friendsManager = simbase.air.generateGlobalObject(OTP_DO_ID_TTR_FRIENDS_MANAGER,
                                                               'TTRFriendsManager')

        if config.GetBool('want-parties', True):
            # want-parties overrides config for want-GlobalPartyManagerUD
            self.globalPartyMgr = self.generateGlobalIfWanted(OTP_DO_ID_GLOBAL_PARTY_MANAGER, 'GlobalPartyManager')
        else:
            self.globalPartyMgr = None

        self.deliveryManager = simbase.air.generateGlobalObject(OTP_DO_ID_TOONTOWN_DELIVERY_MANAGER, 'DistributedDeliveryManager')
