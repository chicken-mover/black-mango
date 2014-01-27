"""
Materials are sprites that inherit from the BaseSprite class and are used as
objects in a level.

They can have behaviours, the interface for which is really rough at this
point.

This file should contain only the base material classes. Subclasses of the
base materials should be divided out into logically appropriate submodules.
"""

import blackmango.configure
import blackmango.sprites

class BaseMaterial(blackmango.sprites.BaseSprite):
    
    def __init__(self, image = None,
            x = 0,
            y = 0,
            z = 0,
            color = None,
        ):

        color = color or (255,255,255,255)

        super(BaseMaterial, self).__init__(image, x, y, z,
                'background', color)

        self.is_solid = True
        self.is_mover = False
        self.is_portal = False
        self.opacity = 0

    def interaction_callback(self, level, mob):
        pass

class BasePortalMaterial(BaseMaterial):

    def __init__(self, image = None,
            x = 0,
            y = 0,
            z = 0,
            color = None,
            destination = None, 
        ):

        color = color or (255,0,0,255)
        super(BasePortalMaterial, self).__init__(image, x, y, z, color)

        self.is_solid = False
        self.is_portal = True
        self.destination = destination

        self.kwargs = {
            'destination': destination,        
        }

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

        self.is_solid = True
        self.is_mover = False
        self.is_portal = False
        self.opacity = 0
