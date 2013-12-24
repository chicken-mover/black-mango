"""
Materials are sprites that inherit from the BaseSprite class and are used as
objects in a level.

They can have behaviours, the interface for which is really rough at this
point.
"""

import pyglet

import blackmango.configure
import blackmango.sprites

materials_batch = pyglet.graphics.Batch()

class BaseMaterial(blackmango.sprites.BaseSprite):
    
    def __init__(self, image = None,
            x = 0,
            y = 0,
            z = 0,
            color = None,
        ):

        color = color or (255,255,255,255)
        group = blackmango.configure.ORDERED_GROUPS.get('background')

        super(BaseMaterial, self).__init__(image, x, y, z,
                materials_batch, group, color)

        self.is_solid = 1
        self.is_mover = 0
        self.is_portal = 0
        self.opacity = 0

class BasePortalMaterial(BaseMaterial):

    def __init__(self, image = None,
            x = 0,
            y = 0,
            z = 0,
            color = None,
            destination = None, 
        ):

        color = color or (255,0,0,255)
        super(BasePortalMaterial, self).__init__(image, x, y, z,
                color)

        self.is_solid = 0
        self.is_portal = 1
        self.destination = destination

    def interaction_callback(self, mob):
        mob.teleport(*self.destination)


class Wall(BaseMaterial):
   pass

class StairUp(BasePortalMaterial):
    pass

class StairDown(BasePortalMaterial):
    pass

class Door(BasePortalMaterial):
    pass

class VoidMaterial(BaseMaterial):

    def __init__(self):

        color = (0,0,0,0)

        super(VoidMaterial, self).__init__(color = color)

        self.is_solid = 1
        self.is_mover = 0
        self.is_portal = 0
        self.opacity = 0

# Global dict for lookups by the levels module
MATERIALS = {
    -1: VoidMaterial,
    0: None,
    1: Wall,
    7: Door,
    8: StairUp,
    9: StairDown,
}
