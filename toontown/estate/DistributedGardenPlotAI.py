from direct.directnotify import DirectNotifyGlobal
from otp.ai.MagicWordGlobal import *
from DistributedLawnDecorAI import DistributedLawnDecorAI
import GardenGlobals

class DistributedGardenPlotAI(DistributedLawnDecorAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedGardenPlotAI')
    
    def announceGenerate(self):
        DistributedLawnDecorAI.announceGenerate(self)
        self.plotType = GardenGlobals.whatCanBePlanted(self.ownerIndex, self.plot)
        self.__plantingAvId = 0
        
    def __initialSanityCheck(self, wantedType=None, forceOwner=False):
        if self.__plantingAvId:
            # Busy, silently ignore
            return
            
        avId = self.air.getAvatarIdFromSender()
        
        av = self.air.doId2do.get(avId)
        if not av:
            self.air.writeServerEvent('suspicious', avId, 'called DistributedGardenPlotAI method outside shard!')
            return
            
        if wantedType is not None and self.plotType != wantedType:
            self.air.writeServerEvent('suspicious', avId, 'called incorrect DistributedGardenPlotAI method!', plotType=self.plotType,
                                      wantedType=wantedType)
            return self.d_interactionDenied()
            
            
        if avId != self.ownerDoId and not forceOwner:
            self.air.writeServerEvent('suspicious', avId, 'called someone else\'s DistributedGardenPlotAI plant method!',
                                      ownerDoId=self.ownerDoId)
            return self.d_interactionDenied()
            
        return av

    def plantFlower(self, species, variety, usingSatanFlowerAll=0):
        av = self.__initialSanityCheck(GardenGlobals.FLOWER_TYPE if not usingSatanFlowerAll else None, usingSatanFlowerAll)
        if not av:
            return
            
        def invalid(problem):
            msg = 'tried to plant flower but something went wrong: %s' % problem
            self.notify.warning('%d %s' % (av.doId, msg))
            self.air.writeServerEvent('suspicious', av.doId, msg)
            if not usingSatanFlowerAll:
                return self.d_setMovie(GardenGlobals.MOVIE_PLANT_REJECTED)
            
        attr = GardenGlobals.PlantAttributes.get(species, {})
        if attr.get('plantType') != GardenGlobals.FLOWER_TYPE:
            return invalid('invalid species: %d' % species)
            
        if variety >= len(attr['varieties']):
            return invalid('invalid variety: %d' % variety)
            
        if not usingSatanFlowerAll:
            cost = len(GardenGlobals.Recipes[attr['varieties'][variety][0]]['beans'])
            av.takeMoney(cost)
            
            self.d_setMovie(GardenGlobals.MOVIE_PLANT)
        
        def _plant(task):
            flower = self.mgr.plantFlower(self.flowerIndex, species, variety, plot=self,
                                          ownerIndex=self.ownerIndex, plotId=self.plot,
                                          waterLevel=0)
            index = (0, 1, 2, 2, 2, 3, 3, 3, 4, 4)[self.flowerIndex]
            idx = (0, 0, 0, 1, 2, 0, 1, 2, 0, 1)[self.flowerIndex]
            flower.sendUpdate('setBoxDoId', [self.mgr._boxes[index].doId, idx])
            
            if not usingSatanFlowerAll:
                flower.d_setMovie(GardenGlobals.MOVIE_FINISHPLANTING, self.__plantingAvId)
                flower.d_setMovie(GardenGlobals.MOVIE_CLEAR, self.__plantingAvId)
                
            self.air.writeServerEvent('plant-flower', self.__plantingAvId, species=species, variety=variety,
                                      plot=self.plot, name=attr.get('name', 'unknown satan flower'))
            if task:
                return task.done
        
        if usingSatanFlowerAll:
            _plant(None)
       
        else:
            taskMgr.doMethodLater(7, _plant, self.uniqueName('do-plant'))
            
        self.__plantingAvId = av.doId
        return 1
            
    def plantGagTree(self, track, index):
        av = self.__initialSanityCheck(GardenGlobals.GAG_TREE_TYPE)
        if not av:
            return
            
        for i in xrange(index):
            if not self.mgr.hasTree(track, i):
                msg = 'tried to plant tree but an index is missing: %d' % index
                self.notify.warning('%d %s' % (av.doId, msg))
                self.air.writeServerEvent('suspicious', av.doId, msg)
                return self.d_setMovie(GardenGlobals.MOVIE_PLANT_REJECTED)
                
        if self.mgr.hasTree(track, index):
            msg = 'tried to plant tree but gag already planted'
            self.notify.warning('%d %s' % (av.doId, msg))
            self.air.writeServerEvent('suspicious', av.doId, msg)
            return self.d_setMovie(GardenGlobals.MOVIE_PLANT_REJECTED)
        
        if av.inventory.useItem(track, index) == -1:
            msg = 'tried to plant tree but not carrying selected gag'
            self.notify.warning('%d %s' % (av.doId, msg))
            self.air.writeServerEvent('suspicious', av.doId, msg)
            return self.d_setMovie(GardenGlobals.MOVIE_PLANT_REJECTED)
            
        av.d_setInventory(av.getInventory())
        self.d_setMovie(GardenGlobals.MOVIE_PLANT)
        
        def _plant(task):
            if not self.air:
                return
                
            tree = self.mgr.plantTree(self.treeIndex, track * 7 + index, plot=self, ownerIndex=self.ownerIndex,
                                      plotId=self.plot, pos=(self.getPos(), self.getH()))
            tree.d_setMovie(GardenGlobals.MOVIE_FINISHPLANTING, self.__plantingAvId)
            tree.d_setMovie(GardenGlobals.MOVIE_CLEAR, self.__plantingAvId)
            self.air.writeServerEvent('plant-tree', self.__plantingAvId, track=track, index=index, plot=self.plot)
            return task.done
        
        taskMgr.doMethodLater(7, _plant,  self.uniqueName('do-plant'))
        self.__plantingAvId = av.doId

    def plantStatuary(self, species):
        av = self.__initialSanityCheck(GardenGlobals.STATUARY_TYPE)
        if not av:
            return
            
        def invalid(problem):
            msg = 'tried to plant statuary but something went wrong: %s' % problem
            self.notify.warning('%d %s' % (av.doId, msg))
            self.air.writeServerEvent('suspicious', av.doId, msg)
            return self.d_setMovie(GardenGlobals.MOVIE_PLANT_REJECTED)
            
        attr = GardenGlobals.PlantAttributes.get(species, {})
        if attr.get('plantType') != GardenGlobals.STATUARY_TYPE:
            return invalid('invalid species: %d' % species)
          
        it = species - 100
        if it == 134:
            it = 135
            
        if not av.removeGardenItem(it, 1):
            return invalid('av doesn\'t own item: %d' % species)
            
        self.d_setMovie(GardenGlobals.MOVIE_PLANT)
            
        def _plant(task):
            if not self.air:
                return
                
            statuary = self.mgr.placeStatuary(self.mgr.S_pack(0, 0, species, 0), plot=self,
                                              ownerIndex=self.ownerIndex, plotId=self.plot,
                                              pos=(self.getPos(), self.getH()), generate=False)
            statuary.generateWithRequired(self.zoneId)
            statuary.d_setMovie(GardenGlobals.MOVIE_FINISHPLANTING, self.__plantingAvId)
            statuary.d_setMovie(GardenGlobals.MOVIE_CLEAR, self.__plantingAvId)
            self.air.writeServerEvent('plant-statuary', self.__plantingAvId, species=species, plot=self.plot)
            return task.done
            
        taskMgr.doMethodLater(7, _plant,  self.uniqueName('do-plant'))
        self.__plantingAvId = av.doId

    def plantToonStatuary(self, species, dnaCode):
        av = self.__initialSanityCheck(GardenGlobals.STATUARY_TYPE)
        if not av:
            return
            
        def invalid(problem):
            msg = 'tried to plant statuary but something went wrong: %s' % problem
            self.notify.warning('%d %s' % (av.doId, msg))
            self.air.writeServerEvent('suspicious', av.doId, msg)
            return self.d_setMovie(GardenGlobals.MOVIE_PLANT_REJECTED)
            
        attr = GardenGlobals.PlantAttributes.get(species, {})
        if attr.get('plantType') != GardenGlobals.STATUARY_TYPE:
            return invalid('invalid species: %d' % species)
            
        if not av.removeGardenItem(species - 100, 1):
            return invalid('av doesn\'t own item: %d' % species)
            
        self.d_setMovie(GardenGlobals.MOVIE_PLANT)
            
        def _plant(task):
            if not self.air:
                return
                
            statuary = self.mgr.placeStatuary(self.mgr.S_pack(dnaCode, 0, species, 0), plot=self,
                                              ownerIndex=self.ownerIndex, plotId=self.plot,
                                              pos=(self.getPos(), self.getH()), generate=False)
            statuary.generateWithRequired(self.zoneId)
            statuary.d_setMovie(GardenGlobals.MOVIE_FINISHPLANTING, self.__plantingAvId)
            self.air.writeServerEvent('plant-statuary', self.__plantingAvId, species=species, plot=self.plot)
            return task.done
            
        taskMgr.doMethodLater(7, _plant,  self.uniqueName('do-plant'))
        self.__plantingAvId = av.doId

    def plantNothing(self, burntBeans):
        av = self.__initialSanityCheck()
        if av:
            av.takeMoney(burntBeans)
   
@magicWord(category=CATEGORY_SYSADMIN, types=[int, int])
def satanFlowerAll(species=49, variety=0):
    invoker = spellbook.getInvoker()
    av = spellbook.getTarget()
    estate = av.air.estateManager._lookupEstate(av)
    
    if not estate:
        return 'Estate not found!'
        
    garden = estate.gardenManager.gardens.get(av.doId)
    if not garden:
        return 'Garden not found!'
    
    i = 0
    for obj in garden.objects.copy():
        if isinstance(obj, DistributedGardenPlotAI):
            if obj.plotType != GardenGlobals.FLOWER_TYPE:
                continue
                
            if not obj.plantFlower(species, variety, 1):
                return 'Error on plot %d' % i
                
            i += 1
            
    return '%d disgusting flowers planted' % i

@magicWord(category=CATEGORY_SYSADMIN)
def gibSpecials():
    av = spellbook.getTarget()
    av.gardenSpecials = []
    for x in (100, 101, 103, 105, 106, 107, 108, 130, 131, 135):
        av.addGardenItem(x, 99)
    