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

# Grid size. Used for translating world coordinates into screen coordinates.
GRID_SIZE = 50

# Main game window size.
GX, GY = (19, 11)
SCREEN_SIZE = (GRID_SIZE * GX, GRID_SIZE * GY)

SAVE_GAME_VERSION='BLACKMANGO-001'

# Default POSIX data dir (except Mac OS)
POSIX_DATA_DIR = '~/.blackmango'

# Batch rendering groups.
ORDERED_GROUPS = {
    'background': pyglet.graphics.OrderedGroup(0),
    'mobs': pyglet.graphics.OrderedGroup(2),
    'foreground': pyglet.graphics.OrderedGroup(3),
}

HEIGHT_OFFSET = 7 # In pixels

# number of frames when animating movement slides. potentially will be used for
# sprite animations, too.
BASE_ANIMATION_FRAMES = 10 # Keep this a common factor of GRID_SIZE or you will

# Loaded by assetloader.load_colordata()
COLORS = {}

logger = None

def setup_logger(lvl = DEBUG):
    global logger
    # Set up console logging
    logging.basicConfig()
    logger = logging.getLogger('blackmango')
    logger.setLevel(DEBUG)

STARTING_LEVEL = 'test' #'puzzle_demo1'

LEVEL_TEMPLATE = """
from blackmango.levels.%(MODULE_NAME)s.triggers import LevelTriggers

SIZE = %(SIZE)s
NAME = %(NAME)s

TRIGGERS = LevelTriggers

# Everything below this line is automatically generated.

ROOMS = %(ROOMS)s
PLAYER_START = %(PLAYER_START)s
BLOCKS = %(BLOCKS)s
MOBS = %(MOBS)s
"""

TRIGGER_TEMPLATE = """
import blackmango.levels

class LevelTriggers(blackmango.levels.BasicLevelTriggers):
    pass
"""
