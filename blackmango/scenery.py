
import pyglet

import blackmango.configure
import blackmango.ui

class Background(object):

    def __init__(self, image):
        self.image = image
        image = blackmango.assetloader.load_image(self.image)
        self.texture = pyglet.image.TileableTexture.create_for_image(image)

    def draw(self):
        w, h = blackmango.ui.game_window.get_size()
        self.texture.blit_tiled(1, 1, 0, w, h)

