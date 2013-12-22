
import pyglet

import blackmango.configure
import blackmango.sprites.base

materials_batch = pyglet.graphics.Batch()

class BasicMaterialSprite(blackmango.sprites.base.BaseSprite):
    
    def __init__(self, image = None,
            x = 0,
            y = 0,
            z = 0
        ):

        color = (255,255,255,255)
        group = blackmango.configure.ORDERED_GROUPS.get('background')

        super(BasicMaterialSprite, self).__init__(image, x, y, z,
                materials_batch, group, color)

        self.is_solid = 1
        self.is_mover = 0
        self.is_portal = 0
        self.opacity = 0


class Wall(BasicMaterialSprite):
   pass


MATERIALS = {
    0: None,
    1: Wall,
}
