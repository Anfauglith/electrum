#!/bin/bash

# You probably need to update only this link
FERMATUM_GIT_URL=git://github.com/anfauglith/fermatum.git
BRANCH=master
NAME_ROOT=fermatum


# These settings probably don't need any change
export WINEPREFIX=/opt/wine64

PYHOME=c:/python27
PYTHON="wine $PYHOME/python.exe -OO -B"


# Let's begin!
cd `dirname $0`
set -e

cd tmp

if [ -d "fermatum-git" ]; then
    # GIT repository found, update it
    echo "Pull"
    cd fermatum-git
    git checkout master
    git pull
    cd ..
else
    # GIT repository not found, clone it
    echo "Clone"
    git clone -b $BRANCH $FERMATUM_GIT_URL fermatum-git
fi

cd fermatum-git
VERSION=`git describe --tags`
echo "Last commit: $VERSION"

cd ..

rm -rf $WINEPREFIX/drive_c/fermatum
cp -r fermatum-git $WINEPREFIX/drive_c/fermatum
cp fermatum-git/LICENCE .

# add python packages (built with make_packages)
cp -r ../../../packages $WINEPREFIX/drive_c/fermatum/

# add locale dir
cp -r ../../../lib/locale $WINEPREFIX/drive_c/fermatum/lib/

# Build Qt resources
wine $WINEPREFIX/drive_c/Python27/Lib/site-packages/PyQt4/pyrcc4.exe C:/fermatum/icons.qrc -o C:/fermatum/lib/icons_rc.py
wine $WINEPREFIX/drive_c/Python27/Lib/site-packages/PyQt4/pyrcc4.exe C:/fermatum/icons.qrc -o C:/fermatum/gui/qt/icons_rc.py

cd ..

rm -rf dist/

# build standalone version
$PYTHON "C:/pyinstaller/pyinstaller.py" --noconfirm --ascii --name $NAME_ROOT-$VERSION.exe -w deterministic.spec

# build NSIS installer
# $VERSION could be passed to the fermatum.nsi script, but this would require some rewriting in the script iself.
wine "$WINEPREFIX/drive_c/Program Files (x86)/NSIS/makensis.exe" /DPRODUCT_VERSION=$VERSION fermatum.nsi

cd dist
mv fermatum-setup.exe $NAME_ROOT-$VERSION-setup.exe
cd ..

# build portable version
cp portable.patch $WINEPREFIX/drive_c/fermatum
pushd $WINEPREFIX/drive_c/fermatum
patch < portable.patch 
popd
$PYTHON "C:/pyinstaller/pyinstaller.py" --noconfirm --ascii --name $NAME_ROOT-$VERSION-portable.exe -w deterministic.spec

echo "Done."
