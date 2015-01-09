from otp.level.EntityTypes import *

class CogdoLevelMgr(LevelMgr):
    type = 'levelMgr'


class CogdoBoardroomGameSettings(Entity):
    type = 'cogdoBoardroomGameSettings'
    aTTWibs = (('TimerScale', 1.0, 'float'),)


class CogdoCraneGameSettings(Entity):
    type = 'cogdoCraneGameSettings'
    aTTWibs = (('GameDuration', 180.0, 'float'),
     ('EmptyFrictionCoef', 0.1, 'float'),
     ('Gravity', -32, 'int'),
     ('RopeLinkMass', 1.0, 'float'),
     ('MagnetMass', 1.0, 'float'),
     ('MoneyBagGrabHeight', -8.2, 'float'))


class CogdoCraneCogSettings(Entity):
    type = 'cogdoCraneCogSettings'
    aTTWibs = (('CogSpawnPeriod', 10.0, 'float'),
     ('CogWalkSpeed', 2.0, 'float'),
     ('CogMachineInteractDuration', 2.0, 'float'),
     ('CogFlyAwayHeight', 50.0, 'float'),
     ('CogFlyAwayDuration', 4.0, 'float'))
