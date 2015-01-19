import json
import urllib2
import sys
import os
from ManagedFile import ManagedFile

####################################################################################################
# FIXME: The stuff where mirror lists are obtained is done on module import, so either move it to the Patch method, or import the module later!
####################################################################################################

# Start by getting our base directory
PATCHER_BASE = os.environ.get('PATCHER_BASE', './')
# Try to find our list of mirrors
print 'Obtaining available mirrors...'
MIRRORS = []
try:
    remoteMirrors = urllib2.urlopen('https://www.toontownrewritten.com/api/mirrors', timeout=20) # Don't wait too long for the dynamic mirrors list
    MIRRORS = json.loads(remoteMirrors.read())
    print 'Obtained %s mirrors from remote server.' % len(MIRRORS)
except:
    pass # Whatever
if not MIRRORS:
    try:
        # We need to try our backup mirror location
        remoteMirrors = urllib2.urlopen('http://s3.amazonaws.com/cdn.toontownrewritten.com/mirrors.txt', timeout=10)
        MIRRORS = json.loads(remoteMirrors.read())
        print 'Obtained %s mirrors from backup remote server.' % len(MIRRORS)
    except:
        pass
if not MIRRORS:
    # We can't obtain any remote mirror lists, so just use the single hardcoded mirror we know of
    MIRRORS = ['http://s3.amazonaws.com/cdn.toontownrewritten.com/content/']
    print 'Unable to obtain remote mirror list! Using local backup instead.'
 
# de-unicodify the mirrors, just to keep with convention of all patcher strings are ascii
MIRRORS = [mirror.encode('ascii') for mirror in MIRRORS]
 
MANIFEST_URL = 'http://s3.amazonaws.com/cdn.toontownrewritten.com/content/patchmanifest.txt'
 
# Begin by obtaining the manifest
MANIFEST = urllib2.urlopen(MANIFEST_URL).read()
MANIFEST = json.loads(MANIFEST)
 
# Now create ManagedFiles
files = []
 
# This is gross and bad and I'm sorry jj
def Patch(progressCallback=None, fileCallback=None):
    count = 0
    for filename in MANIFEST:
        global count
        count += 1
        entry = MANIFEST.get(filename)
        print 'Updating file %s of %s, %s...' % (count, len(MANIFEST), filename)
        if fileCallback is not None:
            fileCallback('Updating file %s of %s' % (count, len(MANIFEST)))
        if sys.platform not in entry.get('only', ['linux2', 'win32', 'darwin']):
            print 'Skipped updating, file is not required on this platform.'
            continue
        managedFile = ManagedFile(filename, installBase=PATCHER_BASE, hash=entry.get('hash'), dl=entry.get('dl'), compHash=entry.get('compHash'), progressCallback=progressCallback)
        managedFile.update(MIRRORS, patches=entry.get('patches'))
        files.append(managedFile)

#if __name__ == '__main__':
#    Patch()