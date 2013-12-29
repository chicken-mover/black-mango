"""
The main player class, a subclass of the BasicMobileSprite class.
"""

import blackmango.configure
import blackmango.mob

class Player(blackmango.mobs.BasicMobileSprite):

    current_level = None
    
    def __init__(self, x = 0, y = 0, z = 0):

        color = (0,255,0, 255)
        group = blackmango.configure.ORDERED_GROUPS.get('player')

        super(Player, self).__init__(None, x, y, z,
                color)

    def teleport(self, x, y, z):
        """
        Overrides the parent class, because if the player changes floors, we
        want to move the currently viewed level floor, too.
        """
        dest = (x, y, z)
        self.current_level.set_mob(None, *self.world_location)
        self.current_level.set_mob(self, *dest)
        self.world_location = dest
        if self.current_level.current_floor != z:
            self.current_level.switch_floor(z)
        self.translate()

