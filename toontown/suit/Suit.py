from direct.actor import Actor
from otp.avatar import Avatar
import SuitDNA
from toontown.toonbase import ToontownGlobals
from pandac.PandaModules import *
from toontown.battle import SuitBattleGlobals
from toontown.nametag import NametagGlobals
from direct.task.Task import Task
from toontown.battle import BattleProps
from toontown.toonbase import TTLocalizer
from pandac.PandaModules import VirtualFileMountHTTP, VirtualFileSystem, Filename, DSearchPath
from direct.showbase import AppRunnerGlobal
from toontown.nametag import NametagGroup
import string
import os
from toontown.suit import SuitGlobals

aSize = 6.06
bSize = 5.29
cSize = 4.14
SuitDialogArray = []
SkelSuitDialogArray = []
AllSuits = (('walk', 'walk'), ('run', 'walk'), ('neutral', 'neutral'))
AllSuitsMinigame = (('victory', 'victory'),
 ('flail', 'flailing'),
 ('tug-o-war', 'tug-o-war'),
 ('slip-backward', 'slip-backward'),
 ('slip-forward', 'slip-forward'))
AllSuitsTutorialBattle = (('lose', 'lose'), ('pie-small-react', 'pie-small'), ('squirt-small-react', 'squirt-small'))
AllSuitsBattle = (('drop-react', 'anvil-drop'),
 ('flatten', 'drop'),
 ('sidestep-left', 'sidestep-left'),
 ('sidestep-right', 'sidestep-right'),
 ('squirt-large-react', 'squirt-large'),
 ('landing', 'landing'),
 ('reach', 'walknreach'),
 ('rake-react', 'rake'),
 ('hypnotized', 'hypnotize'),
 ('soak', 'soak'),
 ('lured', 'lured'))
SuitsCEOBattle = (('sit', 'sit'),
 ('sit-eat-in', 'sit-eat-in'),
 ('sit-eat-loop', 'sit-eat-loop'),
 ('sit-eat-out', 'sit-eat-out'),
 ('sit-angry', 'sit-angry'),
 ('sit-hungry-left', 'leftsit-hungry'),
 ('sit-hungry-right', 'rightsit-hungry'),
 ('sit-lose', 'sit-lose'),
 ('tray-walk', 'tray-walk'),
 ('tray-neutral', 'tray-neutral'),
 ('sit-lose', 'sit-lose'))
f = (('throw-paper', 'throw-paper', 3.5), ('phone', 'phone', 3.5), ('shredder', 'shredder', 3.5))
p = (('pencil-sharpener', 'pencil-sharpener', 5),
 ('pen-squirt', 'pen-squirt', 5),
 ('hold-eraser', 'hold-eraser', 5),
 ('finger-wag', 'finger-wag', 5),
 ('hold-pencil', 'hold-pencil', 5))
ym = (('throw-paper', 'throw-paper', 5),
 ('golf-club-swing', 'golf-club-swing', 5),
 ('magic3', 'magic3', 5),
 ('rubber-stamp', 'rubber-stamp', 5),
 ('smile', 'smile', 5))
mm = (('speak', 'speak', 5),
 ('effort', 'effort', 5),
 ('magic1', 'magic1', 5),
 ('pen-squirt', 'fountain-pen', 5),
 ('finger-wag', 'finger-wag', 5))
ds = (('magic1', 'magic1', 5),
 ('magic2', 'magic2', 5),
 ('throw-paper', 'throw-paper', 5),
 ('magic3', 'magic3', 5))
hh = (('pen-squirt', 'fountain-pen', 7),
 ('glower', 'glower', 5),
 ('throw-paper', 'throw-paper', 5),
 ('magic1', 'magic1', 5),
 ('roll-o-dex', 'roll-o-dex', 5))
cr = (('pickpocket', 'pickpocket', 5), ('throw-paper', 'throw-paper', 3.5), ('glower', 'glower', 5))
tbc = (('cigar-smoke', 'cigar-smoke', 8),
 ('glower', 'glower', 5),
 ('song-and-dance', 'song-and-dance', 8),
 ('golf-club-swing', 'golf-club-swing', 5))
cc = (('speak', 'speak', 5),
 ('glower', 'glower', 5),
 ('phone', 'phone', 3.5),
 ('finger-wag', 'finger-wag', 5))
tm = (('speak', 'speak', 5),
 ('throw-paper', 'throw-paper', 5),
 ('pickpocket', 'pickpocket', 5),
 ('roll-o-dex', 'roll-o-dex', 5),
 ('finger-wag', 'finger-wag', 5))
nd = (('pickpocket', 'pickpocket', 5),
 ('roll-o-dex', 'roll-o-dex', 5),
 ('magic3', 'magic3', 5),
 ('smile', 'smile', 5))
gh = (('speak', 'speak', 5), ('pen-squirt', 'fountain-pen', 5), ('rubber-stamp', 'rubber-stamp', 5))
ms = (('effort', 'effort', 5),
 ('throw-paper', 'throw-paper', 5),
 ('stomp', 'stomp', 5),
 ('quick-jump', 'jump', 6))
tf = (('phone', 'phone', 5),
 ('smile', 'smile', 5),
 ('throw-object', 'throw-object', 5),
 ('glower', 'glower', 5))
m = (('speak', 'speak', 5),
 ('magic2', 'magic2', 5),
 ('magic1', 'magic1', 5),
 ('golf-club-swing', 'golf-club-swing', 5))
mh = (('magic1', 'magic1', 5),
 ('smile', 'smile', 5),
 ('golf-club-swing', 'golf-club-swing', 5),
 ('song-and-dance', 'song-and-dance', 5))
sc = (('throw-paper', 'throw-paper', 3.5), ('watercooler', 'watercooler', 5), ('pickpocket', 'pickpocket', 5))
pp = (('throw-paper', 'throw-paper', 5), ('glower', 'glower', 5), ('finger-wag', 'fingerwag', 5))
tw = (('throw-paper', 'throw-paper', 3.5),
 ('glower', 'glower', 5),
 ('magic2', 'magic2', 5),
 ('finger-wag', 'finger-wag', 5))
bc = (('phone', 'phone', 5), ('hold-pencil', 'hold-pencil', 5))
nc = (('phone', 'phone', 5), ('throw-object', 'throw-object', 5))
mb = (('magic1', 'magic1', 5), ('throw-paper', 'throw-paper', 3.5))
ls = (('throw-paper', 'throw-paper', 5), ('throw-object', 'throw-object', 5), ('hold-pencil', 'hold-pencil', 5))
rb = (('glower', 'glower', 5), ('magic1', 'magic1', 5), ('golf-club-swing', 'golf-club-swing', 5))
bf = (('pickpocket', 'pickpocket', 5),
 ('rubber-stamp', 'rubber-stamp', 5),
 ('shredder', 'shredder', 3.5),
 ('watercooler', 'watercooler', 5))
b = (('effort', 'effort', 5),
 ('throw-paper', 'throw-paper', 5),
 ('throw-object', 'throw-object', 5),
 ('magic1', 'magic1', 5))
dt = (('rubber-stamp', 'rubber-stamp', 5),
 ('throw-paper', 'throw-paper', 5),
 ('speak', 'speak', 5),
 ('finger-wag', 'fingerwag', 5),
 ('throw-paper', 'throw-paper', 5))
ac = (('throw-object', 'throw-object', 5),
 ('roll-o-dex', 'roll-o-dex', 5),
 ('stomp', 'stomp', 5),
 ('phone', 'phone', 5),
 ('throw-paper', 'throw-paper', 5))
bs = (('magic1', 'magic1', 5), ('throw-paper', 'throw-paper', 5), ('finger-wag', 'fingerwag', 5))
sd = (('magic2', 'magic2', 5),
 ('quick-jump', 'jump', 6),
 ('stomp', 'stomp', 5),
 ('magic3', 'magic3', 5),
 ('hold-pencil', 'hold-pencil', 5),
 ('throw-paper', 'throw-paper', 5))
le = (('speak', 'speak', 5),
 ('throw-object', 'throw-object', 5),
 ('glower', 'glower', 5),
 ('throw-paper', 'throw-paper', 5))
bw = (('finger-wag', 'fingerwag', 5),
 ('cigar-smoke', 'cigar-smoke', 8),
 ('gavel', 'gavel', 8),
 ('magic1', 'magic1', 5),
 ('throw-object', 'throw-object', 5),
 ('throw-paper', 'throw-paper', 5))
if not base.config.GetBool('want-new-cogs', 0):
    ModelDict = {'a': ('/models/char/suitA-', 4),
     'b': ('/models/char/suitB-', 4),
     'c': ('/models/char/suitC-', 3.5)}
    TutorialModelDict = {'a': ('/models/char/suitA-', 4),
     'b': ('/models/char/suitB-', 4),
     'c': ('/models/char/suitC-', 3.5)}
else:
    ModelDict = {'a': ('/models/char/tt_a_ene_cga_', 4),
     'b': ('/models/char/tt_a_ene_cgb_', 4),
     'c': ('/models/char/tt_a_ene_cgc_', 3.5)}
    TutorialModelDict = {'a': ('/models/char/tt_a_ene_cga_', 4),
     'b': ('/models/char/tt_a_ene_cgb_', 4),
     'c': ('/models/char/tt_a_ene_cgc_', 3.5)}
HeadModelDict = {'a': ('/models/char/suitA-', 4),
 'b': ('/models/char/suitB-', 4),
 'c': ('/models/char/suitC-', 3.5)}

SuitParts = ['phase_3.5/models/char/suitA-mod',
            'phase_3.5/models/char/suitB-mod',
            'phase_3.5/models/char/suitC-mod',
            'phase_4/models/char/suitA-heads',
            'phase_4/models/char/suitB-heads',
            'phase_3.5/models/char/suitC-heads']

Preloaded = {}

def loadModels():
    global Preloaded
    if not Preloaded:
        print 'Preloading suits...'
        for filepath in SuitParts:
            Preloaded[filepath] = loader.loadModel(filepath)
            Preloaded[filepath].flattenMedium()

def loadTutorialSuit():
    loader.loadModel('phase_3.5/models/char/suitC-mod')
    loadDialog(1)

def loadSuits(level):
    loadDialog(level)

def unloadSuits(level):
    #loadSuitModelsAndAnims(level, flag=0)
    unloadDialog(level)

def loadSuitModelsAndAnims(level, flag = 0):
    for key in ModelDict.keys():
        model, phase = ModelDict[key]
        if flag:
            filepath = 'phase_3.5' + model + 'mod'
            Preloaded[filepath] = loader.loadModel(filepath)
            filepath = 'phase_' + str(phase) + model + 'heads'
            Preloaded[filepath] = loader.loadModel(filepath)

def cogExists(filePrefix):
    searchPath = DSearchPath()
    if AppRunnerGlobal.appRunner:
        searchPath.appendDirectory(Filename.expandFrom('$TT_3_5_ROOT/phase_3.5'))
    else:
        basePath = os.path.expandvars('$TTMODELS') or './ttmodels'
        searchPath.appendDirectory(Filename.fromOsSpecific(basePath + '/built/phase_3.5'))
    filePrefix = filePrefix.strip('/')
    pfile = Filename(filePrefix)
    found = vfs.resolveFilename(pfile, searchPath)
    if not found:
        return False
    return True


def loadSuitAnims(suit, flag = 1):
    if suit in SuitDNA.suitHeadTypes:
        try:
            animList = eval(suit)
        except NameError:
            animList = ()

    else:
        print 'Invalid suit name: ', suit
        return -1
    for anim in animList:
        phase = 'phase_' + str(anim[2])
        filePrefix = ModelDict[bodyType][0]
        animName = filePrefix + anim[1]
        if flag:
            loader.loadModel(animName)
        else:
            loader.unloadModel(animName)


def loadDialog(level):
    global SuitDialogArray
    if len(SuitDialogArray) > 0:
        return
    else:
        loadPath = 'phase_3.5/audio/dial/'
        SuitDialogFiles = ['COG_VO_grunt',
         'COG_VO_murmur',
         'COG_VO_statement',
         'COG_VO_question']
        for file in SuitDialogFiles:
            SuitDialogArray.append(base.loadSfx(loadPath + file + '.ogg'))

        SuitDialogArray.append(SuitDialogArray[2])
        SuitDialogArray.append(SuitDialogArray[2])


def loadSkelDialog():
    global SkelSuitDialogArray
    if len(SkelSuitDialogArray) > 0:
        return
    else:
        grunt = loader.loadSfx('phase_5/audio/sfx/Skel_COG_VO_grunt.ogg')
        murmur = loader.loadSfx('phase_5/audio/sfx/Skel_COG_VO_murmur.ogg')
        statement = loader.loadSfx('phase_5/audio/sfx/Skel_COG_VO_statement.ogg')
        question = loader.loadSfx('phase_5/audio/sfx/Skel_COG_VO_question.ogg')
        SkelSuitDialogArray = [grunt,
         murmur,
         statement,
         question,
         statement,
         statement]


def unloadDialog(level):
    global SuitDialogArray
    SuitDialogArray = []


def unloadSkelDialog():
    global SkelSuitDialogArray
    SkelSuitDialogArray = []


def attachSuitHead(node, suitName):
    suitIndex = SuitDNA.suitHeadTypes.index(suitName)
    suitDNA = SuitDNA.SuitDNA()
    suitDNA.newSuit(suitName)
    suit = Suit()
    suit.setDNA(suitDNA)
    headParts = suit.getHeadParts()
    head = node.attachNewNode('head')
    for part in headParts:
        copyPart = part.copyTo(head)
        copyPart.setDepthTest(1)
        copyPart.setDepthWrite(1)

    suit.delete()
    suit = None
    p1 = Point3()
    p2 = Point3()
    head.calcTightBounds(p1, p2)
    d = p2 - p1
    biggest = max(d[0], d[2])
    column = suitIndex % SuitDNA.suitsPerDept
    s = (0.2 + column / 100.0) / biggest
    pos = -0.14 + (SuitDNA.suitsPerDept - column - 1) / 135.0
    head.setPosHprScale(0, 0, pos, 180, 0, 0, s, s, s)
    return head


class Suit(Avatar.Avatar):
    __module__ = __name__
    healthColors = (Vec4(0, 1, 0, 1),
     Vec4(1, 1, 0, 1),
     Vec4(1, 0.5, 0, 1),
     Vec4(1, 0, 0, 1),
     Vec4(0.3, 0.3, 0.3, 1))
    healthGlowColors = (Vec4(0.25, 1, 0.25, 0.5),
     Vec4(1, 1, 0.25, 0.5),
     Vec4(1, 0.5, 0.25, 0.5),
     Vec4(1, 0.25, 0.25, 0.5),
     Vec4(0.3, 0.3, 0.3, 0))
    medallionColors = {'c': Vec4(0.863, 0.776, 0.769, 1.0),
     's': Vec4(0.843, 0.745, 0.745, 1.0),
     'l': Vec4(0.749, 0.776, 0.824, 1.0),
     'm': Vec4(0.749, 0.769, 0.749, 1.0)}

    def __init__(self):
        try:
            self.Suit_initialized
            return
        except:
            self.Suit_initialized = 1

        Avatar.Avatar.__init__(self)
        self.setFont(ToontownGlobals.getSuitFont())
        self.setPlayerType(NametagGlobals.CCSuit)
        self.setPickable(1)
        self.leftHand = None
        self.rightHand = None
        self.shadowJoint = None
        self.nametagJoint = None
        self.headParts = []
        self.healthBar = None
        self.healthCondition = 0
        self.isDisguised = 0
        self.isWaiter = 0
        self.isRental = 0

    def delete(self):
        try:
            self.Suit_deleted
        except:
            self.Suit_deleted = 1
            if self.leftHand:
                self.leftHand.removeNode()
                self.leftHand = None
            if self.rightHand:
                self.rightHand.removeNode()
                self.rightHand = None
            if self.shadowJoint:
                self.shadowJoint.removeNode()
                self.shadowJoint = None
            if self.nametagJoint:
                self.nametagJoint.removeNode()
                self.nametagJoint = None
            for part in self.headParts:
                part.removeNode()

            self.headParts = []
            self.removeHealthBar()
            Avatar.Avatar.delete(self)

    def setHeight(self, height):
        Avatar.Avatar.setHeight(self, height)
        self.nametag3d.setPos(0, 0, height + 1.0)

    def getRadius(self):
        return 2

    def setDNAString(self, dnaString):
        self.dna = SuitDNA.SuitDNA()
        self.dna.makeFromNetString(dnaString)
        self.setDNA(self.dna)

    def setDNA(self, dna):
        if self.style:
            return

        self.style = dna
        self.generateSuit()
        self.initializeDropShadow()
        self.initializeNametag3d()

    def generateSuit(self):
        dna = self.style
        self.headParts = []
        self.headColor = None
        self.headTexture = None
        self.loseActor = None
        self.isSkeleton = 0

        if dna.name in SuitGlobals.suitProperties:
            self.scale = SuitGlobals.suitProperties[dna.name][SuitGlobals.SCALE_INDEX]
            self.handColor = SuitGlobals.suitProperties[dna.name][SuitGlobals.HAND_COLOR_INDEX]

            if dna.name == 'cc':
                self.headColor = SuitGlobals.ColdCallerHead

            self.generateBody()

            if SuitGlobals.suitProperties[dna.name][SuitGlobals.HEAD_TEXTURE_INDEX]:
                self.headTexture = SuitGlobals.suitProperties[dna.name][SuitGlobals.HEAD_TEXTURE_INDEX]

            for head in SuitGlobals.suitProperties[dna.name][SuitGlobals.HEADS_INDEX]:
                self.generateHead(head)

            self.setHeight(SuitGlobals.suitProperties[dna.name][SuitGlobals.HEIGHT_INDEX])

        self.setName(SuitBattleGlobals.SuitAttributes[dna.name]['name'])
        self.getGeomNode().setScale(self.scale)
        self.generateHealthBar()
        self.generateCorporateMedallion()

    def generateBody(self):
        global Preloaded
        animDict = self.generateAnimDict()
        filePrefix, bodyPhase = ModelDict[self.style.body]
        filepath = 'phase_3.5' + filePrefix + 'mod'
        self.loadModel(Preloaded[filepath], copy = True)
        self.loadAnims(animDict)
        self.setSuitClothes()

    def generateAnimDict(self):
        animDict = {}
        filePrefix, bodyPhase = ModelDict[self.style.body]
        for anim in AllSuits:
            animDict[anim[0]] = 'phase_' + str(bodyPhase) + filePrefix + anim[1]

        for anim in AllSuitsMinigame:
            animDict[anim[0]] = 'phase_4' + filePrefix + anim[1]

        for anim in AllSuitsTutorialBattle:
            filePrefix, bodyPhase = TutorialModelDict[self.style.body]
            animDict[anim[0]] = 'phase_' + str(bodyPhase) + filePrefix + anim[1]

        for anim in AllSuitsBattle:
            animDict[anim[0]] = 'phase_5' + filePrefix + anim[1]

        if self.style.body == 'a':
            animDict['neutral'] = 'phase_4/models/char/suitA-neutral'
            for anim in SuitsCEOBattle:
                animDict[anim[0]] = 'phase_12/models/char/suitA-' + anim[1]
        elif self.style.body == 'b':
            animDict['neutral'] = 'phase_4/models/char/suitB-neutral'
            for anim in SuitsCEOBattle:
                animDict[anim[0]] = 'phase_12/models/char/suitB-' + anim[1]
        elif self.style.body == 'c':
            animDict['neutral'] = 'phase_3.5/models/char/suitC-neutral'
            for anim in SuitsCEOBattle:
                animDict[anim[0]] = 'phase_12/models/char/suitC-' + anim[1]

        try:
            animList = eval(self.style.name)
        except NameError:
            animList = ()

        for anim in animList:
            phase = 'phase_' + str(anim[2])
            animDict[anim[0]] = phase + filePrefix + anim[1]

        return animDict

    def initializeBodyCollisions(self, collIdStr):
        Avatar.Avatar.initializeBodyCollisions(self, collIdStr)
        if not self.ghostMode:
            self.collNode.setCollideMask(self.collNode.getIntoCollideMask() | ToontownGlobals.PieBitmask)

    def setSuitClothes(self, modelRoot = None):
        if not modelRoot:
            modelRoot = self
        dept = self.style.dept
        phase = 3.5

        torsoTex = loader.loadTexture('phase_%s/maps/%s_blazer.jpg' % (phase, dept))
        torsoTex.setMinfilter(Texture.FTLinearMipmapLinear)
        torsoTex.setMagfilter(Texture.FTLinear)
        legTex = loader.loadTexture('phase_%s/maps/%s_leg.jpg' % (phase, dept))
        legTex.setMinfilter(Texture.FTLinearMipmapLinear)
        legTex.setMagfilter(Texture.FTLinear)
        armTex = loader.loadTexture('phase_%s/maps/%s_sleeve.jpg' % (phase, dept))
        armTex.setMinfilter(Texture.FTLinearMipmapLinear)
        armTex.setMagfilter(Texture.FTLinear)
        modelRoot.find('**/torso').setTexture(torsoTex, 1)
        modelRoot.find('**/arms').setTexture(armTex, 1)
        modelRoot.find('**/legs').setTexture(legTex, 1)
        modelRoot.find('**/hands').setColor(self.handColor)
        self.leftHand = self.find('**/joint_Lhold')
        self.rightHand = self.find('**/joint_Rhold')
        self.shadowJoint = self.find('**/joint_shadow')
        self.nametagJoint = self.find('**/joint_nameTag')

    def makeWaiter(self, modelRoot = None):
        if not modelRoot:
            modelRoot = self
        self.isWaiter = 1
        torsoTex = loader.loadTexture('phase_3.5/maps/waiter_m_blazer.jpg')
        torsoTex.setMinfilter(Texture.FTLinearMipmapLinear)
        torsoTex.setMagfilter(Texture.FTLinear)
        legTex = loader.loadTexture('phase_3.5/maps/waiter_m_leg.jpg')
        legTex.setMinfilter(Texture.FTLinearMipmapLinear)
        legTex.setMagfilter(Texture.FTLinear)
        armTex = loader.loadTexture('phase_3.5/maps/waiter_m_sleeve.jpg')
        armTex.setMinfilter(Texture.FTLinearMipmapLinear)
        armTex.setMagfilter(Texture.FTLinear)
        modelRoot.find('**/torso').setTexture(torsoTex, 1)
        modelRoot.find('**/arms').setTexture(armTex, 1)
        modelRoot.find('**/legs').setTexture(legTex, 1)

    def makeRentalSuit(self, suitType, modelRoot = None):
        if not modelRoot:
            modelRoot = self.getGeomNode()
        if suitType == 's':
            torsoTex = loader.loadTexture('phase_3.5/maps/tt_t_ene_sellbotRental_blazer.jpg')
            legTex = loader.loadTexture('phase_3.5/maps/tt_t_ene_sellbotRental_leg.jpg')
            armTex = loader.loadTexture('phase_3.5/maps/tt_t_ene_sellbotRental_sleeve.jpg')
            handTex = loader.loadTexture('phase_3.5/maps/tt_t_ene_sellbotRental_hand.jpg')
        else:
            self.notify.warning('No rental suit for cog type %s' % suitType)
            return
        self.isRental = 1
        modelRoot.find('**/torso').setTexture(torsoTex, 1)
        modelRoot.find('**/arms').setTexture(armTex, 1)
        modelRoot.find('**/legs').setTexture(legTex, 1)
        modelRoot.find('**/hands').setTexture(handTex, 1)

    def generateHead(self, headType):
        filePrefix, phase = ModelDict[self.style.body]
        filepath = 'phase_' + str(phase) + filePrefix + 'heads'
        headModel = NodePath('cog_head')
        Preloaded[filepath].copyTo(headModel)
        headReferences = headModel.findAllMatches('**/' + headType)
        for i in xrange(0, headReferences.getNumPaths()):
            headPart = self.instance(headReferences.getPath(i), 'modelRoot', 'joint_head')
            if self.headTexture:
                headTex = loader.loadTexture('phase_' + str(phase) + '/maps/' + self.headTexture)
                headTex.setMinfilter(Texture.FTLinearMipmapLinear)
                headTex.setMagfilter(Texture.FTLinear)
                headPart.setTexture(headTex, 1)
            if self.headColor:
                headPart.setColor(self.headColor)
            headPart.flattenStrong()
            self.headParts.append(headPart)
        headModel.removeNode()

    def generateCorporateTie(self, modelPath = None):
        if not modelPath:
            modelPath = self
        dept = self.style.dept
        tie = modelPath.find('**/tie')
        if tie.isEmpty():
            self.notify.warning('skelecog has no tie model!!!')
            return
        if dept == 'c':
            tieTex = loader.loadTexture('phase_5/maps/cog_robot_tie_boss.jpg')
        elif dept == 's':
            tieTex = loader.loadTexture('phase_5/maps/cog_robot_tie_sales.jpg')
        elif dept == 'l':
            tieTex = loader.loadTexture('phase_5/maps/cog_robot_tie_legal.jpg')
        elif dept == 'm':
            tieTex = loader.loadTexture('phase_5/maps/cog_robot_tie_money.jpg')
        tieTex.setMinfilter(Texture.FTLinearMipmapLinear)
        tieTex.setMagfilter(Texture.FTLinear)
        tie.setTexture(tieTex, 1)

    def generateCorporateMedallion(self):
        icons = loader.loadModel('phase_3/models/gui/cog_icons')
        dept = self.style.dept
        chestNull = self.find('**/joint_attachMeter')
        if dept == 'c':
            self.corpMedallion = icons.find('**/CorpIcon').copyTo(chestNull)
        elif dept == 's':
            self.corpMedallion = icons.find('**/SalesIcon').copyTo(chestNull)
        elif dept == 'l':
            self.corpMedallion = icons.find('**/LegalIcon').copyTo(chestNull)
        elif dept == 'm':
            self.corpMedallion = icons.find('**/MoneyIcon').copyTo(chestNull)
        self.corpMedallion.setPosHprScale(0.02, 0.05, 0.04, 180.0, 0.0, 0.0, 0.51, 0.51, 0.51)
        self.corpMedallion.setColor(self.medallionColors[dept])
        icons.removeNode()

    def generateHealthBar(self):
        self.removeHealthBar()
        model = loader.loadModel('phase_3.5/models/gui/matching_game_gui')
        button = model.find('**/minnieCircle')
        model.removeNode()

        button.setScale(3.0)
        button.setH(180.0)
        button.setColor(self.healthColors[0])
        chestNull = self.find('**/joint_attachMeter')
        button.reparentTo(chestNull)
        self.healthBar = button
        glow = BattleProps.globalPropPool.getProp('glow')
        glow.reparentTo(self.healthBar)
        glow.setScale(0.28)
        glow.setPos(-0.005, 0.01, 0.015)
        glow.setColor(self.healthGlowColors[0])
        button.flattenLight()
        self.healthBarGlow = glow
        self.healthBar.hide()
        self.healthCondition = 0

    def resetHealthBarForSkele(self):
        self.healthBar.setPos(0.0, 0.1, 0.0)

    def updateHealthBar(self, hp, forceUpdate = 0):
        if hp > self.currHP:
            hp = self.currHP
        self.currHP -= hp
        health = float(self.currHP) / float(self.maxHP)
        if health > 0.95:
            condition = 0
        elif health > 0.7:
            condition = 1
        elif health > 0.3:
            condition = 2
        elif health > 0.05:
            condition = 3
        elif health > 0.0:
            condition = 4
        else:
            condition = 5
        if self.healthCondition != condition or forceUpdate:
            if condition == 4:
                blinkTask = Task.loop(Task(self.__blinkRed), Task.pause(0.75), Task(self.__blinkGray), Task.pause(0.1))
                taskMgr.add(blinkTask, self.uniqueName('blink-task'))
            elif condition == 5:
                if self.healthCondition == 4:
                    taskMgr.remove(self.uniqueName('blink-task'))
                blinkTask = Task.loop(Task(self.__blinkRed), Task.pause(0.25), Task(self.__blinkGray), Task.pause(0.1))
                taskMgr.add(blinkTask, self.uniqueName('blink-task'))
            else:
                self.healthBar.setColor(self.healthColors[condition], 1)
                self.healthBarGlow.setColor(self.healthGlowColors[condition], 1)
            self.healthCondition = condition

    def __blinkRed(self, task):
        self.healthBar.setColor(self.healthColors[3], 1)
        self.healthBarGlow.setColor(self.healthGlowColors[3], 1)
        if self.healthCondition == 5:
            self.healthBar.setScale(1.17)
        return Task.done

    def __blinkGray(self, task):
        if not self.healthBar:
            return
        self.healthBar.setColor(self.healthColors[4], 1)
        self.healthBarGlow.setColor(self.healthGlowColors[4], 1)
        if self.healthCondition == 5:
            self.healthBar.setScale(1.0)
        return Task.done

    def removeHealthBar(self):
        if self.healthBar:
            self.healthBar.removeNode()
            self.healthBar = None
        if self.healthCondition == 4 or self.healthCondition == 5:
            taskMgr.remove(self.uniqueName('blink-task'))
        self.healthCondition = 0
        return

    def getLoseActor(self):
        if self.loseActor == None:
            if not self.isSkeleton:
                filePrefix, phase = TutorialModelDict[self.style.body]
                loseModel = 'phase_' + str(phase) + filePrefix + 'lose-mod'
                loseAnim = 'phase_' + str(phase) + filePrefix + 'lose'
                self.loseActor = Actor.Actor(loseModel, {'lose': loseAnim})
                loseNeck = self.loseActor.find('**/joint_head')
                for part in self.headParts:
                    part.instanceTo(loseNeck)

                if self.isWaiter:
                    self.makeWaiter(self.loseActor)
                else:
                    self.setSuitClothes(self.loseActor)
            else:
                loseModel = 'phase_5/models/char/cog' + string.upper(self.style.body) + '_robot-lose-mod'
                filePrefix, phase = TutorialModelDict[self.style.body]
                loseAnim = 'phase_' + str(phase) + filePrefix + 'lose'
                self.loseActor = Actor.Actor(loseModel, {'lose': loseAnim})
                self.generateCorporateTie(self.loseActor)
        self.loseActor.setScale(self.scale)
        self.loseActor.setPos(self.getPos())
        self.loseActor.setHpr(self.getHpr())
        shadowJoint = self.loseActor.find('**/joint_shadow')
        dropShadow = loader.loadModel('phase_3/models/props/drop_shadow')
        dropShadow.setScale(0.45)
        dropShadow.setColor(0.0, 0.0, 0.0, 0.5)
        dropShadow.reparentTo(shadowJoint)
        return self.loseActor

    def cleanupLoseActor(self):
        self.notify.debug('cleanupLoseActor()')
        if self.loseActor != None:
            self.notify.debug('cleanupLoseActor() - got one')
            self.loseActor.cleanup()
        self.loseActor = None
        return

    def makeSkeleton(self):
        model = 'phase_5/models/char/cog' + string.upper(self.style.body) + '_robot-zero'
        anims = self.generateAnimDict()
        anim = self.getCurrentAnim()
        dropShadow = self.dropShadow
        if not dropShadow.isEmpty():
            dropShadow.reparentTo(hidden)
        self.removePart('modelRoot')
        self.loadModel(model)
        self.loadAnims(anims)
        self.getGeomNode().setScale(self.scale * 1.0173)
        self.generateHealthBar()
        self.generateCorporateMedallion()
        self.generateCorporateTie()
        self.setHeight(self.height)
        parts = self.findAllMatches('**/pPlane*')
        for partNum in xrange(0, parts.getNumPaths()):
            bb = parts.getPath(partNum)
            bb.setTwoSided(1)

        self.setName(TTLocalizer.Skeleton)
        nameInfo = TTLocalizer.SuitBaseNameWithLevel % {'name': self.name,
         'dept': self.getStyleDept(),
         'level': self.getActualLevel()}
        self.setDisplayName(nameInfo)
        self.leftHand = self.find('**/joint_Lhold')
        self.rightHand = self.find('**/joint_Rhold')
        self.shadowJoint = self.find('**/joint_shadow')
        self.nametagNull = self.find('**/joint_nameTag')
        if not dropShadow.isEmpty():
            dropShadow.setScale(0.75)
            if not self.shadowJoint.isEmpty():
                dropShadow.reparentTo(self.shadowJoint)
        self.loop(anim)
        self.isSkeleton = 1

    def getHeadParts(self):
        return self.headParts

    def getRightHand(self):
        return self.rightHand

    def getLeftHand(self):
        return self.leftHand

    def getShadowJoint(self):
        return self.shadowJoint

    def getNametagJoints(self):
        return []

    def getDialogueArray(self):
        if self.isSkeleton:
            loadSkelDialog()
            return SkelSuitDialogArray
        else:
            return SuitDialogArray
