"""
:mod:`scenery` --- Static scene graphics
===========================================

This module provides utilities for managing static scene graphics, like
backgrounds and 'doodads'.

"""

import pyglet

import blackmango.configure
import blackmango.ui

class Background(object):
    """
    A wrapper for the :py:class:`pyglet.image.TileableTexture` class which takes
    care of blitting an image across the window. Each level will generate one
    instance of this class per unique background image that is loaded for that
    level.
    """

    def __init__(self, image):
        """
        Create a new instance using *image* as the source image file. *image*
        must reside in the :ref:`Assets directory <asset-dirtree>`
        """
        self.image = image
        im = blackmango.assetloader.load_image(self.image)
        self.texture = pyglet.image.TileableTexture.create_for_image(im)

    def draw(self):
        """
        Draw the background, blitting the image in a tiled pattern from the top-
        left corner of the screen.
        """
        w, h = blackmango.ui.game_window.get_size()
        self.texture.blit_tiled(1, 1, 0, w, h)

