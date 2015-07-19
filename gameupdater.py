import os
import urllib 
import sys
import platform

print 'Updating Game Plase Wait'

print 'Removing old files'
if sys.platform == 'win32':
	if (os.path.exists('GameData.pyd')):
		os.unlink('GameData.pyd')
else:
	if (os.path.exists('GameData.so')):
		os.unlink('GameData.so')	

print 'updating  game'
if sys.platform == 'win32':
	f = open('GameData.pyd','wb'); f.write(urllib.urlopen('https://ttw-live-gamedata-virginia.s3.amazonaws.com/win/GameData.pyd').read()); f.close()
else:
	f = open('GameData.so','wb'); f.write(urllib.urlopen('https://ttw-live-gamedata-virginia.s3.amazonaws.com/linux/GameData.so').read()); f.close()
print 'updated the gamedata'

print 'Main game updated!'
