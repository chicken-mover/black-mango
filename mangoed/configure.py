"""
:mod:`mangoed.configure` --- Configuration and universal variables
==================================================================

This overrides and expands on the values present in :mod:`blackmango.configure`
for use in MangoEd. Only overriden values are described in the documentation
below.

"""

import logging

import blackmango.configure
import blackmango.sprites

from blackmango.configure import *

#: The editor version is not necessarily the same as the Black Mango version.
EDITOR_VERSION = '0.0.0a'

#: Grid size. MangoEd uses a slightly smaller grid size to fit more tiles on
#: the screen.
GRID_SIZE  = GRID_SIZE - 5

blackmango.configure.GRID_SIZE = GRID_SIZE

#: Screen size. MangoEd displays the blocks just offscreen in the editor.
SCREEN_SIZE = (GRID_SIZE * 21, GRID_SIZE * 13)
blackmango.sprites.TRANSLATION_OFFSET = 1
blackmango.configure.SCREEN_SIZE = SCREEN_SIZE

#: Pyglet window title.
MAIN_WINDOW_TITLE = 'MANGOED'

#: The default DEBUG value in MangoEd is higher than in Black Mango.
DEBUG = logging.ERROR

#: 
logger = None

def setup_logger(lvl = DEBUG):
    """
    Called by the main initialization sequence. Sets up a logger with the output
    level set to *lvl* (which should be relevant data value from
    :ref:`the logging module <python:levels>`). This also overrides
    :data:`blackmango.configure.logger` so that any Black Mango logging code
    called during the run of MangoEd uses the same logger.
    """
    global logger
    # Set up console logging
    logging.basicConfig()
    logger = logging.getLogger('mangoed')
    logger.setLevel(DEBUG)
    import blackmango.configure
    blackmango.configure.logger = logger
