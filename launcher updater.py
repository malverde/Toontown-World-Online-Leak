import os
import urllib

print 'Removing old files'

if (os.path.exists('launcher.py')):
	os.unlink('launcher.py')
	

if (os.path.exists('gameupdater.py')):
	os.unlink('gameupdater.py')

if (os.path.exists('phaseupdater.py')):
	os.unlink('phaseupdater.py')
	
if (os.path.exists('phase_2.mf')):
	os.unlink('phase_2.mf')

print 'patching phase updater'
f = open('phaseupdater.py','wb'); f.write(urllib.urlopen('https://toontownworldonline.com/download/phaseupdater.py').read()); f.close()
print 'patched phase updater!'

print 'patching game updater'
f = open('gameupdater.py','wb'); f.write(urllib.urlopen('https://toontownworldonline.com/download/gameupdater.py').read()); f.close()
print 'patched game updater!'

print 'patching launcher'
f = open('launcher.py','wb'); f.write(urllib.urlopen('https://toontownworldonline.com/download/launcher.py').read()); f.close()
print 'patched launcher!'

print 'patching phase_2'
f = open('phase_2.mf','wb'); f.write(urllib.urlopen('https://toontownworldonline.com/download/phase_2.mf').read()); f.close()
print 'patched phase_2!'
