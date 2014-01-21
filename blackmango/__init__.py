"""
Black Mango is a puzzle game.

(c) 2014 Chicken Mover.
All rights reserved.
"""

import argparse
import os
import pyglet
import sys
import traceback

import blackmango.app
import blackmango.assetloader
import blackmango.configure
import blackmango.ui

ARGUMENTS = (
    ('--data-dir', {
        'dest': 'data_dir',
        'help': 'On Linux and non-Darwin POSIX systems, this specifies the '
                'directory into which application data and saved games are '
                'placed. The default value is %s.' % \
                    blackmango.configure.POSIX_DATA_DIR,
    }),
    ('--debug', {
        'dest': 'debug',
        'help': 'Specify the debug level to use for logging output. This should'
                ' match one of the log levels found in the built-in `logging` '
                'module (0, 10, 20, 30, 40, 50)',
        'type': int,
    }),
    ('--fullscreen', {
        'dest': 'fullscreen',
        'action': 'store_true',
        'help': 'Set full screen mode.',
    }),
)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=__doc__.strip())

    for name, argspec in ARGUMENTS:
        parser.add_argument(name, **argspec)

    args = parser.parse_args()

    if args.debug:
        blackmango.configure.DEBUG = args.debug
    if args.data_dir:
        blackmango.configure.POSIX_DATA_DIR = args.data_dir
    if args.fullscreen:
        blackmango.configure.FULLSCREEN = True

    blackmango.configure.setup_logger(blackmango.configure.DEBUG)
    logger = blackmango.configure.logger

    logger.debug("Initializing ui and app")
    blackmango.ui.init()
    blackmango.app.init()
    
    logger.debug("Loading fonts and colors")
    blackmango.assetloader.load_fonts()
    blackmango.configure.COLORS = blackmango.assetloader.load_colordata()

    logger.debug("Initializing starting view")
    from blackmango.ui.views.main_menu import MainMenuView
    blackmango.ui.game_window.set_view(MainMenuView())

    logger.debug("Scheduling tick handler")
    pyglet.clock.schedule(blackmango.ui.game_window.tick)

    try:
        logger.debug("Starting event loop")
        blackmango.app.game_app.run()
        logger.debug("Exited event loop")
    except Exception as e:
        logger.fatal("Exited event loop due to error")
        # TODO implement crash logs/reporting
        print >>sys.stderr, traceback.format_exc()
        sys.exit(os.EX_SOFTWARE)

    sys.exit(blackmango.app.game_app.returncode)
