import os 
username = raw_input('Username: ' )
#password = raw_input('Password: ')
os.environ['TTR_PLAYCOOKIE'] =  username
import panda3d.core 
import GameData
import toontown.toonbase.ToontownStartDist
