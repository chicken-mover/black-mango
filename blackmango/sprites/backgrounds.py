
import pyglet

import blackmango.configure
import blackmango.ui

class BackgroundImage(object):

    def __init__(self, image):

        w, h = 128, 128
        
        image = blackmango.assetloader.load_image(image)
        self.img = pyglet.image.TileableTexture.create_for_image(image)

    def draw(self):
        w, h = blackmango.ui.game_window.get_size()
        self.img.blit_tiled(1, 1, 0, w, h)

