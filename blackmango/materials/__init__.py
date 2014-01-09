"""
Materials are sprites that inherit from the BaseSprite class and are used as
objects in a level.

They can have behaviours, the interface for which is really rough at this
point.

This file should contain only the base material classes. Subclasses of the
base materials should be divided out into logically appropriate submodules.
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

    def interaction_callback(self, level, mob):
        """
        This is called by the mob object when it steps onto the material.
        Going forward, we might need to account for other kinds of interaction,
        like walking up to an object, or more complex ones that do things like
        interact with the level itself
        """
        mob.teleport(level, *self.destination)
        

class VoidMaterial(BaseMaterial):

    def __init__(self):

        color = (0,0,0,0)

        super(VoidMaterial, self).__init__(color = color)

        self.is_solid = 1
        self.is_mover = 0
        self.is_portal = 0
        self.opacity = 0