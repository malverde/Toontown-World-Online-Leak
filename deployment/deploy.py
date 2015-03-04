#!/usr/bin/env python2
import StringIO
import copy
import ftplib
import json
import os
import shutil
import subprocess
import sys
import tarfile
from xml.etree import ElementTree

import bz2


# We have some dependencies that aren't in the standard Python library. Notify
# the user if they are missing one:
try:
    import requests
except ImportError, e:
    print 'Missing dependency:', e.message[16:]
    print 'It is recommended that you install this using Pip.'
    sys.exit(1)

print 'Starting the deployment process...'

# Stop the user if they are missing vital files:
missingFiles = []
for filename in ('deploy.json'):
    if sys.platform == 'win32':
        # On the Windows platform, if there is no extension, we must infer that
        # this is an executable file. Therefore, let's append '.exe':
        if not os.path.splitext(filename)[1]:
            filename += '.exe'
    if filename not in os.listdir('.'):
        missingFiles.append(filename)
if missingFiles:
    for filename in missingFiles:
        print 'Missing file:', filename
    sys.exit(1)

print 'Reading deploy configuration...'
with open('deploy.json', 'r') as f:
    deployData = json.load(f)

# Next, we must choose the correct path to Python for our Panda3D installation:
if sys.platform == 'win32':
    with open('../PPYTHON_PATH', 'r') as f:
        pythonPath = f.read().strip()
else:
    pythonPath = '/usr/bin/python2'

# Collect our FTP credentials:
ftpAddress = deployData['ftp-address']
ftpUsername = deployData['ftp-username']
if not ftpUsername:
    print 'Missing FTP username.'
ftpPassword = deployData['ftp-password']
if not ftpPassword:
    print 'Missing FTP password.'
    sys.exit(1)

# Ensure that the platform we're building for is supported:
platform = deployData['platform']
if platform not in ('win32', 'linux2', 'darwin'):  # Supported platforms
    print 'Unsupported platform:', platform
    sys.exit(2)

# Ensure that the distribution we're building for is supported:
distribution = deployData['distribution']
if distribution not in ('dev', 'test', 'en'):  # Supported distributions
    print 'Unsupported distribution:', distribution
    sys.exit(2)

deployToken = distribution + '/' + platform

# Ensure the desired source code branch exists:
branch = deployData['branch']
os.chdir('..')
branches = subprocess.Popen(
    ['git', 'rev-parse', '--abbrev-ref', '--branches', 'HEAD'],
    stdout=subprocess.PIPE).stdout.read().split()
if branch not in branches:
    print "No local source code branch named:", branch
    sys.exit(3)

# Check if the desired resources branch exists:
resourcesBranch = deployData['resources-branch']
os.chdir('../resources')
branches = subprocess.Popen(
    ['git', 'rev-parse', '--abbrev-ref', '--branches', 'HEAD'],
    stdout=subprocess.PIPE).stdout.read().split()
if resourcesBranch not in branches:
    print "No local resources branch named:", resourcesBranch
    sys.exit(3)

# We're all set. Let's gather the rest of the deployment configurations:
serverVersion = deployData['version-prefix'] + deployData['version']
launcherVersion = deployData['launcher-version']
accountServer = deployData['account-server']
clientAgent = deployData['client-agent']
patcherIncludes = deployData['patcher-includes']
configDir = deployData['config-dir']
vfsMounts = deployData['vfs-mounts']
modules = deployData['modules']
mainModule = deployData['main-module']

# ...and output them for verbosity:
print 'Deploy token:', deployToken
print 'Branch:', branch
print 'Resources branch:', resourcesBranch
print 'Server version:', serverVersion
print 'Configuration directory:', configDir
print 'Virtual file system (%d):' % len(vfsMounts)
for vfsMount in vfsMounts:
    print '  %s' % vfsMount
print 'Modules (%d):' % len(modules)
for module in modules:
    print '  %s' % module
print 'Main module:', mainModule

# Create a 'src' directory containing the source code from the desired branch:
sys.stdout.write('Collecting source code from branch: ' + branch + '... 0%')
sys.stdout.flush()
os.chdir('../src')
if os.path.exists('deployment/src'):
    shutil.rmtree('deployment/src')
os.mkdir('deployment/src')
td = subprocess.Popen(['git', 'archive', branch],
                      stdout=subprocess.PIPE).stdout.read()
tss = StringIO.StringIO(td)
tf = tarfile.TarFile(fileobj=tss)
directories = []
members = tf.getmembers()
for (i, ti) in enumerate(members):
    if ti.isdir():
        directories.append(ti)
        ti = copy.copy(ti)
        ti.mode = 0o700
    tf.extract(ti, 'deployment/src')
    percentage = int((float(i+1)/len(members)) * 100)
    sys.stdout.write('\rCollecting source code from branch: ' + branch +
                     '... ' + str(percentage) + '%')
    sys.stdout.flush()
directories.sort(key=lambda a: a.name)
directories.reverse()
for ti in directories:
    dirpath = os.path.join('deployment/src', ti.name)
    try:
        tf.chown(ti, dirpath)
        tf.utime(ti, dirpath)
        tf.chmod(ti, dirpath)
    except tarfile.ExtractError as e:
        if tf.errorlevel > 1:
            raise
        else:
            tf._dbg(1, 'tarfile: %s' % e)
sys.stdout.write('\n')
sys.stdout.flush()

# Create a 'resources' directory inside the 'src' directory containing all of
# the resource files from the desired resources branch:
sys.stdout.write('Collecting resources from branch: ' + resourcesBranch + '... 0%')
sys.stdout.flush()
os.chdir('../resources')
td = subprocess.Popen(['git', 'archive', resourcesBranch],
                      stdout=subprocess.PIPE).stdout.read()
tss = StringIO.StringIO(td)
tf = tarfile.TarFile(fileobj=tss)
os.chdir('../src/deployment')
directories = []
members = tf.getmembers()
for (i, ti) in enumerate(members):
    if ti.isdir():
        directories.append(ti)
        ti = copy.copy(ti)
        ti.mode = 0o700
    tf.extract(ti, 'src/resources')
    percentage = int((float(i+1)/len(members)) * 100)
    sys.stdout.write('\rCollecting resources from branch: ' + resourcesBranch +
                     '... ' + str(percentage) + '%')
    sys.stdout.flush()
directories.sort(key=lambda a: a.name)
directories.reverse()
for ti in directories:
    dirpath = os.path.join('src/resources', ti.name)
    try:
        tf.chown(ti, dirpath)
        tf.utime(ti, dirpath)
        tf.chmod(ti, dirpath)
    except tarfile.ExtractError as e:
        if tf.errorlevel > 1:
            raise
        else:
            tf._dbg(1, 'tarfile: %s' % e)
sys.stdout.write('\n')
sys.stdout.flush()

# All of our source code and resources are collected. Now, let's run the
# prepare_client utility:
cmd = (pythonPath + ' ../tools/prepare_client.py' +
       ' --distribution ' + distribution +
       ' --build-dir build' +
       ' --src-dir src' +
       ' --server-ver ' + serverVersion +
       ' --build-mfs' +
       ' --resources-dir src/resources' +
       ' --config-dir ' + configDir +
       ' --include NonRepeatableRandomSourceUD.py' +
       ' --include NonRepeatableRandomSourceAI.py' +
       ' --exclude ServiceStart.py')
for vfsMount in vfsMounts:
    cmd += ' --vfs ' + vfsMount
for module in modules:
    cmd += ' ' + module
os.system(cmd)

# Next, run the build_client utility:
if sys.platform == 'win32':
    output = 'GameData.pyd'
else:
    output = 'GameData.so'
cmd = (pythonPath + ' ../tools/build_client.py' +
       ' --output ' + output +
       ' --main-module ' + mainModule +
       ' --build-dir build')
for module in modules:
    cmd += ' ' + module
os.system(cmd)


# Copy the necessary patcher includes:
for include in patcherIncludes:
    dirname = os.path.dirname(include)
    if dirname and (not os.path.exists(dirname)):
        os.makedirs(dirname)
    if os.path.exists(os.path.join('..', include)):
        shutil.copyfile(os.path.join('..', include), include)

# Create a 'dist' directory that will contain everything that will be uploaded
# to the CDN:
os.chdir('..')
if os.path.exists('dist'):
    shutil.rmtree('dist')
os.mkdir('dist')

# Now, if we have deployed a previous version of this distribution before,
# let's get the last resources revision so that we can choose what phase files
# need to be updated using 'git diff'. We need to do this because two
# compilations of the same multifile will never have the same hash:
updatedFiles = []
request = requests.get('http://' + ftpAddress + '/' + deployToken + '/patcher.xml')
try:
    root = ElementTree.fromstring(request.text)
except:
    root = None
os.chdir('../resources')
if root and (root.tag == 'patcher'):  # We have a patcher file
    resourcesRevision = root.find('resources-revision')
    if resourcesRevision is not None:
        resourcesRevision = resourcesRevision.text
        diff = subprocess.Popen(
            ['git', 'diff', '--name-only', resourcesRevision, resourcesBranch],
            stdout=subprocess.PIPE).stdout.read()
        filenames = diff.split('\n')
        for filename in filenames:
            directory = filename.split('/', 1)[0].split('\\', 1)[0]
            if directory.startswith('phase_'):
                phase = 'resources/' + directory + '.mf'
                if phase not in updatedFiles:
                    updatedFiles.append(phase)
resourcesRevision = subprocess.Popen(
    ['git', 'rev-parse', resourcesBranch],
    stdout=subprocess.PIPE).stdout.read()[:7]
os.chdir('../src/deployment')
updatedFiles.extend(patcherIncludes)

cmd = (pythonPath + ' ../tools/write_patcher.py' +
       ' --build-dir build' +
       ' --dest-dir dist' +
       ' --output patcher.xml' +
       ' --launcher-version ' + launcherVersion +
       ' --account-server ' + accountServer +
       ' --client-agent ' + clientAgent +
       ' --server-version ' + serverVersion +
       ' --resources-revision ' + resourcesRevision)
for include in patcherIncludes:
    cmd += ' ' + include
os.system(cmd)

et = ElementTree.parse('dist/patcher.xml')
localRoot = et.getroot()
for directory in localRoot.findall('directory'):
    directoryName = directory.get('name')
    # If we haven't pushed a patcher previously, we can assume this is the
    # first time deploying this distribution. Therefore, let's upload
    # everything:
    if (not root) or (root.tag != 'patcher'):
        for child in directory.getchildren():
            filepath = child.get('name')
            if directoryName:
                filepath = directoryName + '/' + filepath
            if filepath not in updatedFiles:
                updatedFiles.append(filepath)
    else:
        # Otherwise, we'll want to ensure that we don't overwrite certain
        # files' size/hash, in case they weren't updated:
        for child in directory.getchildren():
            filepath = child.get('name')
            if directoryName:
                filepath = directoryName + '/' + filepath
            if filepath not in updatedFiles:
                for _directory in root.findall('directory'):
                    if _directory.get('name') != directoryName:
                        continue
                    for _child in _directory.getchildren():
                        if _child.get('name') != child.get('name'):
                            continue
                        child.find('size').text = _child.find('size').text
                        child.find('hash').text = _child.find('hash').text
                        break
                    break
ElementTree.ElementTree(localRoot).write('dist/patcher.xml')


def compressFile(filepath):
    with open(filepath, 'rb') as f:
        data = f.read()
    filename = os.path.basename(filepath)
    directory = filepath[6:].split(filename, 1)[0]
    if not os.path.exists(os.path.join('dist', directory)):
        os.mkdir(os.path.join('dist', directory))
    bz2Filename = os.path.splitext(filename)[0] + '.bz2'
    bz2Filepath = os.path.join('dist', directory, bz2Filename)
    f = bz2.BZ2File(bz2Filepath, 'w')
    f.write(data)
    f.close()


# Compress the updated files:
for filepath in updatedFiles:
    print 'Compressing %s...' % filepath
    compressFile(os.path.join('build', filepath))

print 'Uploading files to download.toontowninfinite.com...'
ftp = ftplib.FTP(ftpAddress, ftpUsername, ftpPassword)
ftp.cwd(deployToken)

print 'Uploading... patcher.xml'
with open('dist/patcher.xml', 'rb') as f:
    ftp.storbinary('STOR patcher.xml', f)


for filepath in updatedFiles:
    filepath = os.path.splitext(filepath)[0] + '.bz2'
    print 'Uploading... ' + filepath
    with open('dist/' + filepath, 'rb') as f:
        ftp.storbinary('STOR ' + filepath, f)

print 'Done uploading files.'

print 'Successfully finished the deployment process!'
