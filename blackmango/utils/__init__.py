
import os
import sys


APPDATA_DIRECTORY = None

try:
    uname = os.uname()

    if not 'Darwin' in uname:
        APPDATA_DIRECTORY = os.path.expanduser('~/.blackmango')
    else:
        APPDATA_DIRECTORY = os.path.expanduser(
            '~/Library/Application Support/Black Mango'
        )

except AttibuteError:
    
    if sys.platform == 'win32':

        APPDATA_DIRECTORY = '%USERPROFILE%/Application Data/Black Mango'
        APPDATA_DIRECTORY = os.path.expandvars(APPDATA_DIRECTORY)

    else:

        APPDATA_DIRECTORY = os.path.join(os.getcwd(), 'blackmango')

