from panda3d.core import *
from direct.interval.IntervalGlobal import *
from direct.fsm.FSM import *
import random, math

estateRadius = 130
estateCenter = (0, -40)

houseRadius = 15
houses = ((60, 10), (42, 75), (-37, 35),  (80, -80), (-70, -120), (-55, -40))

def inCircle(x, y, c=estateCenter, r=estateRadius):
    center_x, center_y = c
    square_dist = (center_x - x) ** 2 + (center_y - y) ** 2
    return square_dist <= r ** 2
    
def housePointCollision(x, y):
    for i, h in enumerate(houses):
        if inCircle(x, y, h, houseRadius):
            return 1
            
    return 0
    
def generatePos():
    def get():
        r = random.randint(0, estateRadius) - estateRadius / 2
        r2 = random.randint(0, estateRadius) - estateRadius / 2
        x = r + estateCenter[0]
        y = r2 + estateCenter[1]
        assert inCircle(x, y)
        return x, y
        
    p = get()
    while housePointCollision(*p):
        p = get()
        
    return p

def lineInCircle(pt1, pt2, circlePoint, circleRadius=houseRadius):
    x1, y1 = pt1
    x2, y2 = pt2
    
    dist = math.hypot(x2 - x1, y2 - y1)
    if dist == 0:
        return 0
  
    dx = (x2 - x1) / dist
    dy = (y2 - y1) / dist
    
    t = dx * (circlePoint[0] - x1) + dy * (circlePoint[1] - y1)
    
    ex = t * dx + x1
    ey = t * dy + y1
    
    d2 = math.hypot(ex - circlePoint[0], ey - circlePoint[1])
    return d2 <= circleRadius
                
def houseCollision(pt1, pt2):
    for i, h in enumerate(houses):
        if lineInCircle(pt1, pt2, h):
            return 1
            
    return 0
    
def generatePath(start, end):
    points = [start]
    if not houseCollision(start, end):
        points.append(end)
        return points

    while True:
        next = generatePos()
        while houseCollision(points[-1], next):
            next = generatePos()
            
        points.append(next)
        if not houseCollision(next, end):
            points.append(end)
            return points
    
class PetMoverAI(FSM):    
    def __init__(self, pet):
        self.pet = pet
        FSM.__init__(self, 'PetMoverAI-%d' % self.pet.doId)
        self.chaseTarget = None
        self.__seq = None
        self.fwdSpeed = 10.0
        self.rotSpeed = 360.0
        self.__moveFromStill()
        self.__chaseCallback = None
        
    def enterStill(self):
        taskMgr.doMethodLater(random.randint(15, 60), self.__moveFromStill, self.pet.uniqueName('next-state'))
                
    def exitStill(self):
        taskMgr.remove(self.pet.uniqueName('next-state'))
        
    def __moveFromStill(self, task=None):
        choices = ["Wander"]
        # if self.pet._getNearbyAvatarDict():
        #     choices.append("Chase")
            
        nextState = random.choice(choices)
        self.request(nextState)
        
    def enterWander(self):
        target = self.getPoint()
        self.walkToPoint(target)
        
    def getPoint(self):
        x, y = generatePos()
        return Point3(x, y, 0)
        
    def walkToPoint(self, target):
        here = self.pet.getPos()
        dist = Vec3((here - target)).length()
        dist = dist * 0.9
        self.__seq = Sequence(Func(self.pet.lookAt, target), self.pet.posInterval(dist / self.fwdSpeed, target, here),
                              Func(self.__stateComplete))
        self.__seq.start()
        
    def exitWander(self):
        if self.__seq:
            self.__seq.pause()
            
        self.__seq = None
        
    def __stateComplete(self):
        try:
            self.request("Still")
            
        except:
            pass
        
    def destroy(self):
        self.demand("Off")
        
    def setFwdSpeed(self, speed):
        self.fwdSpeed = speed
        
    def getFwdSpeed(self):
        return self.fwdSpeed
        
    def setRotSpeed(self, speed):
        self.rotSpeed = speed

    def getRotSpeed(self):
        return self.rotSpeed
        
    def lock(self):
        if self.state != "Still":
            self.demand("Still")
        
    def enterChase(self, target=None):
        if not target:
            target = hidden.attachNewNode('target')
            target.setPos(self.getPoint())
            
        self.walkToPoint(target.getPos())
        
        
    def exitChase(self):
        if self.__chaseCallback:
            self.__chaseCallback()
            self.__chaseCallback = None
            
        if self.__seq:
            self.__seq.pause()
            
        self.__seq = None
        
    def walkToAvatar(self, av, callback=None):
        if callback:
            self.__chaseCallback = callback
            
        self.demand("Chase", av)
        