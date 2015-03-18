import os 
username = = raw_input('Username: ' )
#password = raw_input('Password: ')
os.environ['TTR_PLAYCOOKIE'] =  username
os.environ['TTR_GAMESERVER'] = '52.0.191.143'
import panda3d.core 
import GameData
import toontown.toonbase.ToontownStartDist
