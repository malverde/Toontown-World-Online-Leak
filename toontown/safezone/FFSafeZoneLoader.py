########################## THE TOON LAND PROJECT ##########################
# Filename: FFSafeZoneLoader.py
# Created by: Cody/Fd Green Cat Fd (January 31st, 2013)
####
# Description:
#
# The Funny Farm safe zone loader. This is where any music, and/or models will be loaded.
####

from pandac.PandaModules import *
from otp.otpbase import OTPGlobals
from toontown.safezone import SafeZoneLoader
from direct.task.Task import Task
from toontown.estate import HouseGlobals

class FFSafeZoneLoader(SafeZoneLoader.SafeZoneLoader):

    def __loadPythonImplementation(self, task):
        if render.find('**/%d:safe_zone' % PlaygroundGlobals.FUNNY_FARM):
            execfile('%s\\toonland\\playground\\funnyfarm\\_FunnyFarm.py' % __filebase__)
            fountain = render.find('**/prop_funny_farm_fountain_DNARoot')
            triggerName = 'fountainSplash_trigger'
            triggerEvent_enter = 'enter%s' % triggerName
            cs = CollisionSphere(-33.0, 12.0, -27, 39.5)
            cs.setTangible(0)
            cn = CollisionNode(triggerName)
            cn.addSolid(cs)
            cn.setIntoCollideMask(OTPGlobals.WallBitmask)
            trigger = fountain.attachNewNode(cn)
            base.localAvatar.accept(triggerEvent_enter, self.handleSplashEffect)
            base.localAvatar.d_setParent('x\x8c6\xdd\xb6\x80')
            return Task.done
        taskMgr.doMethodLater(0.2, self._FFSafeZoneLoader__loadPythonImplementation, 'FF-LPI')

    def __init__(self, hood, parentFSM, doneEvent):
        SafeZoneLoader.SafeZoneLoader.__init__(self, hood, parentFSM, doneEvent)
        self.playgroundClass = FFPlayground.FFPlayground
        filepath = '%s/toonland/playground/funnyfarm/bgm' % __filebase__
        self.musicFile = '%s/FF_nbrhood.mp3' % filepath
        self.activityMusicFile = 'phase_3.5/audio/bgm/TC_SZ_activity.mid'
        filepath = '%s/toonland/playground/funnyfarm/dna' % __filebase__
        self.dnaFile = '%s/funny_farm_sz.dna' % filepath
        self.safeZoneStorageDNAFile = '%s/storage_FF_sz.dna' % filepath
        HouseGlobals.houseColors += [HouseGlobals.houseColors[2], (0.78, 0.52, 0.42), (1.0, 0.453, 0.4)]
        HouseGlobals.houseColors2 += [HouseGlobals.houseColors2[2], (0.58, 0.37, 0.27), (0.9, 0.353, 0.3)]
        self.houseModels = [loader.loadModel('phase_5.5/models/estate/houseB')]
        self.houseNode = []
        nodepaths = [(-82, 78, 10, -59), (-35, 79, 10, -52), (41, 92, 10, -118)]
        for houseId in range(3):
            nodepath = render.attachNewNode('esHouse_%d' % houseId)
            X, Y, Z, H = nodepaths[houseId]
            nodepath.setPosHpr(X, Y, Z, H, 0, 0)
            self.houseNode.append(nodepath)
        self.houseId2house = {}

    def handleSplashEffect(self, collisionEntry):
        X, Y = base.localAvatar.getX(), base.localAvatar.getY()
        base.localAvatar.playSplashEffect(X, Y, 10)
        base.localAvatar.d_playSplashEffect(X, Y, 10)

    def enter(self, requestStatus):
        SafeZoneLoader.SafeZoneLoader.enter(self, requestStatus)

    def exit(self):
        SafeZoneLoader.SafeZoneLoader.exit(self)

    def load(self):
        SafeZoneLoader.SafeZoneLoader.load(self)
        self.birdSound = map(base.loadSfx, ['phase_4/audio/sfx/SZ_TC_bird1.mp3',
         'phase_4/audio/sfx/SZ_TC_bird2.mp3', 'phase_4/audio/sfx/SZ_TC_bird3.mp3'])
        taskMgr.doMethodLater(0.2, self._FFSafeZoneLoader__loadPythonImplementation, 'FF-LPI')

    def unload(self):
        del self.birdSound
        SafeZoneLoader.SafeZoneLoader.unload(self)
        for objectId in TTSendBuffer.TTSendBuffer.temporary_objects:
            for message in TTSendBuffer.TTSendBuffer.queued_messages:
                if objectId in message:
                    index = TTSendBuffer.TTSendBuffer.queued_messages.index(message)
                    del TTSendBuffer.TTSendBuffer.queued_messages[index]
            object = TTSendBuffer.TTSendBuffer.networking_objects[objectId]
            object.disable()
            object.delete()
            del TTSendBuffer.TTSendBuffer.networking_objects[objectId]
        TTSendBuffer.TTSendBuffer.temporary_objects = []