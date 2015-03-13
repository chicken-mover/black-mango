"""
Importing this module adjusts the values of :data:`sys.modules` and
:data:`sys.path` to compensate for potential import issues in various
environments.

It should be the first import performed during initialization of the app, after
any :mod:`__future__` imports.
"""

import os
import sys

# Fix PIL import if Pillow is installed instead. This *must* happen before
# Pyglet is imported
try:
    import Image
except ImportError:
    from PIL import Image
    sys.modules['Image'] = Image

# To avoid certain annoyances with packaging, set the project directory on the
# import path in the development environment.
#
# _MEIPASS2 is set by PyInstaller in packaged environments.
if not os.environ.get('_MEIPASS2'):
    sys.path.insert(0, os.path.abspath('..'))