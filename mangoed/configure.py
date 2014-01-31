"""
Configuration variables, collected here for easy tweaking.

Also contains a logger for use throughout the app.
"""

import logging

from blackmango.configure import *

EDITOR_VERSION = '0.0.0a'

MAIN_WINDOW_TITLE = 'BLACK MANGO EDITOR'

DEBUG = logging.ERROR

logger = None

def setup_logger(lvl = DEBUG):
    global logger
    # Set up console logging
    logging.basicConfig()
    logger = logging.getLogger('mangoed')
    logger.setLevel(DEBUG)


LEVEL_TEMPLATE = """
SIZE = %(size_tuple)s
NAME = %(name_string)s

NEXT_LEVEL = %(next_level_string)s
PREV_LEVEL = %(prev_level_string)s

# Everything below this line is automatically generated.
# Generated %(generation_date_time)s
BACKGROUNDS = %(backgrounds_dict)s
PLAYER_START = %(player_start_tuple)s
BLOCKS = %(blocks_dict)s
MOBS = %(mobs_dict)s
"""