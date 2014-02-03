"""
A really fuckin' basic level editor for Black Mango
"""

# Perform preload tasks (things which must be executed first)
import blackmango.preload

import argparse
import pyglet
import sys

import blackmango.assetloader
import mangoed.app
import mangoed.configure

ARGUMENTS = (
    ('level', {
        'help': 'The name of the level to edit. If the level does not exist on'
                ' startup it will be created on save.',
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

    from mangoed.ui.views.editor import EditorView
    mangoed.ui.editor_window.set_view(EditorView(args.level))

    pyglet.clock.schedule(mangoed.ui.editor_window.tick)

    mangoed.app.app.run()

    sys.exit(mangoed.app.app.returncode)

