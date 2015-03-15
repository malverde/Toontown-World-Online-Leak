import argparse
import os


parser = argparse.ArgumentParser()
parser.add_argument('--panda3d-dir', default='C:/Panda3D-1.9.0',
                    help='The path to the Panda3D build to use for this distribution.')
parser.add_argument('--main-module', default='toontown.toonbase.ToontownStartDist',
                    help='The path to the instantiation module.')
parser.add_argument('modules', nargs='*', default=['otp', 'toontown'],
                    help='The Toontown modules to be included in the build.')
args = parser.parse_args()

print 'Building the client...'

os.chdir('build')

cmd = os.path.join(args.panda3d_dir, 'python/ppython.exe')
cmd += ' -m direct.showutil.pfreeze'
args.modules.extend(['direct', 'pandac'])
for module in args.modules:
    cmd += ' -i {0}.*.*'.format(module)
cmd += ' -i {0}.*'.format('encodings')
cmd += ' -i {0}'.format('base64')
cmd += ' -i {0}'.format('site')
cmd += ' -o GameData.pyd'
cmd += ' {0}'.format(args.main_module)

os.system(cmd)

print 'Done building the client.'