from direct.distributed.DistributedObjectAI import *
from direct.showbase.DirectObject import *
import TopToonsGlobals

class DistributedTopToonsManagerAI(DirectObject):
    def __init__(self, air):
        self.air = air

        self.accept('topToonsManager-event', self.__handleEvent)

    def toonKilledBoss(self, av, boss):
        cat = {'VP': TopToonsGlobals.CAT_VP,
               'CFO': TopToonsGlobals.CAT_CFO,
               'CJ': TopToonsGlobals.CAT_CJ,
               'CEO': TopToonsGlobals.CAT_CEO}.get(boss, 0)
        self.__handleEvent(av.doId, cat, 1)

    def __handleEvent(self, *args): # avId, categories, score
        self.air.sendNetEvent('topToonsManager-AI-score-site', list(args))

from otp.ai.MagicWordGlobal import *
@magicWord(types=[int, int])
def topToon(score, cat=TopToonsGlobals._CAT_ALL):
    av = spellbook.getTarget()
    mgr = av.air.topToonsMgr
    if not mgr:
        return 'No manager!'

    if cat > TopToonsGlobals._CAT_ALL:
        return 'Max value: %d' % TopToonsGlobals._CAT_ALL

    messenger.send('topToonsManager-event', [av.doId, cat, score])