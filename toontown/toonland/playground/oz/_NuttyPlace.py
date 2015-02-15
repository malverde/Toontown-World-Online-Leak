########################## THE TOON LAND PROJECT ##########################
# Filename: _NuttyPlace.py
# Created by: Cody/Fd Green Cat Fd (February 11th, 2013)
####
# Description:
#
# The Nutty Place added Python implementation.
####

from pandac.PandaModules import *

town_top_level = render.find('**/town_top_level')

def loadPineTree(parent, x, y, z, *scale):
    parentNp = loader.loadModel('phase_6/models/golf/outdoor_zone_entrance')
    treeNp = parentNp.find('**/outdoor_zone_entrance_tree1')
    if not scale:
        treeNp.setScale(0.5)
    else:
        treeNp.setScale(*scale)
    dummyNp = parent.attachNewNode('prop_outdoor_zone_tree')
    dummyNp.setPos((x + 10), (y - 5), z)
    treeNp.reparentTo(dummyNp)

_Z = 40
parentNp = loader.loadModel('phase_6/models/golf/golf_hub2')
for background in parentNp.findAllMatches('**/*background*'):
    background.reparentTo(town_top_level)
    background.setZ(_Z)
    _Z += 20

loadPineTree(town_top_level, 12, 2, 20, 0.6)
loadPineTree(town_top_level, -12, -16, 20, 0.7)
loadPineTree(town_top_level, -8, 6, 20, 0.5)
loadPineTree(town_top_level, 0, -10, 20, 0.4, 0.4, 0.5)
loadPineTree(town_top_level, 52, 35, 20, 0.8)
loadPineTree(town_top_level, -28, -22.5, 20, 0.8)
loadPineTree(town_top_level, -24, 0, 20, 0.4)
loadPineTree(town_top_level, -8, -3, 20, 0.4)
loadPineTree(town_top_level, -36, -101, 20, 0.8)
loadPineTree(town_top_level, -66, -66, 20, 0.8)
loadPineTree(town_top_level, -76, -30, 20, 1.0)
loadPineTree(town_top_level, -62, -84, 20, 0.6)
loadPineTree(town_top_level, 15, -50, 20, 0.5, 0.5, 0.6)
loadPineTree(town_top_level, 75, -15, 20, 0.9)
loadPineTree(town_top_level, 8, 70, 20, 1.0)
loadPineTree(town_top_level, 75, 15, 20, 0.7)
loadPineTree(town_top_level, -10, -130, 20, 1.0)
loadPineTree(town_top_level, 25, -122, 20, 0.8)

for picnicTable in town_top_level.findAllMatches('**/prop_picnic_table_OZ_DNARoot'):
    tableCloth = picnicTable.find('**/basket_locator')
    tableClothSphereNode = tableCloth.attachNewNode(CollisionNode('tablecloth_sphere'))
    tableClothSphereNode.node().addSolid(CollisionSphere(0, 0, 0, 5.5))

collisionMap = [((2, 0, 20), (0, 0, 0, 15)),
                ((-4, 0, 20), (0, 0, 0, 15)),
                ((-12, 0, 20), (0, 0, 0, 15)),
                ((-20, -4, 20), (0, 0, 0, 15)),
                ((-28, -10, 20), (0, 0, 0, 15)),
                ((-36, -12, 20), (0, 0, 0, 15)),
                ((-44, -12, 20), (0, 0, 0, 15)),
                ((50, 45, 20), (0, 0, 0, 15)),
                ((-45, -100, 20), (0, 0, 0, 15))]

for collision in collisionMap:
    dummyNp = town_top_level.attachNewNode('prop_outdoor_zone_tree_collision')
    dummyNp.setPos(collision[0][0], collision[0][1], collision[0][2])
    treeSphereNode = dummyNp.attachNewNode(CollisionNode('tree_sphere'))
    treeSphereNode.node().addSolid(CollisionSphere(collision[1][0], collision[1][1],
                                                   collision[1][2], collision[1][3]))