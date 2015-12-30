from direct.directnotify import DirectNotifyGlobal
from DistributedLawnDecorAI import DistributedLawnDecorAI

import GardenGlobals
import time

FOUR_DAYS = 86400 * 4

class DistributedStatuaryAI(DistributedLawnDecorAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedStatuaryAI")
    
    def calculate(self, lastCheck):
        self.attributes = GardenGlobals.PlantAttributes[self.index]
        self.growthThresholds = self.attributes.get('growthThresholds', (0, 0))
        
        now = int(time.time())
        self.lastCheck = lastCheck
        if self.lastCheck == 0:
            self.lastCheck = now

        self.growthLevel = min((now - self.lastCheck) // FOUR_DAYS, self.growthThresholds[-1] + 1)
        self.update()

    def getTypeIndex(self):
        return self.index

    def getWaterLevel(self):
        return 1

    def getGrowthLevel(self):
        return self.growthLevel
        
    def getOptional(self):
        return self.data

    def update(self):
        self.mgr.data['statuary'] = self.mgr.S_pack(self.data, self.lastCheck, self.index, self.growthLevel)
        self.mgr.update()
        
    def removeItem(self):
        avId = self.air.getAvatarIdFromSender()
        self.d_setMovie(GardenGlobals.MOVIE_REMOVE)
        
        def _remove(task):
            if not self.air:
                return
                
            plot = self.mgr.placePlot(-1)
            plot.setPlot(self.plot)
            plot.setPos(self.getPos())
            plot.setH(self.getH())
            plot.setOwnerIndex(self.ownerIndex)
            plot.generateWithRequired(self.zoneId)
            
            self.air.writeServerEvent('remove-statuary', avId, plot=self.plot)
            self.requestDelete()
            
            self.mgr.objects.remove(self)

            self.mgr.data['statuary'] = 0
            self.mgr.update()
            
            return task.done
        
        taskMgr.doMethodLater(7, _remove,  self.uniqueName('do-remove'))
        