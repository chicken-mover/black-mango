"""
Configuration variables, collected here for easy tweaking.

Also contains a logger for use throughout the app.
"""

import logging

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

# Batch rendering groups. This is actually only of limited value, because
# if we want stuff to render on top of the player, everything has to be in one
# batch group (as of this writing, materials and mobs get their own groups).
ORDERED_GROUPS = {
    'player': 10,
    'mobs': 5,
    'background': 0,
    'foreground': 1,
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
