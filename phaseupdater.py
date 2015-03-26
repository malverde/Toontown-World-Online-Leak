import os
import urllib 

print 'Updating phase files Plase Wait'

print 'Removing old phase files.'

if (os.path.exists('phase_3.mf')):
	os.unlink('phase_3.mf')

if (os.path.exists('phase_4.mf')):
	os.unlink('phase_4.mf')
	
if (os.path.exists('phase_3.5.mf')):
	os.unlink('phase_3.5.mf')
	
if (os.path.exists('phase_5.mf')):
	os.unlink('phase_5.mf')
	
if (os.path.exists('phase_5.5.mf')):
	os.unlink('phase_5.5.mf')
	
if (os.path.exists('phase_6.mf')):
	os.unlink('phase_6.mf')
	
if (os.path.exists('phase_7.mf')):
	os.unlink('phase_7.mf')
	
if (os.path.exists('phase_8.mf')):
	os.unlink('phase_8.mf')
	
if (os.path.exists('phase_9.mf')):
	os.unlink('phase_9.mf')
	
if (os.path.exists('phase_10.mf')):
	os.unlink('phase_10.mf')
	
if (os.path.exists('phase_11.mf')):
	os.unlink('phase_11.mf')
	
if (os.path.exists('phase_12.mf')):
	os.unlink('phase_12.mf')
	
if (os.path.exists('phase_13.mf')):
	os.unlink('phase_13.mf')
	
print 'patching phase 12'
f = open('phase_12.mf','wb'); f.write(urllib.urlopen('https://toontownworldonline.com/download/phase_2.mf').read()); f.close()
print 'patched phase 12'
print 'patching phase 3'
f = open('phase_3.mf','wb'); f.write(urllib.urlopen('https://toontownworldonline.com/download/phase_3.mf').read()); f.close()
print 'patched phase 3'
print 'patching phase 3.5'
f = open('phase_3.5.mf','wb'); f.write(urllib.urlopen('https://toontownworldonline.com/download/phase_3.5.mf').read()); f.close()
print 'patched phase 3.5'
print 'patching phase 4'
f = open('phase_4.mf','wb'); f.write(urllib.urlopen('https://toontownworldonline.com/download/phase_4.mf').read()); f.close()
print 'patched phase 4'
print 'patching phase 5'
f = open('phase_5.mf','wb'); f.write(urllib.urlopen('https://toontownworldonline.com/download/phase_5.mf').read()); f.close()
print 'patched phase 5'
print 'patching phase 5.5'
f = open('phase_5.5.mf','wb'); f.write(urllib.urlopen('https://toontownworldonline.com/download/phase_5.5.mf').read()); f.close()
print 'patched phase 5.5'
print 'patching phase 6'
f = open('phase_6.mf','wb'); f.write(urllib.urlopen('https://toontownworldonline.com/download/phase_6.mf').read()); f.close()
print 'patched phase 6'
print 'patching phase 7'
f = open('phase_7.mf','wb'); f.write(urllib.urlopen('https://toontownworldonline.com/download/phase_7.mf').read()); f.close()
print 'patched phase 7'
print 'patching phase 8'
f = open('phase_8.mf','wb'); f.write(urllib.urlopen('https://toontownworldonline.com/download/phase_8.mf').read()); f.close()
print 'patched phase 8'
print 'patching phase 9'
f = open('phase_9.mf','wb'); f.write(urllib.urlopen('https://toontownworldonline.com/download/phase_9.mf').read()); f.close()
print 'patched phase 9'
print 'patching phase 11'
f = open('phase_11.mf','wb'); f.write(urllib.urlopen('https://toontownworldonline.com/download/phase_11.mf').read()); f.close()
print 'patched phase 11'
print 'patching phase 12'
f = open('phase_12.mf','wb'); f.write(urllib.urlopen('https://toontownworldonline.com/download/phase_12.mf').read()); f.close()
print 'patched phase 12'
print 'patching phase 13'
f = open('phase_13.mf','wb'); f.write(urllib.urlopen('https://toontownworldonline.com/download/phase_13.mf').read()); f.close()
print 'patched phase 13'
print 'patching phase 10'
f = open('phase_10.mf','wb'); f.write(urllib.urlopen('https://toontownworldonline.com/download/phase_10.mf').read()); f.close()
print 'patched phase 10'

print 'All phase files updated!'
