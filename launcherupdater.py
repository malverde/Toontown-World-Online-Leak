import os
import urllib

print 'Removing old files'

if (os.path.exists('launcher.py')):
	os.unlink('launcher.py')
	

if (os.path.exists('gameupdater.py')):
	os.unlink('gameupdater.py')

if (os.path.exists('phaseupdater.py')):
	os.unlink('phaseupdater.py')
	
if (os.path.exists('GameLaunch.py')):
	os.unlink('GameLaunch.py')
	
if (os.path.exists('phase_2.mf')):
	os.unlink('phase_2.mf')

print 'updating phase updater'
f = open('phaseupdater.py','wb'); f.write(urllib.urlopen('https://ttw-live-gamedata-virginia.s3.amazonaws.com/syst/phaseupdater.py').read()); f.close()
print 'patched phase updater!'

print 'updating game updater'
f = open('gameupdater.py','wb'); f.write(urllib.urlopen('https://ttw-live-gamedata-virginia.s3.amazonaws.com/syst/gameupdater.py').read()); f.close()
print 'patched game updater!'

print 'updating launcher'
f = open('launcher.py','wb'); f.write(urllib.urlopen('https://ttw-live-gamedata-virginia.s3.amazonaws.com/syst/launcher.py').read()); f.close()
print 'patched launcher!'

print 'updating game launcher'
f = open('Gamelaunch.py','wb'); f.write(urllib.urlopen('https://ttw-live-gamedata-virginia.s3.amazonaws.com/syst/Gamelaunch.py').read()); f.close()
print 'patched game launcher!'

print 'updating phase_2'
f = open('phase_2.mf','wb'); f.write(urllib.urlopen('https://ttw-live-gamedata-virginia.s3.amazonaws.com//phase_2.mf').read()); f.close()
print 'patched phase_2!'

print 'updating start file'
f = open('Toontown World Online Launcher.exe','wb'); f.write(urllib.urlopen('https://ttw-live-gamedata-virginia.s3.amazonaws.com/win/Toontown World Online Launcher.exe').read()); f.close()
print 'updated some launcher files'
