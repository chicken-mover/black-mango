"""
A really fuckin' basic level editor for Black Mango
"""
# Fix PIL import if Pillow is installed instead. This *must* happen before
# Pyglet is imported
import sys
try:
    import Image
except ImportError:
    from PIL import Image
    sys.modules['Image'] = Image

import argparse
import sys

import blackmango.assetloader
import mangoed.app
import mangoed.configure

ARGUMENTS = (
    ('filepath', {
        'help': 'Filepath to load on startup and write to on completion.'
                ' Without a file specified, the program will just dump the '
                'final output to stdout when it exits.'
    }),)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=__doc__.strip())

    for name, argspec in ARGUMENTS:
        parser.add_argument(name, **argspec)

    args = parser.parse_args()

    mangoed.configure.setup_logger(mangoed.configure.DEBUG)
    logger = mangoed.configure.logger

    mangoed.ui.init()
    mangoed.app.init()

    blackmango.assetloader.load_fonts()
    mangoed.configure.COLORS = blackmango.assetloader.load_colordata()

    pyglet.clock.schedule(blackmango.ui.game_window.tick)

    mangoed.app.app.run()

    sys.exit(mangoed.app.app.returncode)

