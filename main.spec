# -*- mode: python -*-
import shutil

block_cipher = None

a = Analysis(['main.py'],
             pathex=['C:\\Games\\tornconsole'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='tornconsole',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
          
shutil.copyfile('settings.ini.example', '{0}/settings.ini.example'.format(DISTPATH))