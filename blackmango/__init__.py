"""
Black Mango is a puzzle game.

(c) 2014 Chicken Mover.
All rights reserved.
"""

import argparse

import blackmango.app
import blackmango.configure
import blackmango.engine
import blackmango.materials
import blackmango.mobs
import blackmango.ui
import blackmango.ui.labels

ARGUMENTS = (
    ('--data-dir', {
        'dest': 'data_dir',
        'help': 'On Linux and non-Darwin POSIX systems, this specifies the '
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
        blackmango.configure.POSIX_DATA_DIR = args.data_dir

    blackmango.configure.setup_logger(blackmango.configure.DEBUG)

    blackmango.engine.init()
    blackmango.ui.init()
    blackmango.app.init()

    for f in [
        blackmango.ui.lables.titles_batch.draw,
        blackmango.materials.materials_batch.draw,
        blackmango.mobs.mobs_batch.draw,
    ]:
        blackmango.engine.game_engine.register_draw(f)

    blackmango.app.game_app.schedule(blackmango.ui.game_window.tick)
    blackmango.app.game_app.run()