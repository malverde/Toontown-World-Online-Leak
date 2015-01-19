from distutils.core import setup
import py2exe

setup(windows=[{'script': 'start.py', 'icon_resources': [(0, 'icon.ico')]}], options= {'py2exe': {'bundle_files': 1, 'compressed': True, 'dll_excludes': ['w9xpopen.exe']}}, zipfile = None)