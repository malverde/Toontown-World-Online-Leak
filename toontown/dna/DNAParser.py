if config.GetBool('use-libpandadna', False):
    import libpandadna

    from libpandadna import *
    from libpandadna.DNAAnimBuilding import *
    from libpandadna.DNAAnimProp import *
    from libpandadna.DNACornice import *
    from libpandadna.DNADoor import *
    from libpandadna.DNAFlatBuilding import *
    from libpandadna.DNAFlatDoor import *
    from libpandadna.DNAGroup import *
    from libpandadna.DNAInteractiveProp import *
    from libpandadna.DNALandmarkBuilding import *
    from libpandadna.DNANode import *
    from libpandadna.DNAProp import *
    from libpandadna.DNASign import *
    from libpandadna.DNASignBaseline import *
    from libpandadna.DNASignGraphic import *
    from libpandadna.DNASignText import *
    from libpandadna.DNAStreet import *
    from libpandadna.DNAWall import *
    from libpandadna.DNAWindows import *
    
    from libpandadna.DNAStorage import *
    from libpandadna.DNALoader import *
    
    from libpandadna.DNASuitEdge import *
    from libpandadna.DNASuitPoint import *
    from libpandadna.DNASuitPath import *
    
    from libpandadna.DNABattleCell import *

    def loadDNAFile(*a, **kw):
        return loader.loadDNAFile(*a, **kw)
        
    from pandac.PandaModules import *
    def setupDoor(doorNodePath, parentNode, doorOrigin, dnaStore, block, color):
        doorNodePath.setPosHprScale(doorOrigin, (0, 0, 0), (0, 0, 0), (1, 1, 1))
        doorNodePath.setColor(color, 0)
        
        leftHole = doorNodePath.find('door_*_hole_left')
        leftHole.setName('doorFrameHoleLeft')
        
        rightHole = doorNodePath.find('door_*_hole_right')
        rightHole.setName('doorFrameHoleRight')
        
        leftDoor = doorNodePath.find('door_*_left')
        leftDoor.setName('leftDoor')
        
        rightDoor = doorNodePath.find('door_*_right')
        rightDoor.setName('rightDoor')
        
        doorFlat = doorNodePath.find('door_*_flat')
        
        leftHole.wrtReparentTo(doorFlat, 0)
        rightHole.wrtReparentTo(doorFlat, 0)
        
        doorFlat.setEffect(DecalEffect.make())
        
        rightDoor.wrtReparentTo(parentNode, 0)
        leftDoor.wrtReparentTo(parentNode, 0)

        rightDoor.setColor(color, 0)
        leftDoor.setColor(color, 0)
        
        leftHole.setColor((0, 0, 0, 1), 0)
        rightHole.setColor((0, 0, 0, 1), 0)

        doorTrigger = doorNodePath.find('door_*_trigger')
        doorTrigger.setScale(2, 2, 2)
        doorTrigger.wrtReparentTo(parentNode, 0)
        doorTrigger.setName('door_trigger_' + block) 

else:

 import xml.sax

 class DNAError(Exception): pass 
 class DNAParseError(DNAError): pass

 elementRegistry = {}
 def registerElement(element):
    elementRegistry[element.TAG] = element

 class DNASaxHandler(xml.sax.ContentHandler):
    def __init__(self):
        xml.sax.ContentHandler.__init__(self)

        self.stack = []
        self.root = None

    def startElement(self, tag, attrs):
        if self.stack:
            parent = self.stack[-1]
            parentTag = parent.TAG
        else:
            parent = None
            parentTag = None

        element = elementRegistry.get(tag)
        if not element:
            raise DNAParseError('Unknown element type: ' + tag)

        if parentTag not in element.PARENTS:
            raise DNAParseError('Cannot put %s below %s element' % (tag, parentTag))

        element = element(**attrs)
        self.stack.append(element)
        element.reparentTo(parent)

        if not self.root:
            self.root = element

    def endElement(self, tag):
        self.stack.pop(-1)

    def characters(self, chars):
        if not self.stack:
            return

        self.stack[-1].handleText(chars)

 def parse(stream):
    handler = DNASaxHandler()
    xml.sax.parse(stream, handler)
    return handler.root
