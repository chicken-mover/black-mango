"""
Black Mango is a puzzle game.

(c) 2014 Chicken Mover
All rights reserved.
"""

import argparse

import blackmango.configure

ARGUMENTS = (
    ('--data-dir', {
        'dest': 'data_dir',
        'help': 'On Linux and non-Mac OS POSIX systems, this specifies the '
                'directory into which application data and saved games are '
                'placed. The default value is ~/.blackmango.',
    }),
    ('--debug', {
        'dest': 'debug_level',
        'help': 'Specify the debug level to use for logging output. This should'
                ' match one of the log levels found in the built-in `logging` '
                'module.',
        'type': int,
    }),
)

parser = argparse.ArgumentParser(description=__doc__.strip())

for name, argspec in ARGUMENTS:
    parser.add_arguments(name, **argspec)

args = parser.parse_args()

if args.debug:
    blackmango.configure.DEBUG = args.debug
if args.data_dir:
    blackmango.configure.DATA_DIR = args.data_dir

if __name__ == "__main__":
    
    import blackmango.app
    blackmango.app.app.run()
