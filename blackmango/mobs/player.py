"""
The main player class, a subclass of the BasicMobileSprite class.
"""

import blackmango.configure
import blackmango.sprites

from blackmango.masks.masklist import MASKS
from blackmango.ui import keyboard

def isalive(f):
    def wrapped(self, *args, **kwargs):
        if self.dead:
            return
        else:
            return f(self, *args, **kwargs)
    return wrapped

class Player(blackmango.sprites.BasicMobileSprite):

    def __init__(self, x = 0, y = 0, z = 0):

        color = (0,255,0, 255)

        super(Player, self).__init__(None, x, y, z,
                color)

        self.logger = blackmango.configure.logger

        self.current_mask = None
        self.dead = False

    @isalive
    def activate_mask(self, i):
        if self.current_mask:
            self.logger.debug('Deactivate mask: %s' % self.current_mask)
            self.current_mask.on_deactivate()
        self.logger.debug('Activate mask: %s' % i)
        mask = MASKS[i]
        # TODO: Animate mask change
        self.current_mask = mask
        mask.on_activate(self)

    @isalive
    def teleport(self, x, y, z):
        """
        Overrides the parent class, because if the player changes floors, we
        want to move the currently viewed level floor, too.
        """
        level = blackmango.ui.game_window.view.current_level

        dest = (x, y, z)
        level.unset_mob(*self.world_location)
        level.set_mob(self, *dest)
        self.world_location = dest
        if level.current_floor != z:
            level.switch_floor(z)
        self.translate()

    @isalive
    def kill(self):
        self.dead = True

    @isalive
    def move(self, *args, **kwargs):
        super(Player, self).move(*args, **kwargs)

    @isalive
    def turn(self, *args, **kwargs):
        super(Player, self).turn(*args, **kwargs)

    @isalive
    def tick(self):
        """
        Called on every tick by the GameView object.
        """

        if self.current_mask:
            self.current_mask.tick(self)
        
        move = [0,0]
        if keyboard.check('move_up'):
            move[1] = -1
        elif keyboard.check('move_down'):
            move[1] = 1
        # Enable diagonals: change this 'elif' to 'if'
        elif keyboard.check('move_left'):
            move[0] = -1
        elif keyboard.check('move_right'):
            move[0] = 1

        elif keyboard.check('switch_mask_1'):
            self.activate_mask(1)
        elif keyboard.check('switch_mask_2'):
            self.activate_mask(2)
        elif keyboard.check('switch_mask_3'):
            self.activate_mask(3)
        elif keyboard.check('switch_mask_4'):
            self.activate_mask(4)

        if move != [0,0]:
            self.move(*move)
