# -*- mode: python -*-

from math import log2
from sys import maxsize, path
from platform import system, machine

from novault import __version__

bits = str( int( log2( maxsize + 1 ) + 1 )) + 'bit'
exe_name = '-'. join([ 'novault', __version__, system(). casefold(), machine(). casefold(), bits ])

block_cipher = None

a = Analysis(['main.py'],
             pathex=['novault'],
             binaries=None,
             datas=None,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=['PyQt4','gtk'],
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
