"""
Configuration variables, collected here for easy tweaking.

Also contains a logger for use throughout the app.
"""

import logging

import blackmango.sprites

from blackmango.configure import *

EDITOR_VERSION = '0.0.0a'

# Smaller grid just to keep the window similarly sized on my netbook
GRID_SIZE -= 5
# Display the blocks just offscreen in the editor
SCREEN_SIZE = (GRID_SIZE * 21, GRID_SIZE * 13)
blackmango.sprites.TRANSLATION_OFFSET = 1

MAIN_WINDOW_TITLE = 'MANGOED'

DEBUG = logging.ERROR

logger = None

def setup_logger(lvl = DEBUG):
    global logger
    # Set up console logging
    logging.basicConfig()
    logger = logging.getLogger('mangoed')
    logger.setLevel(DEBUG)