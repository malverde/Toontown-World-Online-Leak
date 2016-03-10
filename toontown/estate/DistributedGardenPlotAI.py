from toontown.estate.DistributedLawnDecorAI import DistributedLawnDecorAI
from toontown.estate import GardenGlobals


class DistributedGardenPlotAI(DistributedLawnDecorAI):
    notify = directNotify.newCategory('DistributedGardenPlotAI')

    def __init__(self, air, gardenManager, ownerIndex):
        DistributedLawnDecorAI.__init__(self, air, gardenManager, ownerIndex)

        self.occupier = GardenGlobals.EmptyPlot

    def plantGagTree(self, gagTrack, gagLevel):
        self.setMovie(GardenGlobals.MOVIE_PLANT, self.air.getAvatarIdFromSender())
        self.gardenManager.constructTree(self.plotIndex, gagTrack, gagLevel)

    def plantStatuary(self, species):
        self.setMovie(GardenGlobals.MOVIE_PLANT, self.air.getAvatarIdFromSender())
        self.gardenManager.constructStatuary(self.plotIndex, species)

    def plantToonStatuary(self, species, dnaCode):
        self.setMovie(GardenGlobals.MOVIE_PLANT, self.air.getAvatarIdFromSender())
        self.gardenManager.constructToonStatuary(self.plotIndex, species, dnaCode)

    def plantNothing(self, burntBeans):
        pass

    def movieDone(self):
        if self.movie == GardenGlobals.MOVIE_PLANT:
            self.gardenManager.plantingFinished(self.plotIndex)
            self.setMovie(GardenGlobals.MOVIE_FINISHREMOVING, self.air.getAvatarIdFromSender())
        elif self.movie == GardenGlobals.MOVIE_FINISHREMOVING:
            self.requestDelete()
        else:
            DistributedLawnDecorAI.movieDone(self)


    def construct(self, gardenData):
        DistributedLawnDecorAI.construct(self, gardenData)

    def pack(self, gardenData):
        gardenData.addUint8(self.occupier)
        DistributedLawnDecorAI.pack(self, gardenData)
