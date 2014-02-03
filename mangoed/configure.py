"""
Configuration variables, collected here for easy tweaking and overriding of
certain configuration options inherited from the main Black Mango app.

Also contains a logger for use throughout the app.
"""

import logging

import blackmango.configure
import blackmango.sprites

from blackmango.configure import *

EDITOR_VERSION = '0.0.0a'

# Smaller grid just to keep the window similarly sized on my netbook
GRID_SIZE -= 5
blackmango.configure.GRID_SIZE = GRID_SIZE
# Display the blocks just offscreen in the editor
SCREEN_SIZE = (GRID_SIZE * 21, GRID_SIZE * 13)
blackmango.sprites.TRANSLATION_OFFSET = 1
blackmango.configure.SCREEN_SIZE = SCREEN_SIZE

MAIN_WINDOW_TITLE = 'MANGOED'

DEBUG = logging.ERROR

logger = None

def setup_logger(lvl = DEBUG):
    global logger
    # Set up console logging
    logging.basicConfig()
    logger = logging.getLogger('mangoed')
    logger.setLevel(DEBUG)
    import blackmango.configure
    blackmango.configure.logger = logger
