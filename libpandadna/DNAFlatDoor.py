from panda3d.core import NodePath, DecalEffect
import DNADoor

class DNAFlatDoor(DNADoor.DNADoor):
    COMPONENT_CODE = 18

    def traverse(self, nodePath, dnaStorage):
        node = dnaStorage.findNode(self.getCode())
        node = node.copyTo(nodePath, 0)
        node.setScale(NodePath(), (1, 1, 1))
        node.setPosHpr((0.5, 0, 0), (0, 0, 0))
        node.setColor(self.getColor())
        node.getNode(0).setEffect(DecalEffect.make())
        node.flattenStrong()