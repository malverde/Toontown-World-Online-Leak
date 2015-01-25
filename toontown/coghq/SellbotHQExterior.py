from direct.directnotify import DirectNotifyGlobal
from toontown.coghq import CogHQExterior
from toontown.dna.DNAStorage import DNAStorage
class SellbotHQExterior(CogHQExterior.CogHQExterior):
    notify = DirectNotifyGlobal.directNotify.newCategory('SellbotHQExterior')
    dnaFile = 'phase_9/dna/cog_hq_sellbot_sz.xml'

    def enter(self, requestStatus):
        CogHQExterior.CogHQExterior.enter(self, requestStatus)
        self.loader.hood.startSky()
#revert all that crap i did
    def exit(self):
        self.loader.hood.stopSky()
        CogHQExterior.CogHQExterior.exit(self)
