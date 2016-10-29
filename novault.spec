# -*- mode: python -*-

from sys import path
from platform import system, machine

path.append( '.' )
path.append( 'novault' )
from novault import __version__

exe_name = '-'. join([ 'novault', __version__, system(). casefold(), machine(). casefold() ])

block_cipher = None

a = Analysis(['main.py'],
             pathex=['novault'],
             binaries=None,
             datas=None,
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
          name=exe_name,
          debug=False,
          strip=False,
          upx=True,
          console=True )
