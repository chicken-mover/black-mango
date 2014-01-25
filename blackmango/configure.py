"""
Configuration variables, collected here for easy tweaking.

Also contains a logger for use throughout the app.
"""

import logging
import pyglet

VERSION = '0.0.0a'

MAIN_WINDOW_TITLE = 'BLACK MANGO'

DEBUG = 0 #logging.WARN
FULLSCREEN = False
# Main game window size.
# TODO: Set this appropriately dynamically
SCREEN_SIZE = (950, 550)

SAVE_GAME_VERSION='BLACKMANGO-001'

# Default POSIX data dir (except Mac OS)
POSIX_DATA_DIR = '~/.blackmango'

# Grid size. Used for translating world coordinates into screen coordinates.
GRID_SIZE = 50

# Batch rendering groups.
ORDERED_GROUPS = {
    'mobs': pyglet.graphics.OrderedGroup(5),
    'background': pyglet.graphics.OrderedGroup(0),
    'foreground': pyglet.graphics.OrderedGroup(1),
}

# number of frames when animating movement slides. potentially will be used for
# sprite animations, too.
BASE_ANIMATION_FRAMES = 10

# Loaded by assetloader.load_colordata()
COLORS = {}

logger = None

def setup_logger(lvl = DEBUG):
    global logger
    # Set up console logging
    logging.basicConfig()
    logger = logging.getLogger('blackmango')
    logger.setLevel(DEBUG)
