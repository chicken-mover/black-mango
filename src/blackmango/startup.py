"""
Sidestep certain import problems by keeping the startup logic out of the
central __init__.py file.
"""

import argparse

#import blackmango
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
    ('--test', {
        'dest': 'test',
        'help': 'Run the test suite instead of the normal app.',
        'action': 'store_true',
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

blackmango.engine = blackmango.gameengine.GameEngine()
blackmango.main_window = blackmango.ui.GameWindow(blackmango.engine)

for f in [
    blackmango.materials.materials_batch.draw,
    blackmango.mobs.mobs_batch.draw,
]:
    blackmango.engine.register_draw(f)

blackmango.blackmangoapp = blackmango.app.BlackMangoApp()
blackmango.blackmangoapp.schedule(blackmango.main_window.tick)

def start():
    blackmango.blackmangoapp.run()
