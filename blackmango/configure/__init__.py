
import logging

MAIN_WINDOW_TITLE = 'BLACK MANGO'

DEBUG = logging.DEBUG
FULLSCREEN = False
SCREEN_SIZE = (500, 500)

GRID_SIZE = 50

ORDERED_GROUPS = {
    'player': 10,
    'mobs': 5,
    'background': 0,
    'foreground': 1,
}

# Set up console logging
logging.basicConfig()
logger = logging.getLogger('blackmango')
logger.setLevel(DEBUG)
