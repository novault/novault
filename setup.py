from setuptools import setup
from novault import __version__

setup(
    name = 'novault',
    packages = [ 'novault' ],
    version = __version__,
    description = 'Stateless Password Manager and Brain Wallet',
    license = 'MIT',
    author = 'Avner Herskovits',
    author_email = 'avnr_ at outlook.com',
    url = 'https://github.com/avnr/novault',
    download_url = 'https://github.com/avnr/novault/tarball/' + __version__,
    install_requires=[
        'ecdsa >= 0.13',
        'pyperclip >= 1.5.27',
        'pyscrypt >= 1.6.2',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries',
        'Topic :: Security',
        'Topic :: Security :: Cryptography',
        'Topic :: Utilities',
    ],
)
