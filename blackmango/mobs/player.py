"""
The main player class, a subclass of the BasicMobileSprite class.
"""

import blackmango.configure
import blackmango.mobs

class Player(blackmango.mobs.BasicMobileSprite):
    
    def __init__(self, x = 0, y = 0, z = 0):

        color = (0,255,0, 255)

        super(Player, self).__init__(None, x, y, z,
                color)

    def teleport(self, level, x, y, z):
        """
        Overrides the parent class, because if the player changes floors, we
        want to move the currently viewed level floor, too.
        """
        dest = (x, y, z)
        level.set_mob(None, *self.world_location)
        level.set_mob(self, *dest)
        self.world_location = dest
        if level.current_floor != z:
            level.switch_floor(z)
        self.translate()

