from otp.ai import MagicWordManager
from toontown.toonbase.ToontownGlobals import *
from direct.showbase.InputStateGlobal import inputState
from otp.ai.MagicWordGlobal import *
from otp.otpbase import OTPLocalizer
from toontown.toonbase import ToontownGlobals
from direct.gui.DirectGui import *
from toontown.toon.DistributedToon import *
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *

class ModPanel:

    def __init__(self, invoker):
            self.invoker = invoker
            self.setupButtons()