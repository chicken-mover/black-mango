"""
This module performs the app startup sequence and launches the main app event
loop. It is also responsible for shutting the app down cleanly when the event
loop finally exits.

Command-line arguments
----------------------

.. code-block:: text

  -h, --help           show this help message and exit
  --data-dir DATA_DIR  On Linux and non-Darwin POSIX systems, this specifies
                       the directory into which application data and saved
                       games are placed. The default value is ~/.blackmango.
  --debug DEBUG        Specify the debug level to use for logging output. This
                       should match one of the log levels found in the built-
                       in `logging` module (0, 10, 20, 30, 40, 50)
  --fullscreen         Set full screen mode.
  --start START        Specify the level to start at.


Initialization order
--------------------

The following gives a rough outline of the order in which initialization
occurs:

1. Import :mod:`blackmango.preload` to fix potential import problems.
2. Load modules and set up command-line arguments.
3. Parse command line arguments and override values in
   :mod:`blackmango.configure` as necessary.
4. Run :func:`blackmango.app.init` and :func:`blackmango.ui.init` to set up the
   references to the app and UI objects that the whole program needs access to.
5. Set the starting view to :class:`blackmango.ui.views.main_menu.MainMenuView`.
6. Schedule :meth:`blackmango.ui.GameWindow.tick` with 
   :func:`pyglet.clock.schedule` and start the event loop with
   :meth:`blackmango.app.BlackMangoApp.run`

See also
--------

+ :class:`blackmango.app.BlackMangoApp` - The main app event loop.
+ :mod:`blackmango.ui` - The module which handles the user interface and
  collects input.
"""

# Perform preload tasks (things which must be executed first)
import blackmango.preload

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
    ('--start', {
        'dest': 'start',
        'help': 'Specify the level to start at.',
    }),
)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="""
    Black Mango, (c) 2014 Chicken Mover
    """.strip())

    for name, argspec in ARGUMENTS:
        parser.add_argument(name, **argspec)

    args = parser.parse_args()

    if args.debug:
        blackmango.configure.DEBUG = args.debug
    if args.data_dir:
        blackmango.configure.POSIX_DATA_DIR = args.data_dir
    if args.fullscreen:
        blackmango.configure.FULLSCREEN = True
    if args.start:
        blackmango.configure.STARTING_LEVEL = args.start

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
