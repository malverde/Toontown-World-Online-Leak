# -*- mode: ppython -*-
a = Analysis(['start.py'],
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
          name='Launcher.exe',
          debug=False,
          strip=None,
          upx=True,
          console=False,
          icon='icon.ico' )
