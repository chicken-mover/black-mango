"""
:mod:`system` --- System-dependent global values
================================================

This module smooths over the differences between OSes and packaged environments
and provides values for system paths needed by the app.

"""

import os
import sys

import blackmango.configure

##
## Try to make sure that, no matter what OS we're on, we put data and saves
## game files in the correct place on the system.
##

# '_MEIPASS2' is the PyInstaller temp directory when using --onefile. It is
# nuked on shutdown, so don't rely on it having data from a previous run.
#
#: The path to the root directory from which the main Black Mango app is
#: running. In finalized builds, this may not be a real or permanent directory.
DIR_ENV = os.environ.get('_MEIPASS2') or \
        os.path.dirname(os.path.dirname(blackmango.__file__))
#: The root path to the :ref:`asset tree <asset-tree>`.
DIR_ASSETS = os.path.join(DIR_ENV, 'assets')

#: The app data directory for the current OS. The value of this is dependent on
#: the proper procedure for storing app data on the current system, and is set
#: dynamically on startup.
DIR_APPDATA = None
#: The saved games directory for the current OS. The value of this is dependent
#: on the proper procedure for storing app data on the current system, and is
#: set dynamically on startup.
DIR_SAVEDGAMES = None

# Python should deal with pathsep issues correctly. (test this)
_DIR_WIN_APPDATA = '%USERPROFILE%/Application Data/Black Mango'
_DIR_WIN_SAVEDGAMES = '%USERPROFILE%/Saved Games/Black Mango'

_win_expandfunc = os.path.expandvars

_DIR_MACOS_APPDATA = '~/Library/Application Support/Black Mango'
_DIR_MACOS_SAVEDGAMES = '~/Documents/Black Mango/Saved Games'

_DIR_POSIX_APPDATA = os.path.join(blackmango.configure.POSIX_DATA_DIR,
                        'appdata/')
_DIR_POSIX_SAVEDGAMES = os.path.join(blackmango.configure.POSIX_DATA_DIR,
                            'savedgames/')

_posix_expandfunc = os.path.expanduser

try:

    uname = os.uname()

    path_expansion = _posix_expandfunc

    if not 'Darwin' in uname:
        DIR_APPDATA = _DIR_POSIX_APPDATA
        DIR_SAVEDGAMES = _DIR_POSIX_SAVEDGAMES
    else:
        DIR_APPDATA = _DIR_MACOS_APPDATA
        DIR_SAVEDGAMES = _DIR_MACOS_SAVEDGAMES

except AttributeError:

    if sys.platform == 'win32':

        path_expansion = _win_expandfunc

        DIR_APPDATA = _DIR_WIN_APPDATA
        DIR_SAVEDGAMES = _DIR_WIN_SAVEDGAMES

    else:

        # We're on a more exotic system. Go with POSIX behaviour and hope for
        # the best.
        path_expansion = _posix_expandfunc

        DIR_APPDATA = _DIR_POSIX_APPDATA
        DIR_SAVEDGAMES = _DIR_POSIX_SAVEDGAMES

DIR_APPDATA = path_expansion(DIR_APPDATA)
DIR_SAVEDGAMES = path_expansion(DIR_SAVEDGAMES)
