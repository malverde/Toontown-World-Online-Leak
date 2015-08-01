#Embedded file name: toontown.election.DistributedToonfestCog
from pandac.PandaModules import *
from otp.nametag.NametagConstants import *
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
from direct.distributed.DistributedObject import DistributedObject
from direct.fsm.FSM import FSM
from direct.actor import Actor
from direct.task import Task
from toontown.toon import NPCToons
from toontown.suit import DistributedSuitBase, SuitDNA
from toontown.toonbase import ToontownGlobals
from toontown.battle import BattleProps
from otp.margins.WhisperPopup import *
import ElectionGlobals
from direct.directnotify import DirectNotifyGlobal
from random import choice
from toontown.battle.BattleProps import globalPropPool
from toontown.battle.BattleSounds import globalBattleSoundCache
from toontown.parties import *
from otp.speedchat import SpeedChatGlobals

class DistributedToonfestCog(DistributedObject, FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedToonfestCog')

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        FSM.__init__(self, 'ToonfestCogFSM')
        self.load()
        self.request('Down')
        self.id = 0

    def setIdThroughAI(self, id):
        self.id = id

    def load(self):
        self.root = NodePath('ToonfestCog')
        self.parentNode = NodePath('Parent')
        self.parentNode.reparentTo(render)
        self.root.reparentTo(render)
        path = 'phase_13/models/parties/cogPinata_'
        self.actor = Actor.Actor(path + 'actor', {'idle': path + 'idle_anim',
         'down': path + 'down_anim',
         'up': path + 'up_anim',
         'bodyHitBack': path + 'bodyHitBack_anim',
         'bodyHitFront': path + 'bodyHitFront_anim',
         'headHitBack': path + 'headHitBack_anim',
         'headHitFront': path + 'headHitFront_anim'})
        self.actor.reparentTo(self.root)
        self.temp_transform = Mat4()
        self.head_locator = self.actor.attachNewNode('temphead')
        self.bodyColl = CollisionTube(0, 0, 1, 0, 0, 5.75, 0.75)
        self.bodyColl.setTangible(1)
        self.bodyCollNode = CollisionNode('ToonfestCog-Body-Collision')
        self.bodyCollNode.setCollideMask(ToontownGlobals.PieBitmask)
        self.bodyCollNode.addSolid(self.bodyColl)
        self.bodyCollNodePath = self.root.attachNewNode(self.bodyCollNode)
        self.headColl = CollisionTube(0, 0, 3, 0, 0, 3.0, 1.5)
        self.headColl.setTangible(1)
        self.headCollNode = CollisionNode('ToonfestCog-Head-Collision')
        self.headCollNode.setCollideMask(ToontownGlobals.PieBitmask)
        self.headCollNode.addSolid(self.headColl)
        self.headCollNodePath = self.root.attachNewNode(self.headCollNode)
        self.arm1Coll = CollisionSphere(1.65, 0, 3.95, 1.0)
        self.arm1Coll.setTangible(1)
        self.arm1CollNode = CollisionNode('ToonfestCog-Arm1-Collision')
        self.arm1CollNode.setCollideMask(ToontownGlobals.PieBitmask)
        self.arm1CollNode.addSolid(self.arm1Coll)
        self.arm1CollNodePath = self.root.attachNewNode(self.arm1CollNode)
        self.arm2Coll = CollisionSphere(-1.65, 0, 3.45, 1.0)
        self.arm2Coll.setTangible(1)
        self.arm2CollNode = CollisionNode('ToonfestCog-Arm2-Collision')
        self.arm2CollNode.setCollideMask(ToontownGlobals.PieBitmask)
        self.arm2CollNode.addSolid(self.arm2Coll)
        self.arm2CollNodePath = self.root.attachNewNode(self.arm2CollNode)
        splatName = 'splat-creampie'
        self.splat = globalPropPool.getProp(splatName)
        self.splat.setBillboardPointEye()
        self.splatType = globalPropPool.getPropType(splatName)
        self.pieHitSound = globalBattleSoundCache.getSound('AA_wholepie_only.ogg')
        self.upSound = globalBattleSoundCache.getSound('AV_jump_to_side.ogg')
        self.hole = loader.loadModel('phase_13/models/parties/cogPinataHole')
        self.hole.setTransparency(True)
        self.hole.setP(-90.0)
        self.hole.setScale(3)
        self.hole.setBin('ground', 3)
        self.hole.reparentTo(self.parentNode)
        taskMgr.doMethodLater(60, self.toggleCog, 'toggle-cog', extraArgs=[])

    def toggleCog(self):
        if self.state == 'Down':
            self.request('Up')
        else:
            self.request('Down')
        taskMgr.doMethodLater(60, self.toggleCog, 'toggle-cog', extraArgs=[])

    def unload(self):
        taskMgr.remove('toggle-cog')
        self.request('Off')
        self.clearHitInterval()
        if self.hole is not None:
            self.hole.removeNode()
            self.hole = None
        if self.actor is not None:
            self.actor.cleanup()
            self.actor.removeNode()
            self.actor = None
        if self.root is not None:
            self.root.removeNode()
            self.root = None
        if self.kaboomTrack is not None and self.kaboomTrack.isPlaying():
            self.kaboomTrack.finish()
        self.kaboomTrack = None
        if self.resetRollIval is not None and self.resetRollIval.isPlaying():
            self.resetRollIval.finish()
        self.resetRollIval = None
        if self.hitInterval is not None and self.hitInterval.isPlaying():
            self.hitInterval.finish()
        self.hitInterval = None
        del self.upSound
        del self.pieHitSound

    def delete(self):
        self.demand('Off')
        self.unload()
        DistributedObject.delete(self)

    def enterDown(self):
        if self.oldState == 'Off':
            downAnimControl = self.actor.getAnimControl('down')
            self.actor.pose('down', downAnimControl.getNumFrames() - 1)
            return
        self.clearHitInterval()
        startScale = self.hole.getScale()
        endScale = Point3(5, 5, 5)
        self.hitInterval = Sequence(LerpScaleInterval(self.hole, duration=0.175, scale=endScale, startScale=startScale, blendType='easeIn'), Parallel(SoundInterval(self.upSound, volume=0.6, node=self.actor, cutOff=PartyGlobals.PARTY_COG_CUTOFF), ActorInterval(self.actor, 'down', loop=0)), LerpScaleInterval(self.hole, duration=0.175, scale=Point3(3, 3, 3), startScale=endScale, blendType='easeOut'))
        self.hitInterval.start()

    def enterUp(self):
        self.root.setR(0.0)
        self.root.setH(0.0)
        self.targetDistance = 0.0
        self.targetFacing = 0.0
        self.currentT = 0.0
        self.clearHitInterval()
        startScale = self.hole.getScale()
        endScale = Point3(5, 5, 5)
        self.hitInterval = Sequence(LerpScaleInterval(self.hole, duration=0.175, scale=endScale, startScale=startScale, blendType='easeIn'), Parallel(SoundInterval(self.upSound, volume=0.6, node=self.actor, cutOff=PartyGlobals.PARTY_COG_CUTOFF), ActorInterval(self.actor, 'up', loop=0)), Func(self.actor.loop, 'idle'), LerpScaleInterval(self.hole, duration=0.175, scale=Point3(3, 3, 3), startScale=endScale, blendType='easeOut'))
        self.hitInterval.start()

    def setPosThroughAI(self, x, y, z):
        self.root.setPos(x, y, z)
        self.parentNode.setPos(x, y, z)

    def respondToPieHit(self, timestamp, position, hot = False, direction = 1.0):
        if self.netTimeSentToStartByHit < timestamp:
            self.__showSplat(position, direction, hot)
            self.sendUpdate('updateTower', [])
            if self.netTimeSentToStartByHit < timestamp:
                self.netTimeSentToStartByHit = timestamp
        else:
            self.notify.debug('respondToPieHit self.netTimeSentToStartByHit = %s' % self.netTimeSentToStartByHit)

    def clearHitInterval(self):
        if self.hitInterval is not None and self.hitInterval.isPlaying():
            self.hitInterval.clearToInitial()

    def __showSplat(self, position, direction, hot = False):
        if self.kaboomTrack is not None and self.kaboomTrack.isPlaying():
            self.kaboomTrack.finish()
        self.clearHitInterval()
        splatName = 'splat-creampie'
        self.splat = globalPropPool.getProp(splatName)
        self.splat.setBillboardPointEye()
        self.splat.reparentTo(render)
        self.splat.setPos(self.root, position)
        self.splat.setAlphaScale(1.0)
        if not direction == 1.0:
            self.splat.setColorScale(PartyGlobals.CogActivitySplatColors[0])
            if self.currentFacing > 0.0:
                facing = 'HitFront'
            else:
                facing = 'HitBack'
        else:
            self.splat.setColorScale(PartyGlobals.CogActivitySplatColors[1])
            if self.currentFacing > 0.0:
                facing = 'HitBack'
            else:
                facing = 'HitFront'
        if hot:
            targetscale = 0.75
            part = 'head'
        else:
            targetscale = 0.5
            part = 'body'

        def setSplatAlpha(amount):
            self.splat.setAlphaScale(amount)

        self.hitInterval = Sequence(ActorInterval(self.actor, part + facing, loop=0), Func(self.actor.loop, 'idle'))
        self.hitInterval.start()
        self.kaboomTrack = Parallel(SoundInterval(self.pieHitSound, volume=1.0, node=self.actor, cutOff=PartyGlobals.PARTY_COG_CUTOFF), Sequence(Func(self.splat.showThrough), Parallel(Sequence(LerpScaleInterval(self.splat, duration=0.175, scale=targetscale, startScale=Point3(0.1, 0.1, 0.1), blendType='easeOut'), Wait(0.175)), Sequence(Wait(0.1), LerpFunc(setSplatAlpha, duration=1.0, fromData=1.0, toData=0.0, blendType='easeOut'))), Func(self.splat.cleanup), Func(self.splat.removeNode)))
        self.kaboomTrack.start()
