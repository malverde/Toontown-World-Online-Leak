import os
import urllib 
import platform

print 'Updating Game Plase Wait'

print 'Removing old files'
if platform == 'win32':
	if (os.path.exists('GameData.pyd')):
		os.unlink('GameData.pyd')
if platform == 'darwin':
	if (os.path.exists('GameData.so')):
		os.unlink('GameData.so')	

print 'updating  game'
if platform == 'win32':
	f = open('GameData.pyd','wb'); f.write(urllib.urlopen('https://toontownworldonline.com/download/GameData.pyd').read()); f.close()
if platform == 'darwin':
	f = open('GameData.so','wb'); f.write(urllib.urlopen('https://toontownworldonline.com/download/GameData.so').read()); f.close()
print 'updated the gamedata'

print 'Main game updated!'
