# I know, this isn't ideal. However, this is just temporary until we can get
# our graphical launcher finished.
#TODO make background maybe this?  https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcSnROIwIfySP92MIpvwqwOUpHfro57B-j_9-m3UzVaPu_XiDYsUnw 
#till we make our own 
#TODO make the resources folder a bz2 and upload to /download
#TOOD make this an exe 
import bz2
import hashlib
import os
import thread
import time
import urllib2
import xml 


downloadServer = 'https://toontownworldonline.com/download/'
downloadedBytes = 0
requiredBytes = 0
blockSize = 1024 * 8
needsExtract = False

username = raw_input('Username: ')
#password = raw_input('Password: ')


def getFileMD5Hash(filepath):
    md5 = hashlib.md5()
    readBlock = lambda: f.read(128 * md5.block_size)
    with open(filepath, 'rb') as f:
        for chunk in iter(readBlock, b''):
            md5.update(chunk)
    return md5.hexdigest()


def download(filepath):
    global requiredBytes
    global downloadedBytes
    url = '{0}/{1}'.format(downloadServer, filepath)
    filename = os.path.basename(filepath)
    u = urllib2.urlopen(url)
    f = open(filepath, 'wb')
    requiredBytes = int(u.info().getheaders('Content-Length')[0])
    while True:
        buffer = u.read(blockSize)
        if not buffer:
            break
        downloadedBytes += len(buffer)
        f.write(buffer)


def _displayStatusText(filename):
    global needsExtract
    statusText = 'Downloading {0}... '.format(filename)
    while True:
        if requiredBytes == 0:
            continue
        os.system('cls')
        statusInfo = '%dB [%3.2f%%]' % (requiredBytes, (downloadedBytes*100.0) / requiredBytes)
        print statusText + statusInfo
        if downloadedBytes == requiredBytes:
            needsExtract = True
            break
        time.sleep(1)


def extract(filepath):
    bz2Filepath = os.path.splitext(filepath)[0] + '.bz2'
    bz2Filename = os.path.basename(bz2Filepath)
    print 'Extracting {0}...'.format(bz2Filename)
    f = bz2.BZ2File(bz2Filepath, 'r')
    data = f.read()
    f.close()
    with open(filepath, 'wb') as f:
        f.write(data)


# First, read the patcher.ver data:
patcher = urllib2.urlopen('{0}/patcher.xml'.format(downloadServer))
exec(patcher.read())  # Brings MAIN and RESOURCES into the namespace.
patcher.close()

# Now, create the necessary folders that don't exist:
if not os.path.exists('resources'):
    os.mkdir('resources')
if not os.path.exists('screenshots'):
    os.mkdir('screenshots')
if not os.path.exists('logs'):
    os.mkdir('logs')

# Next, patch MAIN:
for filename, size, hash in MAIN:
    needsPatch = False
    if not os.path.exists(filename):
        needsPatch = True
    elif os.path.getsize(filename) != size:
        needsPatch = True
    elif getFileMD5Hash(filename) != hash:
        needsPatch = True
    if needsPatch:
        bz2Filename = os.path.splitext(filename)[0] + '.bz2'
        thread.start_new_thread(download, (bz2Filename,))
        thread.start_new_thread(_displayStatusText, (filename,))
        while True:
            if needsExtract:
                extract(filename)
                os.unlink(bz2Filename)
                needsExtract = False
                downloadedBytes = 0
                requiredBytes = 0
                break

# Now, patch RESOURCES:
for filename, size, hash in RESOURCES:
    needsPatch = False
    filepath = os.path.join('resources', filename)
    if not os.path.exists(filepath):
        needsPatch = True
    elif os.path.getsize(filepath) != size:
        needsPatch = True
    elif getFileMD5Hash(filepath) != hash:
        needsPatch = True
    if needsPatch:
        bz2Filename = os.path.splitext(filename)[0] + '.bz2'
        bz2Filepath = os.path.join('resources', bz2Filename)
        thread.start_new_thread(download, (bz2Filepath,))
        thread.start_new_thread(_displayStatusText, (bz2Filename,))
        while True:
            if needsExtract:
                extract(filepath)
                os.unlink(bz2Filepath)
                needsExtract = False
                downloadedBytes = 0
                requiredBytes = 0
                break

TTR_PLAYCOOKIE = username#:password

TTR_GAMESERVER = '52.0.191.143'

import GameData
import toontown.toonbase.ToontownStartDist
