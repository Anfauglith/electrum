#!/usr/bin/env python2

# python setup.py sdist --format=zip,gztar

from setuptools import setup
import os
import sys
import platform
import imp
import argparse

version = imp.load_source('version', 'lib/version.py')

if sys.version_info[:3] < (2, 7, 0):
    sys.exit("Error: Electrum-IOP requires Python version >= 2.7.0...")

data_files = []

if platform.system() in ['Linux', 'FreeBSD', 'DragonFly']:
    parser = argparse.ArgumentParser()
    parser.add_argument('--root=', dest='root_path', metavar='dir', default='/')
    opts, _ = parser.parse_known_args(sys.argv[1:])
    usr_share = os.path.join(sys.prefix, "share")
    if not os.access(opts.root_path + usr_share, os.W_OK) and \
       not os.access(opts.root_path, os.W_OK):
        if 'XDG_DATA_HOME' in os.environ.keys():
            usr_share = os.environ['XDG_DATA_HOME']
        else:
            usr_share = os.path.expanduser('~/.local/share')
    data_files += [
        (os.path.join(usr_share, 'applications/'), ['electrum-iop.desktop']),
        (os.path.join(usr_share, 'pixmaps/'), ['icons/electrum-iop.png'])
    ]

setup(
    name="Electrum-IOP",
    version=version.ELECTRUM_IOP_VERSION,
    install_requires=[
        'pyaes',
        'ecdsa>=0.9',
        'pbkdf2',
        'requests',
        'qrcode',
        'protobuf',
        'dnspython',
        'jsonrpclib',
        'PySocks>=1.6.6',
    ],
    packages=[
        'electrum-iop',
        'electrum-iop_gui',
        'electrum-iop_gui.qt',
        'electrum-iop_plugins',
        #'electrum-iop_plugins.audio_modem',
        #'electrum-iop_plugins.cosigner_pool',
        'electrum-iop_plugins.email_requests',
        #'electrum-iop_plugins.greenaddress_instant',
        'electrum-iop_plugins.hw_wallet',
        #'electrum-iop_plugins.keepkey',
        'electrum-iop_plugins.labels',
        #'electrum-iop_plugins.ledger',
        'electrum-iop_plugins.trezor',
        #'electrum-iop_plugins.digitalbitbox',
        #'electrum-iop_plugins.trustedcoin',
        'electrum-iop_plugins.virtualkeyboard',
    ],
    package_dir={
        'electrum-iop': 'lib',
        'electrum-iop_gui': 'gui',
        'electrum-iop_plugins': 'plugins',
    },
    package_data={
        'electrum-iop': [
            'currencies.json',
            'www/index.html',
            'wordlist/*.txt',
            'locale/*/LC_MESSAGES/electrum-iop.mo',
        ]
    },
    scripts=['electrum-iop'],
    data_files=data_files,
    description="Lightweight IoP Wallet",
    author="Thomas Voegtlin",
    author_email="thomasv@electrum.org",
    license="MIT Licence",
    url="https://electrum-iop.org",
    long_description="""Lightweight IoP Wallet"""
)
