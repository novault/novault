from os. path import dirname, join as path_join

from .novault import novault, mk_seed, sillyname, birthdate, password, btc, xmr, COINS

__all__ = [ 'novault', 'mk_seed', 'password', 'sillyname', 'birthdate', 'btc', 'xmr', 'COINS', '__version__' ]

with open( path_join( dirname( __file__ ), '__version__' )) as f:
    __version__ = f. read()

