#!/bin/bash

# You probably need to update only this link
ELECTRUM_IOP_GIT_URL=git://github.com/anfauglith/electrum-iop.git
BRANCH=master
NAME_ROOT=electrum-iop


# These settings probably don't need any change
export WINEPREFIX=/opt/wine64

PYHOME=c:/python27
PYTHON="wine $PYHOME/python.exe -OO -B"


# Let's begin!
cd `dirname $0`
set -e

cd tmp

if [ -d "electrum-iop-git" ]; then
    # GIT repository found, update it
    echo "Pull"
    cd electrum-iop-git
    git checkout master
    git pull
    cd ..
else
    # GIT repository not found, clone it
    echo "Clone"
    git clone -b $BRANCH $ELECTRUM_IOP_GIT_URL electrum-iop-git
fi

cd electrum-iop-git
VERSION=`git describe --tags`
echo "Last commit: $VERSION"

cd ..

rm -rf $WINEPREFIX/drive_c/electrum-iop
cp -r electrum-iop-git $WINEPREFIX/drive_c/electrum-iop
cp electrum-iop-git/LICENCE .

# add python packages (built with make_packages)
cp -r ../../../packages $WINEPREFIX/drive_c/electrum-iop/

# add locale dir
cp -r ../../../lib/locale $WINEPREFIX/drive_c/electrum-iop/lib/

# Build Qt resources
wine $WINEPREFIX/drive_c/Python27/Lib/site-packages/PyQt4/pyrcc4.exe C:/electrum-iop/icons.qrc -o C:/electrum-iop/lib/icons_rc.py
wine $WINEPREFIX/drive_c/Python27/Lib/site-packages/PyQt4/pyrcc4.exe C:/electrum-iop/icons.qrc -o C:/electrum-iop/gui/qt/icons_rc.py

cd ..

rm -rf dist/

# build standalone version
$PYTHON "C:/pyinstaller/pyinstaller.py" --noconfirm --ascii --name $NAME_ROOT-$VERSION.exe -w deterministic.spec

# build NSIS installer
# $VERSION could be passed to the electrum-iop.nsi script, but this would require some rewriting in the script iself.
wine "$WINEPREFIX/drive_c/Program Files (x86)/NSIS/makensis.exe" /DPRODUCT_VERSION=$VERSION electrum-iop.nsi

cd dist
mv electrum-iop-setup.exe $NAME_ROOT-$VERSION-setup.exe
cd ..

# build portable version
cp portable.patch $WINEPREFIX/drive_c/electrum-iop
pushd $WINEPREFIX/drive_c/electrum-iop
patch < portable.patch 
popd
$PYTHON "C:/pyinstaller/pyinstaller.py" --noconfirm --ascii --name $NAME_ROOT-$VERSION-portable.exe -w deterministic.spec

echo "Done."
