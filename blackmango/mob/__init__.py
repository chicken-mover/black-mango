
import pyglet

import blackmango.configure
import blackmango.sprites.base

mobs_batch = pyglet.graphics.Batch()


class BasicMobileSprite(blackmango.sprites.base.BaseSprite):
    
    def __init__(self, image = None,
            x = 0,
            y = 0,
            z = 0
        ):

        color = (0,0,255,255)
        group = blackmango.configure.ORDERED_GROUPS.get('mobs')

        super(BasicMobileSprite, self).__init__(image, x, y, z,
                mobs_batch, group, color)

        self.is_solid = 1
        self.is_mover = 1
        self.is_portal = 0
        self.opacity = 0


class Player(BasicMobileSprite):
    
    def __init__(self, x, y, z):

        color = (0,255,0, 255)
        group = blackmango.configure.ORDERED_GROUPS.get('player')

        super(Player, self).__init__(image, x, y, z,
                mobs_batch, group, color)

MATERIALS = {
    0: None,
    1: blackmango.materials.Wall,
}
