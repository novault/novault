#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#    novault
#    Copyright (c) 2016 Avner Herskovits
#
#    MIT License
#
#    Permission  is  hereby granted, free of charge, to any person  obtaining  a
#    copy of this  software and associated documentation files (the "Software"),
#    to deal in the Software  without  restriction, including without limitation
#    the rights to use, copy, modify, merge,  publish,  distribute,  sublicense,
#    and/or  sell  copies of  the  Software,  and to permit persons to whom  the
#    Software is furnished to do so, subject to the following conditions:
#
#    The above copyright notice and this  permission notice shall be included in
#    all copies or substantial portions of the Software.
#
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT  WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE  WARRANTIES  OF  MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR  ANY  CLAIM,  DAMAGES  OR  OTHER
#    LIABILITY, WHETHER IN AN  ACTION  OF  CONTRACT,  TORT OR OTHERWISE, ARISING
#    FROM,  OUT  OF  OR  IN  CONNECTION WITH THE SOFTWARE OR THE  USE  OR  OTHER
#    DEALINGS IN THE SOFTWARE.
#

# stdlib
from argparse import ArgumentParser, ArgumentTypeError, REMAINDER
from base64 import b85encode
from binascii import hexlify
from datetime import date, timedelta
from getpass import getpass
from hashlib import new as hashlib_new
from itertools import takewhile
from os import urandom
from re import match
from sys import exit

# pypi
from ecdsa import SigningKey, SECP256k1
from pyperclip import copy as pyperclip_copy
from pyscrypt import hash as pyscrypt_hash

# local modules
from novault.ed25519 import B as BASE, encodepoint, l as GROUPGEN, scalarmult
from novault.Keccak import Keccak

def _b58( value ):
    '''Convert big-endian bytes to a Base58 string'''
    v, z, r = int. from_bytes( value, 'big' ), sum( 1 for _ in takewhile( int( 0 ). __eq__, value )), ''
    while v:
        v, c = divmod( v, 58 )
        r = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'[ c ] + r
    return '1' * z + r

def novault( action, description, master ):
    '''Generate a password or wallet from given description & master password'''
    return action( mk_seed( description, master, action() ))

def mk_seed( description, master, length ):
    '''Generate pseudorandom seed of desired length from description & master password'''
    S0, S1, S2 = b'%<6>0Mk$ziGdz@:z-O-', b'Jea`_uH6.ji4R$VM1ZB', b'C!#1P4zJLB2O=no06[1'
    return pyscrypt_hash(
        description + S0 + master,
        pyscrypt_hash( description + S1 + master, master + S2 + description, 1024, 1, 1, 32 ),
        1024, 1, 1, length )

def placebo( seed = None ):
    '''Passthrough action'''
    if not seed: return 0
    return { None: hexlify( seed ). decode( 'latin_1' )}

def password( seed = None ):
    '''Generate a 128 bit password from seed'''
    if not seed: return 16
    password = list( b85encode( seed ). decode( 'latin_1' ))
    pass_len = len( password )  # always 20
    ornament = int. from_bytes( seed[ 12: ], 'little')
    for chr_class in ( '0123456789', 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', '.,:[]/' ):
        pass_len += 1
        ornament, pos  = divmod( ornament, pass_len )
        ornament, char = divmod( ornament, len( chr_class ))
        password. insert( pos, chr_class[ char ])
    result = { 'password': ''. join( password )}
    result[ None ] = result[ 'password' ]
    return result

# btc
def _hash( msg, algo ): hash = hashlib_new( algo ); hash. update( msg ); return hash. digest()
_sha256    = lambda v: _hash( v, 'sha256' )
_ripemd160 = lambda v: _hash( v, 'ripemd160' )

def btc( seed = None ):
    '''Generate BTC address and key from seed'''
    if not seed: return 32
    private_key = b'\x80' + seed + b'\x01'
    private_key += _sha256( _sha256( private_key ))[ :4 ]
    public_key_uncomp = bytes( SigningKey. from_string( seed, curve = SECP256k1 ). get_verifying_key(). to_string() )
    public_key = b'\x03' if public_key_uncomp[ -1 ] & 1 else b'\x02'
    public_key += public_key_uncomp[ :32 ]
    address = b'\x00' + _ripemd160( _sha256( public_key ))
    address += _sha256( _sha256( address ))[ :4 ]
    result = { 'key': _b58( private_key ), 'address': _b58( address )}
    result[ None ] = result[ 'address' ]
    return result

# xmr
_hex = lambda v: hexlify( v. to_bytes( 32, 'little' )). decode( 'latin_1' )
_int = lambda v: int. from_bytes( bytes. fromhex( v ), 'little' )

_keccak_256  = lambda v: Keccak(). Keccak(( len( v ) * 4, v ), 1088, 512, 0x01, 256, False ). lower()
_sc_reduce32 = lambda v: _hex( _int( v ) % GROUPGEN )
_derive_key  = lambda v: _sc_reduce32( _keccak_256( v ))
_secret2pub  = lambda v: hexlify( encodepoint( scalarmult( BASE, _int( v ))). encode( 'latin_1' )). decode( 'latin_1' )
_funny_b58   = lambda v: ''. join( _b58( bytes. fromhex( v[ i: i + 16 ])) for i in range( 0, len( v ), 16 ))
_monero_addr = lambda v: _funny_b58( v + _keccak_256( v )[ :8 ] )

def xmr( seed = None ):
    '''Generate XMR address and private spend and view keys from seed'''
    if not seed: return 32
    ssk = _sc_reduce32( hexlify( seed ). decode( 'latin_1' ))
    svk = _derive_key( ssk )
    address = _monero_addr( '12' + _secret2pub( ssk ) + _secret2pub( svk ))
    return { 'address': address, 'spend': ssk, 'view': svk, None: address }

COINS = ( 'btc', 'xmr' )

consonants = ( 'b', 'bj', 'bl', 'br', 'c', 'ch', 'cj', 'ck', 'cl', 'cr', 'd', 'dj', 'dl', 'dr', 'dv', 'dw', 'f', 'fj', 'fl', 'fn', 'fr',
    'g', 'gd', 'gl', 'gn', 'gr', 'gw', 'h', 'j', 'jl', 'jr', 'k', 'kd', 'kf', 'kj', 'kl', 'kn', 'kp', 'kr', 'ks', 'kv',
    'l', 'lj', 'm', 'mj', 'ml' ,'mr', 'n', 'nj', 'nl', 'nr', 'p', 'pch', 'pf', 'ph', 'pj', 'pk', 'pl', 'pn', 'pqu', 'pr', 'ps', 'pw',
    'qu', 'r', 'rh', 'rn', 's', 'sc', 'sch', 'sd', 'sg', 'sh', 'shm', 'shn', 'shp', 'shr', 'sht', 'shv', 'sj', 'sk', 'sl', 'sm', 'sn',
    'sp', 'sr', 'ss', 'st', 'sv', 'sw', 't', 'tf', 'th', 'thl', 'thn', 'thr', 'tl', 'tn', 'tr', 'ts', 'tsh', 'tv', 'tw', 'tz',
    'v', 'vj', 'vl', 'vn', 'vr', 'w', 'y', 'z', 'zd', 'zg', 'zm', 'zn', 'zr', 'zv', 'zw' )

vowels = ( 'a', 'e', 'i', 'o', 'u', 'ea', 'ai', 'au', 'ei', 'ie', 'oi', 'io', 'ou', 'eau', 'oe', 'ue', 'ee', 'oo' )

lc, lv = len( consonants ), len( vowels )

def sillyname( seed = None ):
    if not seed: return 4
    s, r = int. from_bytes( seed, 'little' ), ''
    s, c = divmod( s, lc )
    s, v = divmod( s, lv )
    r += consonants[ c ] + vowels[ v ]
    s, c = divmod( s, lc )
    s, v = divmod( s, lv )
    r += consonants[ c ] + vowels[ v ]
    s, c = divmod( s, lc )
    r += consonants[ c ]
    return { 'name': r, None: r }

def birthdate( seed = None ):
    if not seed: return 2
    s = int. from_bytes( seed, 'little' ) & 16383
    r = str( date( 1950, 1, 1 ) + timedelta( days = s ))
    return { 'date': r, None: r }
    
def main():
    '''cli utility'''
    def arg_err( msg ): raise ArgumentTypeError( msg )
    is_hex = lambda v: match( '^(?:[0-9a-fA-F][0-9a-fA-F])+$', v ) and v or arg_err( '%s is not a valid hexadecimal number' % v )
    is_positive = lambda v: match( '^0*[1-9]+[0-9]*$', v ) and int( v ) or arg_err( 'expecting a positive integer, got %s' % v )
    p = ArgumentParser( description = 'Stateless password manager and brain wallet' )
    p. add_argument( 'what', nargs = REMAINDER, choices = ( 'seed', 'password', 'address', 'key', 'spend', 'view', 'name', 'date' ), help = 'What information to return' )
    p. add_argument( '-w', action = 'append', nargs = '?', choices = COINS, help = 'Generate wallet (default: btc)' )
    p. add_argument( '-s', action = 'append', nargs = '?', type = is_positive, help = 'Generate raw seed only with given number of bytes (default: 16)' )
    p. add_argument( '-n', action = 'store_const', const = True, help = 'Generate a silly name' )
    p. add_argument( '-b', action = 'store_const', const = True, help = 'Generate a birth date' )
    p. add_argument( '-D', action = 'store', help = 'Description' )
    p. add_argument( '-M', action = 'store', help = 'Master password' )
    p. add_argument( '-S', action = 'store', type = is_hex, help = 'Use this seed instead of description/master' )
    p. add_argument( '-R', action = 'store_const', const = True, help = 'Use a random seed, don\'t ask for inputs' )
    p. add_argument( '-c', action = 'store_const', const = True, help = 'Input master password as clear text' )
    p. add_argument( '-d', action = 'store_const', const = True, help = 'Display result instead of copy to clipboard' )

    cli = p. parse_args()

    if 1 < sum( _ and 1 or 0 for _ in ( cli. w, cli. s, cli. n, cli. b )):
        p. error( '-w, -s, -n, -b options are mutually exclusive' )
    elif cli. S and cli. R:
        p. error( '-S, -R options are mutually exclusive' )
    elif ( cli. S or cli. R ) and ( cli. D or cli. M ):
        p. error( 'The -D/-M options are mutually exclusive with -S/-R' )

    action = btc if cli. w and cli. w[ -1 ] is None else globals()[ cli. w[ -1 ]] if cli. w else placebo if cli. s else sillyname if cli. n else birthdate if cli. b else password
    seed_len = 16 if cli. s and cli. s[ -1 ] is None else cli. s[ -1 ] if cli. s else action()

    if cli. R:
        seed = mk_seed( urandom( 32 ), urandom( 32 ), seed_len )
        result = action( seed )
    elif cli. S:
        seed = bytes. fromhex( cli. S )
        if len( seed ) != seed_len:
            p. error( 'Wrong seed length, expecting %s bytes' % seed_len )
        result = action( seed )
    else:
        try:
            description = bytes( input( 'Enter description: ' ), 'utf-8' ) if not cli. D else bytes( cli. D, 'utf-8' )
            if cli. M:
                master = bytes( cli. M, 'utf-8' )
            elif cli. c:
                master = bytes( input( 'Enter password: ' ), 'utf-8' )
            else:
                master = bytes( getpass( 'Enter password: ' ), 'utf-8' )
                master0 = bytes( getpass( 'Enter password: ' ), 'utf-8' )
                if master != master0:
                    print( 'ERROR: Password mismatch' )
                    exit( 1 )
        except ( EOFError, KeyboardInterrupt ):
            exit( 0 )
        seed = mk_seed( description, master, seed_len )
        result = action( seed )

    result[ 'seed' ] = hexlify( seed ). decode( 'latin_1' )

    if not cli. what:
        output = result[ None ]
    else:
        try:
            output = ' '. join( result[ what ] for what in cli. what )
        except KeyError as e:
            p. error( 'Unexpected output specifier %s' % e )

    if cli. d:
        print( output )
    else:
        pyperclip_copy( output )
        print( 'Result placed in clipboard.' )

