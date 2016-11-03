#######
novault
#######

-------------------------------------------
Stateless Password Manager and Brain Wallet
-------------------------------------------

.. contents::

Overview
********

What is novault
===============

``novault`` is a command-line utility and Python module for generating passwords and cryptocurrency wallets from a combination of a description and a master password. The description and master password are hashed, generating a pseudo-random seed which is then formatted as a password or wallet keys/address. By selecting a strong password as the master password it becomes practicaly impossible for an attacker who obtains one of your generated passwords or wallet keys to recover the master password, and recreate any of your other ``novault``-generated passwords or wallets. ``novault`` provides in addition some convenience features for generating pseudo-random `silly names`_ and `birth dates`_.

From a functionality point of view ``novault`` is very similar to a password manager or an electronic wallet, except that it doesn't save your passwords and wallets in a file. It actually doesn't store them anywhere - your brain is the database. You can re-create your passwords and wallets on the fly on fresh machines without any synching of a repository, by providing the description and master password.

The currencies currently supported by ``novault`` are `Bitcoin
<https://en.wikipedia.org/wiki/Bitcoin>`_ (BTC) and `Monero
<https://en.wikipedia.org/wiki/Monero_(cryptocurrency)>`_ (XMR).

``novault`` is available as a Python module for Linux, Windows, and OSX. Linux and Windows users can download a single binary (.exe file) which contains the entire functionality. In addition, ``novault`` exposes an API which can be used by developers to embed the ``novault`` functionality in other programs.

Announcements are available via the ``novault`` Twitter feed `@_novault
<https://twitter.com/_novault>`_.
Questions, suggestions, opinions and other stuff at `/r/novault
<https://www.reddit.com/r/novault>`_.

When to Use novault
===================

I wrote ``novault`` because this is my preferred way of generally managing my passwords and wallets. With multi-device computing I simply find it more conveniet to be able to access my passwords and wallets on any machine without having to sync a repository. This becomes particularly important when working with cryptocurrencies: The secure way to work with these currencies is to perform offline all processes that require the use of a private key; without ``novault`` I'd have to sync the list of wallets between the offline and online machines using a USB device, and that's both a nuisance and a potential source of security vulnerabilities.

In some cases the use of ``novault`` is not only simpler but also more secure than a repository-based password manager or wallet. Access to these too requires a master password, but if you are coerced to disclose the master password your entire list of assets in the repository is revealed to the attackers. With ``novault`` after a coerced disclosure of the master password the attackers can try to regenerate assets that they already know about (they still do have to get the precise description to match with the master password), yet you have `plausible deniability
<https://en.wikipedia.org/wiki/Plausible_deniability>`_ of the existance of any other assets.

An additional dimension of plausible deniabilty can be achieved with ``novault`` through master password federation, i.e., by using several master passwords for different purposes. When forced to disclose a master password you hedge your exposure only to those assets that use the password you disclosed, while being able to deny having any additional master passwords. With repository based solutions this usually won't be possible because typically the attackers will see that you have multiple repositories, and will force you to disclose all your master passwords.

Installation
************

Pre-Built Executables
=====================

`Download
<https://github.com/novault/novault/releases>`_ the binary file relevant to your machine.

Rename the downloaded file from ``novault-version-osname-hardware`` to ``novault.exe`` (on Windows) or ``novault`` (all other operating systems).

You can copy the executable to a USB drive and run it directly from there, or from any other directory, without any installation.

As a Python Module
==================

This method enables you to use ``novault`` on any Python-supported Linux, Windows, or OSX platform even if a pre-built executable is not available for it. It also enables you to use the ``novault`` API. Install the ``novault`` module using ``pip``::

	$ pip install novault

To run ``novault`` as a CLI utility::

    $ python -m novault <...cli options & arguments...>

Requires Python 3.4.

Under Linux ``novault`` requires either ``xsel`` or ``xclip`` in order to place the results in the clipboard; typically, at least one of them comes with the Linux distribution. If not then ``novault`` may try to fallback to ``PyQt4`` or ``gtk`` (this is a `pyperclip
<https://github.com/asweigart/pyperclip>`_ feature), however this fallback is not tested for ``novault``. So, if you have neither ``xsel`` nor ``xclip`` usually you can install either with a package manager,.e.g. ``sudo apt-get install xclip``. To install ``xsel`` from source::

    $ wget http://www.vergenet.net/~conrad/software/xsel/download/xsel-1.2.0.tar.gz
    $ tar -xf xsel-1.2.0.tar.gz
    $ cd xsel-1.2.0
    $ ./configure
    $ make
    $ sudo make install

Build Your Own Executable
=========================

This is usefull if you want an executable for an architecture for which pre-built binary executables are not available yet.

`Download
<https://github.com/novault/novault/releases>`_ the source package, unzip it, and move into the source directory. Install all dependencies::

    $ python setup.py install

Install `PyInstaller
<http://www.pyinstaller.org>`_ and build the executable::

    $ pip install pyinstaller
    $ pyinstaller novault.spec

The executable will be in the ``dist/`` directory, check that it works correctly.

How to Use novault
******************

Basic Usage
===========

``novault`` is a command line utility. When invoked it will ask for a description and password, and place the result in the clipboard. For example, the password of an email account could be generated as follows::

	$ novault
	Enter description: myemailaddress@somemail.com
	Enter password:
	Verify password:
	Result placed in clipboard.

You will now be able to paste the result from the clipboard into the relevant application or web page. The generated password's entropy is 128 bits, has 24 characters, and is guaranteed to have at least one digit, lowercase letter, uppercase letter, and "special" character.

In the rest of this document we will use two ``novault`` options to make the examples more readable: With the ``-c`` option ``novault`` will accept the password in clear text, echo it, and won't ask for verification; With the ``-d`` option the result will be displayed rather than placed in the clipboard. The above example will then look like this::

	$ novault -cd
	Enter description: myemailaddress@somemail.com
	Enter password: %^mY-ma5T3r-PAsSw0rd~~)!'
	F*XFim:E3ifG#F;c2#CCEwFZ

It is highly recommended **not** to use the ``-c`` and ``-d`` options unless you are sure you're in complete privacy from prying eyes and cameras.

.. Note::
	The password in our example is "meaningful" for the sake of readbility. In practice you should use a truly random password.

.. Attention::
	Use a description that you will be able to precicesly reproduce, including spelling alternatives, upper/lower case, accents, spaces, punctuation, etc. ANY change in the description will produce a different result.

Wallets
=======

To produce a wallet invoke ``novault`` with the ``-w`` option. The ``-w`` option accepts as argument the currency for which to produce a wallet, and by default will generate the wallet's address. if the currency is ommited then the wallet defaults to a Bitcoin wallet. Here are two examples::

    $ novault -cd -w btc
    Enter description: my shop
    Enter password: %^mY-ma5T3r-PAsSw0rd~~)!'
    13qmztfEvTQLNPcQWuxNJeaQHseW57seYi

    $ novault -cd -w xmr
    Enter description: my shop
    Enter password: %^mY-ma5T3r-PAsSw0rd~~)!'
    42rMGPw2Mt6CBWC5wWdPE6hnj1rFoz9kUALvw26ynNTKRwEYjStpVBzdGKpi79X2QdXeh1TRcFKgEKVMe7xPpFKAKc4N44B

At some point you will likely need the private keys of the wallet. ``novalut`` allows you to specify in the command line which information to generate about the wallet and at what order. For Bitcoin you can specify ``address`` and ``key`` and for Monero you can specify ``address``, ``spend``, and ``view``. Here are the above two examples, this time showing the private keys followed by the address::

    $ novault -cd -w btc key address
    Enter description: my shop
    Enter password: %^mY-ma5T3r-PAsSw0rd~~)!'
    L3ZpKbwm1NNHQcMrtfBZYCEnBjLR7FCQAU759v9YREtBog4HMVM3 13qmztfEvTQLNPcQWuxNJeaQHseW57seYi

    $ novault -cd -w xmr spend view address
    Enter description: my shop
    Enter password: %^mY-ma5T3r-PAsSw0rd~~)!'
    2f6756de5442aa82e0755b93dfcdca7380cdf52995d20740c6b589ba37ddaf06 5d3528c622b60aec74e97b34f8f08fb47de083cb81247086813afaaf1444740d 42rMGPw2Mt6CBWC5wWdPE6hnj1rFoz9kUALvw26ynNTKRwEYjStpVBzdGKpi79X2QdXeh1TRcFKgEKVMe7xPpFKAKc4N44B

Silly Names
===========

Web sites often have a practice of requiring users to provide answers to "security" questions, such as your place of birth and mother's maiden name. If you provide these web sites with your true answers these answers become practically public, often available to thousands of web site employees and subcontractors, and therefore breach your privacy and security. With ``novault``'s ``-n`` option you can generate unique silly names to use as answers to these questions. The silly names are kinda pronouncible, just in case you need to communicate them by voice, e.g. when speaking with a customer service representative. For example::

	$ novault -cd -n
	Enter description: first pet myaccount @big-retailer.com
	Enter password: %^mY-ma5T3r-PAsSw0rd~~)!'
	scuvrisj

	$ novault -cd -n
	Enter description: mother maiden name myaccount @big-retailer.com
	Enter password: %^mY-ma5T3r-PAsSw0rd~~)!'
	zwuezoih

.. Attention::
	NEVER use silly names as passwords, they are not secure enough for use as passwords.

.. _`birth dates`:

Birth Date Generator
====================

Web sites often ask you for your date of birth under the pretence of "security". However, giving away your real birth date compromises your privacy and security, and should be avoided except when there is no other choice (e.g., when dealing with regulated financial institutions). With ``novaults``'s ``-b`` option you can generate in a reproducible way a different date of birth for each web site or service::

	$ novault -cd -b
	Enter description: myaccount @big-retailer.com
	Enter password: %^mY-ma5T3r-PAsSw0rd~~)!'
	1982-01-16

The generated date will be in the range between `1950-01-01
<https://en.wikipedia.org/wiki/Before_Present>`_ and 1994-11-09.

Non-Interactive Use
===================

Sometimes you may need to use ``novault`` non-interactively, e.g., when invoked from a shell script. In such case you can use the ``-D`` option to provide the description and the ``-M`` option to provide the master password. For example, get the password of an email account::

	$ novault -d -D myemailaddress@somemail.com -M "%^mY-ma5T3r-PAsSw0rd~~)!'"
	F*XFim:E3ifG#F;c2#CCEwFZ

Another example, get the spend key of a Monero wallet::

	$ novault -dw xmr -D "online store mysite.com" -M "%^mY-ma5T3r-PAsSw0rd~~)!'" spend
	52c57a01a0fc1ba2d358362a61ee7c15ad2d78e89fb6ba9f6f5e0f04fa9acb08

The Seed (advanced topic)
=========================

All the values generated by ``novault`` are representations of a pseudo-random seed that results from the hashing of the description and master password. Sometimes it may be useful for you to get not just the final result but also the seed, for example in case there is another representation you want to derive from it. Adding the seed to the result is possible by adding the ``seed`` argument to the command line. Here are three examples that use the same description and master password to generate different representations with their seed::

    $ novault -cd seed password
    Enter description: test
    Enter password: %^mY-ma5T3r-PAsSw0rd~~)!'
    bb5bfa6140933377ded52b93c73f573e yIcBUK$A0ef-qO.kCU6$3Is-
    
    $ novault -cdw btc seed address
    Enter description: test
    Enter password: %^mY-ma5T3r-PAsSw0rd~~)!'
    bb5bfa6140933377ded52b93c73f573ec26fe973c5d8c4fc8fc54eaec144369e 156KN9GoSZmXvZVNQFdbZ88d8GwSiYRz5w

    $ novault -cdw xmr seed address
    Enter description: test
    Enter password: %^mY-ma5T3r-PAsSw0rd~~)!'
    bb5bfa6140933377ded52b93c73f573ec26fe973c5d8c4fc8fc54eaec144369e 44cstf51YYJEuR1v9MRZAXam7XYA8wRdCSFbJNDtoEG16TuULaerSXoXx2JGex9Hbd6fcaLn9qVkL2Xw7PpN6jAR9kVKmZP

As you can see all three examples produce the same seed (except that the password seed is just 128 bit versus the wallets' 256 bits). If you want to generate just a seed then you can use the ``-s`` option and provide it with the number of *bytes* to produce (defaults to 16)::

    $ novault -cd -s 32
    Enter description: test
    Enter password: %^mY-ma5T3r-PAsSw0rd~~)!'
    bb5bfa6140933377ded52b93c73f573ec26fe973c5d8c4fc8fc54eaec144369e

Once having a seed, this seed can be used to generate results without providing a description and master password. To provide a specific seed to ``novault`` use the ``-S`` option::

    $ novault -cd -S bb5bfa6140933377ded52b93c73f573e
    yIcBUK$A0ef-qO.kCU6$3Is-

``novault`` can also generate a random seed for you by specifying the ``-R`` option. The random seed is actually a random value generated by the operating system with an additional randomiztion layer in the form of ``novault``'s hashing::

    $ novault -cd -R -s 32
    de6b0a8e7f0c317b1dc00fd919e854cf32a1d3851b5667029ee8090439a00356

The ``-R`` option is also usefull in case you want to produce a random password, just note that this password cannot be reproduced unless you somehow back it up::

    $ novault -cd -R
    zm!sf6tX!TaN;3Zd(~4+,pZa

CLI Reference
*************

::

    usage: novault [-h] [-w [{btc,xmr}]] [-s [S]] [-n] [-b] [-D D] [-M M] [-S S] [-R] [-c] [-d]
                   ...

    Stateless password manager and brain wallet

    positional arguments:
      {seed,password,address,key,spend,view,name,date}
                            What information to return

    optional arguments:
      -h, --help            show this help message and exit
      -w [{btc,xmr}]        Generate wallet (default: btc)
      -s [S]                Generate raw seed only with given number of bytes (default: 16)
      -n                    Generate a silly name
      -b                    Generate a birth date
      -D D                  Description
      -M M                  Master password
      -S S                  Use this seed instead of description/master
      -R                    Use a random seed, don't ask for inputs
      -c                    Input master password as clear text
      -d                    Display result instead of copy to clipboard

API
***

To access ``novault``'s functionality programatically install the module (e.g. using ``pip`` as described in the Installation_ chapter) and include an ``import novault`` statement in your code.

``novault`` exports one constant, ``novault.COINS`` with the list of coins it supports::

    >>> import novault
    >>> novault.COINS
    ('btc', 'xmr')

The ``novault`` module exports the following functions.

novault.novault
===============

A general wrapper of all actions. An action is a function that accepts a seed and returns a representation; if the seed is not provided the function returns the number of bytes that should be in seeds accepted by the action. An action reurns a dictionary with all values it generated, where the key ``None`` points to the value that should be displayed by default.

**novault.novault( action, description, master )**

*action* - ``novault.password``, ``novault.btc``, ``novault.xmr``, ``novault.sillyname`` or ``novault.birthdate``.

*description* - The description to use in generating the seed.

*master* - The master password to use in generating the seed.

Returns the result returned by the action.

**Example**::

    >>> novault.novault( novault.password, b'test', b'mypassword' )
    {'password': 'bHY^GLsEu!Io3q#CWbA|zfO,', None: 'bHY^GLsEu!Io3q#CWbA|zfO,'}
    >>> novault.novault( novault.btc, b'test', b'mypassword' )
    {None: '1Lb4NGg4kJMm82qqoL7AdbahLZXF7YHG9z', 'address': '1Lb4NGg4kJMm82qqoL7AdbahLZXF7YHG9z', 'key': 'Ky31n6uHG6X5pkEeELK9DvsEwBBw7GYxYjNdSiAae3tNUYqsv5Ra'}

novault.mk_seed
===============

The seed generation function.

**novault.mk_seed( description, master, length )**

*description* - The description to use in generating the seed.

*master* - The master password to use in generating the seed.

*length* - The number of bytes to generate.

Returns the generated seed.

**Example**::

    >>> from binascii import hexlify
    >>> hexlify(novault.mk_seed( b'test', b'mypassword', 32 ))
    b'362c09fea88d6f6c9d8028d976265cc9324ac2795e12626b00c65729a5cd7325'

novault.password
================

Generates a password representation from a 16 byte seed.

**novault.password( seed = None )**

*seed* - The seed used for generating the password.

Returns a dictionary with the key ``password``.

**Example**::

    >>> from binascii import unhexlify
    >>> novault.password(unhexlify(b'362c09fea88d6f6c9d8028d976265cc9'))
    {'password': 'bHY^GLsEu!Io3q#CWbA|zfO,', None: 'bHY^GLsEu!Io3q#CWbA|zfO,'}

novault.btc
===========

Generates a Bitcoin wallet representation from a 32 byte seed.

**novault.btc( seed = None )**

*seed* - The seed used for generating the password.

Returns a dictionary with the keys ``address`` and ``key``.

**Example**::

    >>> novault.btc(unhexlify(b'362c09fea88d6f6c9d8028d976265cc9324ac2795e12626b00c65729a5cd7325'))
    {None: '1Lb4NGg4kJMm82qqoL7AdbahLZXF7YHG9z', 'address': '1Lb4NGg4kJMm82qqoL7AdbahLZXF7YHG9z', 'key': 'Ky31n6uHG6X5pkEeELK9DvsEwBBw7GYxYjNdSiAae3tNUYqsv5Ra'}

novault.xmr
===========

Generates a Monero wallet representation from a 32 byte seed.

**novault.xmr( seed = None )**

*seed* - The seed used for generating the password.

Returns a dictionary with the keys ``address``, ``spend`` and ``view``.

**Example**::

    >>> novault.xmr(unhexlify(b'362c09fea88d6f6c9d8028d976265cc9324ac2795e12626b00c65729a5cd7325'))
    {'view': 'b1c1f02b4782c57b00a918b9232c3f00850f2f204e02fed18c5f60ca7e50ee0a', None: '48SC75jKUDriiHiRsBW5bENxWef37T6yCRVrBNPrCy5JQ5epdHT2epkiJ3FeH4438BBa5C8juFNuLgcSpeRZX2hg4zCmrhD', 'address': '48SC75jKUDriiHiRsBW5bENxWef37T6yCRVrBNPrCy5JQ5epdHT2epkiJ3FeH4438BBa5C8juFNuLgcSpeRZX2hg4zCmrhD', 'spend': '5c841d4474c74abcf0463993b9329e9f324ac2795e12626b00c65729a5cd7305'}

novault.sillyname
=================

Generates a silly name representation from a 4 byte seed.

**novault.sillyname( seed = None )**

*seed* - The seed used for generating the silly name.

Returns a dictionary with the key ``name``.

**Example**::

    >>> novault.sillyname(unhexlify(b'362c09fe'))
    {None: 'sweaupjeethr', 'name': 'sweaupjeethr'}

novault.birthdate
=================

Generates a birth date representation from a 2 byte seed.

**novault.birthdate( seed = None )**

*seed* - The seed used for generating the birth date.

Returns a dictionary with the key ``date``.

**Example**::

    >>> novault.birthdate(unhexlify(b'362c'))
    {'date': '1980-12-27', None: '1980-12-27'}

Frequently Asked Questions
**************************

.. contents::
    :local:

There are other stateless password managers and brain wallets around, why develop yet another one?
=====================================================================================================

Each of the exisiting solutions that I could find had drawbacks that rendered them unsuitable for my needs, in particular:

- I won't use browser-based solutions as the browser cannot be trusted IMHO with the master password. Note that opening the Network monitor on the Developer Console of a web browser doesn't guarantee to display all the communication between the browser and the network, particularly if the tool being used is installed as an add-on. For example, a naive (?) bug such as sending form data to a search suggestions server would expose the master password to the entire internet without ever showing on the console.

- Many of the existing solutions use sub-par hashing techniques. Others' hashing is over-verbose and require e.g. entering a name. 

- Many of the existing solutions display their result in clear text. This is not acceptable in many environments where the user is susceptible to prying eyes and security cameras. Results should, by default, be placed in the clipboard.

- I find it more convenient to use a single manager for passwords and currecny wallets. After all, the logic is pretty similar, so why fuss with many different tools?

What is the difference between ``novault`` and HD wallets?
=====================================================================================================

HD wallets are similar to ``novault`` in the sense that a single tool can generate many wallets. However, HD - standing for Hierarchical Deterministic - means that all wallets are somehow related, typically in order to generate one-time addresses that can be easily recreated using a single seed. ``novault`` on the other hand can generate many addresses that are not neccessarilly related, each with its own description. ``novault`` can, however, be used to simulate HD hierarchies by using a description that contains a serial number. This is somewhat similar to Type 1 HD.

Can I use as master password a list of mnemonics?
=====================================================================================================

Yes, the master password is not checked against a maximum length and can contain the space character. The ``novault`` master password should be precise though, unlike some mnemonic implementations that allow mnemonics to be shortened to the first three characters.

Can I enter a description and/or master password in non-latin characters?
=====================================================================================================

Yes, you can use any characters in the description and master password. Take care though, when using non-Latin-1 characters, that the shell's code page settings can influence the representation of the string. The same *printed* string entered under different code pages can yield different *binary* strings. To avoid such problems you can either adhere to Latin-1 characters or make sure you always invoke ``novault`` with the same code page; since ``novault`` internally converts the strings to UTF-8 it is best advised to use a UTF-8 generating code page whenever using non-Latin-1 characters.

What hashing algorithm is used to derive the seed from the description and master password?
=====================================================================================================

``novault`` uses two rounds of `scrypt
<https://www.tarsnap.com/scrypt.html>`_. The first round uses two different-salted concatenations of the description and master password to generate a 256-bit value which will be used as the salt for the second round. The second round uses a key generated by a third salted concatenation of the description and master password and the salt generated in the first round. The result of the second round is used as the ``novault`` seed. The Python code is as follows::

    def mk_seed( description, master, length ):
        '''Generate pseudorandom seed of desired length from description & master password'''
        S0, S1, S2 = b'%<6>0Mk$ziGdz@:z-O-', b'Jea`_uH6.ji4R$VM1ZB', b'C!#1P4zJLB2O=no06[1'
        return pyscrypt_hash(
            description + S0 + master,
            pyscrypt_hash( description + S1 + master, master + S2 + description, 1024, 1, 1, 32 ),
            1024, 1, 1, length )

The calls to scrypt use a low difficulty in order to make the algorithm usable on weaker platforms such as mobile devices and SBCs.

Can you add support for additional currencies?
=====================================================================================================

Yes, post in `/r/novault
<https://www.reddit.com/r/novault>`_ or get in touch at `novault.dev@gmail.com
<mailto:novault.dev@gmail.com>`_.

Can you add pre-built executables for an additional platform?
=====================================================================================================

In order to generate an executable for a platform one must have such a machine (this is a `PyInstaller
<http://www.pyinstaller.org>`_ limitation), and for security reasons I don't accept binary contributions. Therefore the choice of available platforms depends on what I currently have. If you wish to buy me an additional platform then please post in `/r/novault
<https://www.reddit.com/r/novault>`_ or get in touch at `novault.dev@gmail.com
<mailto:novault.dev@gmail.com>`_.

License
*******

``novault`` is provided under the `MIT License
<https://github.com/novault/novault/blob/master/LICENSE>`_. Beyond Python and its standard libraries ``novault`` makes use and depends on the following 3rd party packages, and bundles them in the pre-built binary executables:

`ecdsa
<https://github.com/warner/python-ecdsa>`_, licensed under the MIT License.

`pyperclip
<https://github.com/asweigart/pyperclip>`_, licensed under the BSD License.

`pyscrypt
<https://github.com/ricmoo/pyscrypt>`_, licensed under the MIT License.

Contributing to novault
***********************

Please help make ``novault`` better by `reporting
<https://github.com/novault/novault/issues>`_ any bugs or other issues you encounter.

If you find ``novault`` usefull your donation will be most appreciated:

**btc** - ``1FE4CtY3qvxu3Yw1yWngTFKe7btXwaU2XZ``

**xmr** - ``44tLk21kgrQBMAuk41j8LURHxvo96sJfRhXR3ksJALwhrWs2YJK6uPCKbgwPpJcwefdKnZ766QeYbaDCmQ2rV7uBnVXRiz``

**PayPal** - press `here
<https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=novault.dev@gmail.com>`_

