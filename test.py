# The following tests verify resulting enumerations against pre-computed results.
# The main purpose of these tests is to make sure that changes in code don't break
# the consistency of results.

from unittest import main, TestCase

from novault import *

tests = (
    ((password,b'',b''), {None: '+*I:rq8`yAfB&20zr#z!aI9<', 'password': '+*I:rq8`yAfB&20zr#z!aI9<'}),
    ((sillyname,b'',b''), {None: 'kleauthloesn', 'name': 'kleauthloesn'}),
    ((birthdate,b'',b''), {None: '1964-08-15', 'date': '1964-08-15'}),
    ((btc,b'',b''), {None: '1BhUSjFE7rbVdSUUtZSXU8F1W77iK4JCJH', 'key': 'L4c1Mh8DD8wMqkPXcPnNcfQgJMqNZEHrKJSAKqiu46sgtEnFAjMk', 'address': '1BhUSjFE7rbVdSUUtZSXU8F1W77iK4JCJH'}),
    ((xmr,b'',b''), {None: '43scM1Vz5YAfgB4Fscw4YY3eT3ksUqHBuagRw6C8GQ3eEDBqnYTKvbMjSNE8wEQwegGwoVfrV7Z8fQy6WAuuhaXp89WmJsQ', 'view': '72e79dadc72c59ba228d9338c9e9ab352b1ec619a2620f097bf88a3994b3930d', 'address': '43scM1Vz5YAfgB4Fscw4YY3eT3ksUqHBuagRw6C8GQ3eEDBqnYTKvbMjSNE8wEQwegGwoVfrV7Z8fQy6WAuuhaXp89WmJsQ', 'spend': 'f9e984a48f095d463e3d856fb57088a1cc08e7b01882b5127acd46e67786ad00'}),
    ((password,b'test?',b'test!'), {None: 'U}Ed`+Q9nsE3&^m=xPuV,1sA', 'password': 'U}Ed`+Q9nsE3&^m=xPuV,1sA'}),
    ((sillyname,b'test?',b'test!'), {None: 'pfiepleautn', 'name': 'pfiepleautn'}),
    ((birthdate,b'test?',b'test!'), {None: '1976-03-13', 'date': '1976-03-13'}),
    ((btc,b'test?',b'test!'), {None: '1LRJPAYBwrwe1yJsysH6hH1WAFjJomfCMX', 'key': 'KzT6TAwTZeZqBegBy19KjSnck47upqSRq4WJx9H4dC1jUqYQbg2A', 'address': '1LRJPAYBwrwe1yJsysH6hH1WAFjJomfCMX'}),
    ((xmr,b'test?',b'test!'), {None: '47nP8an1dZrWhG9E4E9hcsTzUAFkDfGPJeJANYryEAXx7dtCEpTnt4JG1uLfFRFW2JWaEqTWzaDGzUpPUnjxBfdyNAXAbT6', 'view': '2cc991b8645b464f30fbf1f6939c61ba214f7821f9d9b54d9b46fe07a3fe8600', 'address': '47nP8an1dZrWhG9E4E9hcsTzUAFkDfGPJeJANYryEAXx7dtCEpTnt4JG1uLfFRFW2JWaEqTWzaDGzUpPUnjxBfdyNAXAbT6', 'spend': 'e59902909889c8cb2e7eeb50a2aef72ad0b4a3bce6ca57627a6e5b4009a6380c'}),
    ((password,b'\xe4\xbd\xa0\xe5\xa5\xbd',b'\xe4\xb8\x96\xe7\x95\x8c'), {None: 'Zf}Us1CU^Y.oyb#gFC;-M6)n', 'password': 'Zf}Us1CU^Y.oyb#gFC;-M6)n'}),
    ((sillyname,b'\xe4\xbd\xa0\xe5\xa5\xbd',b'\xe4\xb8\x96\xe7\x95\x8c'), {None: 'sveeskuemj', 'name': 'sveeskuemj'}),
    ((birthdate,b'\xe4\xbd\xa0\xe5\xa5\xbd',b'\xe4\xb8\x96\xe7\x95\x8c'), {None: '1983-03-31', 'date': '1983-03-31'}),
    ((btc,b'\xe4\xbd\xa0\xe5\xa5\xbd',b'\xe4\xb8\x96\xe7\x95\x8c'), {None: '1GSX8U7w5QaGMhiMjR1MxuCApM3PJP4Aid', 'key': 'KzvPC4Sg9LVETUektM3csvdeNfoLe58u74y5pSdFMm9W2rJKXPmG', 'address': '1GSX8U7w5QaGMhiMjR1MxuCApM3PJP4Aid'}),
    ((xmr,b'\xe4\xbd\xa0\xe5\xa5\xbd',b'\xe4\xb8\x96\xe7\x95\x8c'), {None: '49abobZyzdcC8QziTjZM8zU8FBwY3ef8P1NVu91bp6uGWniEBy1NTZREe5ysZjPATR8LW9bDefWbwcCfqifzTkQvQZaQvQE', 'view': '4b947d23605ec362f331d1276ea99c52cb82917c5ae91e750e1507a53878e203', 'address': '49abobZyzdcC8QziTjZM8zU8FBwY3ef8P1NVu91bp6uGWniEBy1NTZREe5ysZjPATR8LW9bDefWbwcCfqifzTkQvQZaQvQE', 'spend': 'f3a3cf444bdf1b4999286bd4cbcc109c23c601c4ba12d71679c23c02032e1d0d'}),
)

NAME = 'Test_novault'

def mk_test( t, r ):
    setattr( globals()[ NAME ], 'test_%s' % count, lambda self: self. assertEqual( novault( *t ), r ))

if __name__ == '__main__':
    globals()[ NAME ], count = type( NAME, ( TestCase, ), {} ), 0
    for t, r in tests:
        mk_test( t,r )
        count += 1
    main()

#
# Results file can be generated using the following code:
#
# with open( 'tests.txt', 'w' ) as f:
#     for t, r in tests:
#         f.write( '((' + t[ 0 ]. __name__ + ',' + str( t[ 1 ]) + ',' + str( t[ 2 ]) + '), ' + str( novault( *t )) + '),\n' )
