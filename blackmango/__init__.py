"""
Black Mango is a puzzle game.

(c) 2014 Chicken Mover.
All rights reserved.
"""

import argparse
import os
import sys
import traceback

import blackmango.app
import blackmango.assetloader
import blackmango.configure
import blackmango.ui
import blackmango.ui.views.main_menu

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
                'module.',
        'type': int,
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

    blackmango.configure.setup_logger(blackmango.configure.DEBUG)

    blackmango.configure.logger.info("Initializing ui and app")
    blackmango.ui.init()
    blackmango.app.init()
    
    blackmango.configure.logger.info("Loading fonts")
    blackmango.assetloader.load_fonts()

    blackmango.configure.logger.info("Initializing starting view")
    starting_view = blackmango.ui.views.main_menu.MainMenu()
    blackmango.ui.game_window.set_view(starting_view)

    blackmango.configure.logger.info("Scheduling tick handler")
    blackmango.app.game_app.schedule(blackmango.ui.game_window.tick)

    try:
        blackmango.configure.logger.info("Starting event loop")
        blackmango.app.game_app.run()
        blackmango.configure.logger.info("Exited event loop")
    except Exception as e:
        blackmango.configure.logger.debug("Exited event loop due to error")
        # TODO implement crash logs/reporting
        print >>sys.stderr, traceback.format_exc()
        sys.exit(os.EX_SOFTWARE)

    sys.exit(blackmango.app.game_app.returncode)
