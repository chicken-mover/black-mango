
import os
import sys

import blackmango.configure

##
## Try to make sure that, no matter what OS we're on, we put data and saves
## game files in the correct place on the system.
##

DIR_APPDATA = None
DIR_SAVEGAMES = None

# Python will deal with pathsep issues correctly.
_DIR_WIN_APPDATA = '%USERPROFILE%/Application Data/Black Mango'
_DIR_WIN_SAVEDGAMES = '%USERPROFILE%/Saved Games/Black Mango'

_win_expandfunc = os.path.expandvars

_DIR_MACOS_APPDATA = '~/Library/Application Support/Black Mango'
_DIR_MACOS_SAVEDGAMES = '~/Documents/Black Mango/Saved Games'

_DIR_POSIX_APPDATA = os.path.join(blackmango.configure.DATA_DIR, 'appdata/')
_DIR_POSIX_SAVEDGAMES = os.path.join(blackmango.configure.DATA_DIR, 'savedgames/')

_posix_expandfunc = os.path.expanduser

try:

    uname = os.uname()

    path_expansion = _posix_expandfunc

    if not 'Darwin' in uname:
        DIR_APPDATA = _DIR_POSIX_APPDATA
        DIR_SAVEGAMES = _DIR_POSIX_SAVEDGAMES
    else:
        DIR_APPDATA = _DIR_MACOS_APPDATA
        DIR_SAVEGAMES = _DIR_MACOS_SAVEDGAMES

except AttibuteError:
    
    if sys.platform == 'win32':

        path_expansion = _win_expandfunc

        DIR_APPDATA = '%USERPROFILE%/Application Data/Black Mango'
        DIR_APPDATA = os.path.expandvars(DIR_APPDATA)

    else:

        # We're on a more exotic system. Go with POSIX behaviour and hope for
        # the best.
        path_expansion = _posix_expandfunc

        DIR_APPDATA = _DIR_POSIX_APPDATA
        DIR_SAVEGAMES = _DIR_POSIX_SAVEDGAMES

DIR_APPDATA = path_expansion(DIR_APPDATA)
DIR_SAVEDGAMES = path_expansion(DIR_SAVEDGAMES)

