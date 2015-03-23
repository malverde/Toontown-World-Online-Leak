from pandac.PandaModules import *

class CMover:
    
    def __init__(self, objNodePath, fwdSpeed=1, rotSpeed=1):
        self.objNodePath = objNodePath
        self.fwdSpeed = fwdSpeed
        self.rotSpeed = rotSpeed
        