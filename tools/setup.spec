# -*- mode: python -*-
a = Analysis(['setup.py'],
             pathex=['C:\\Users\\michael\\Desktop\\tools'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='setup.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True )
