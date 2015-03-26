from direct.distributed.DistributedObject import DistributedObject
import random

from toontown.building import  ToonInteriorColors
from toontown.dna.DNAParser import DNADoor
from toontown.hood import ZoneUtil
from toontown.toon.DistributedNPCToonBase import DistributedNPCToonBase


class DistributedLibraryInterior(DistributedObject):
    def announceGenerate(self):
        DistributedObject.announceGenerate(self)

        self.interior = loader.loadModel('phase_4/models/modules/ttc_library_interior.bam')
        self.interior.reparentTo(render)

        generator = random.Random()
        generator.seed(self.zoneId)
        self.replaceRandom(self.interior, generator=generator)

        doorOrigin = self.interior.find('**/door_origin;+s')
        doorOrigin.setScale(0.8)
        doorOrigin.setY(doorOrigin, -0.025)

        door = self.cr.playGame.dnaStore.findNode('door_double_round_ur')
        doorNodePath = door.copyTo(doorOrigin)

        hoodId = ZoneUtil.getCanonicalHoodId(self.zoneId)
        doorColor = ToonInteriorColors.colors[hoodId]['TI_door'][0]
        DNADoor.setupDoor(
            doorNodePath, self.interior, doorOrigin, self.cr.playGame.dnaStore,
            str(self.block), doorColor)

        doorFrame = doorNodePath.find('door_double_round_ur_flat')
        doorFrame.wrtReparentTo(self.interior)
        doorFrame.setColor(doorColor)

        for npcToon in self.cr.doFindAllInstances(DistributedNPCToonBase):
            npcToon.initToonState()

    def disable(self):
        self.interior.removeNode()
        del self.interior

        DistributedObject.disable(self)

    def setZoneIdAndBlock(self, zoneId, block):
        self.zoneId = zoneId
        self.block = block

    def replaceRandom(self, root, generator=random):
        for nodePath in root.findAllMatches('**/random_???_*'):
            name = nodePath.getName()

            category = name[11:]

            if name[7] in ('m', 't'):
                codeCount = self.cr.playGame.dnaStore.getNumCatalogCodes(category)
                index = generator.randint(0, codeCount - 1)
                code = self.cr.playGame.dnaStore.getCatalogCode(category, index)
                if name[7] == 'm':
                    _nodePath = self.cr.playGame.dnaStore.findNode(code).copyTo(nodePath)
                    if name[8] == 'r':
                        self.replaceRandom(_nodePath, generator=generator)
                else:
                    texture = self.cr.playGame.dnaStore.findTexture(code)
                    nodePath.setTexture(texture, 100)
                    _nodePath = nodePath

            if name[8] == 'c':
                hoodId = ZoneUtil.getCanonicalHoodId(self.zoneId)
                colors = ToonInteriorColors.colors[hoodId]
                _nodePath.setColorScale(generator.choice(colors[category]))
