"""
Black Mango is a puzzle game.

(c) 2014 Chicken Mover.
All rights reserved.
"""

import argparse

import blackmango.app
import blackmango.configure
import blackmango.gameengine
import blackmango.materials
import blackmango.mobs
import blackmango.ui

ARGUMENTS = (
    ('--data-dir', {
        'dest': 'data_dir',
        'help': 'On Linux and non-Mac OS POSIX systems, this specifies the '
                'directory into which application data and saved games are '
                'placed. The default value is ~/.blackmango.',
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
        blackmango.configure.DATA_DIR = args.data_dir

    blackmango.configure.setup_logger(blackmango.configure.DEBUG)

    engine = blackmango.gameengine.GameEngine()
    main_window = blackmango.ui.GameWindow(engine)

    for f in [
        blackmango.materials.materials_batch.draw,
        blackmango.mobs.mobs_batch.draw,
    ]:
        engine.register_draw(f)

    blackmangoapp = blackmango.app.BlackMangoApp()
    blackmangoapp.schedule(main_window.tick)

    blackmangoapp.run()