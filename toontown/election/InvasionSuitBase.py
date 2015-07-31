#Embedded file name: toontown.election.InvasionSuitBase
from pandac.PandaModules import *
from toontown.toonbase import ToontownGlobals

class InvasionSuitBase:

    def __init__(self):
        self.walkSpeed = ToontownGlobals.SuitWalkSpeed
        self.freezeLerp(0, 0)

    def setLerpPoints(self, x1, y1, x2, y2):
        self._originPoint = Point2(x1, y1)
        endPoint = Point2(x2, y2)
        self._lerpVector = endPoint - self._originPoint
        self._idealH = -self._lerpVector.signedAngleDeg(Vec2(0, 1))
        vectorLength = self._lerpVector.length()
        self._lerpDelay = vectorLength / self.walkSpeed
        self._lerpDelay = max(self._lerpDelay, 0.01)

    def freezeLerp(self, x, y):
        self.setLerpPoints(x, y, x, y)

    def getPosAt(self, t):
        vecScale = min(max(t / self._lerpDelay, 0.0), 1.0)
        return self._originPoint + self._lerpVector * vecScale

    def freezeLerpAt(self, t):
        x, y = self.getPosAt(t)
        self.freezeLerp(x, y)
