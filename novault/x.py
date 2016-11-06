from binascii import hexlify, unhexlify
from itertools import takewhile

_b58_buf_len = ( 0, 2, 3, 5, 6, 7, 9, 10, 11, 13, 14, 16, 17, 18, 20, 21, 22, 24, 25, 26, 28, 29, 31, 32, 33, 35, 36, 37, 39, 40, 41, 43, 44 )
def _b58( value ):
    '''Convert big-endian bytes to a Base58 string'''
    print( hexlify( value ))
    v, z, r = int. from_bytes( value, 'big' ), sum( 1 for _ in takewhile( int( 0 ). __eq__, value )), ''
    while v:
        v, c = divmod( v, 58 )
        print( v, c )
        r = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'[ c ] + r

    z = _b58_buf_len[ len( value )] - len( r )
    print( '1' * z + r )
    return '1' * z + r

_b58( unhexlify( b'051a9d90f13feb12' ))
