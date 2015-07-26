#Embedded file name: toontown.catalog.CatalogManager
from direct.distributed import DistributedObject
from direct.directnotify import DirectNotifyGlobal

class CatalogManager(DistributedObject.DistributedObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('CatalogManager')
    neverDisable = 1

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)

    def generate(self):
        if base.cr.catalogManager != None:
            base.cr.catalogManager.delete()
        base.cr.catalogManager = self
        DistributedObject.DistributedObject.generate(self)
        if hasattr(base.localAvatar, 'catalogScheduleNextTime') and base.localAvatar.catalogScheduleNextTime == 0:
            self.d_startCatalog()

    def disable(self):
        base.cr.catalogManager = None
        DistributedObject.DistributedObject.disable(self)

    def delete(self):
        base.cr.catalogManager = None
        DistributedObject.DistributedObject.delete(self)

    def d_startCatalog(self):
        self.sendUpdate('startCatalog', [])
