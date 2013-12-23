"""
Materials are sprites that inherit from the BaseSprite class and are used as
objects in a level.
"""

import pyglet

import blackmango.configure
import blackmango.sprites

materials_batch = pyglet.graphics.Batch()

class BasicMaterialSprite(blackmango.sprites.BaseSprite):
    
    def __init__(self, image = None,
            x = 0,
            y = 0,
            z = 0,
            color = None,
        ):

        color = color or (255,255,255,255)
        group = blackmango.configure.ORDERED_GROUPS.get('background')

        super(BasicMaterialSprite, self).__init__(image, x, y, z,
                materials_batch, group, color)

        self.is_solid = 1
        self.is_mover = 0
        self.is_portal = 0
        self.opacity = 0


class Wall(BasicMaterialSprite):
   pass

class VoidMaterial(BasicMaterialSprite):

    def __init__(self):

        color = (0,0,0,0)

        super(VoidMaterial, self).__init__(color = color)

        self.is_solid = 1
        self.is_mover = 0
        self.is_portal = 0
        self.opacity = 0


MATERIALS = {
    -1: VoidMaterial,
    0: None,
    1: Wall,
}
