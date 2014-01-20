"""
The main player class, a subclass of the BasicMobileSprite class.
"""

import blackmango.configure
import blackmango.masks.masklist
import blackmango.mobs

class Player(blackmango.mobs.BasicMobileSprite):
    
    def __init__(self, x = 0, y = 0, z = 0):

        color = (0,255,0, 255)

        super(Player, self).__init__(None, x, y, z,
                color)

        self.current_mask = None

    def activate_mask(self, id):

        if self.current_mask:
            self.current_mask.on_deactivate()
        mask = blackmango.masks.masklist.MASKS[id]
        # TODO: Animate mask change
        self.current_mask(mask)
        mask.on_activate(self)

    def teleport(self, level, x, y, z):
        """
        Overrides the parent class, because if the player changes floors, we
        want to move the currently viewed level floor, too.
        """
        dest = (x, y, z)
        level.unset_mob(*self.world_location)
        level.set_mob(self, *dest)
        self.world_location = dest
        if level.current_floor != z:
            level.switch_floor(z)
        self.translate()

    def user_input(self, keyboard, level):
        """
        Called on every tick by the GameView object.
        """

        if keyboard[key.UP]:
            self.move(level, 0, -1)
        elif keyboard[key.DOWN]:
            self.move(level, 0, 1)
        elif keyboard[key.LEFT]:
            self.move(level, -1, 0)
        elif keyboard[key.RIGHT]:
            self.move(level, 1, 0)

