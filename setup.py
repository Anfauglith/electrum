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
    sys.exit("Error: Fermatum requires Python version >= 2.7.0...")

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
        (os.path.join(usr_share, 'applications/'), ['fermatum.desktop']),
        (os.path.join(usr_share, 'pixmaps/'), ['icons/fermatum.png'])
    ]

setup(
    name="Fermatum",
    version=version.FERMATUM_VERSION,
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
        'fermatum',
        'fermatum_gui',
        'fermatum_gui.qt',
        'fermatum_plugins',
        #'fermatum_plugins.audio_modem',
        #'fermatum_plugins.cosigner_pool',
        'fermatum_plugins.email_requests',
        #'fermatum_plugins.greenaddress_instant',
        'fermatum_plugins.hw_wallet',
        #'fermatum_plugins.keepkey',
        'fermatum_plugins.labels',
        #'fermatum_plugins.ledger',
        'fermatum_plugins.trezor',
        #'fermatum_plugins.digitalbitbox',
        #'fermatum_plugins.trustedcoin',
        'fermatum_plugins.virtualkeyboard',
    ],
    package_dir={
        'fermatum': 'lib',
        'fermatum_gui': 'gui',
        'fermatum_plugins': 'plugins',
    },
    package_data={
        'fermatum': [
            'currencies.json',
            'www/index.html',
            'wordlist/*.txt',
            'locale/*/LC_MESSAGES/fermatum.mo',
        ]
    },
    scripts=['fermatum'],
    data_files=data_files,
    description="Lightweight IoP Wallet",
    author="Thomas Voegtlin",
    author_email="thomasv@electrum.org",
    license="MIT Licence",
    url="https://fermatum.org",
    long_description="""Lightweight IoP Wallet"""
)
