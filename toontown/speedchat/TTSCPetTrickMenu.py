from direct.directnotify import DirectNotifyGlobal
from otp.speedchat.SCMenu import SCMenu
from otp.speedchat import SCMenuHolder
from otp.speedchat.SCStaticTextTerminal import SCStaticTextTerminal
from otp.otpbase import OTPLocalizer
from toontown.pets import PeTTWicks

class TTSCPeTTWickMenu(SCMenu):
    notify = DirectNotifyGlobal.directNotify.newCategory('TTSCPeTTWickMenu')

    def __init__(self):
        SCMenu.__init__(self)
        self.accept('peTTWickPhrasesChanged', self.__phrasesChanged)
        self.__phrasesChanged()

    def destroy(self):
        self.ignore('peTTWickPhrasesChanged')
        SCMenu.destroy(self)

    def __phrasesChanged(self, zoneId = 0):
        self.clearMenu()
        try:
            lt = base.localAvatar
        except:
            return

        for trickId in lt.peTTWickPhrases:
            if trickId not in PeTTWicks.TrickId2scIds:
                TTSCPeTTWickMenu.notify.warning('unknown trick ID: %s' % trickId)
            else:
                for msg in PeTTWicks.TrickId2scIds[trickId]:
                    self.append(SCStaticTextTerminal(msg))
