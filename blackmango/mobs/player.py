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

    def __init__(self):

        color = (0,255,0, 255)

        super(Player, self).__init__(None, color)

        self.logger = blackmango.configure.logger

        self.current_mask = None
        self.dead = False
        self.moving = False
    
    @isalive
    def activate_mask(self, i):
        if self.current_mask:
            self.logger.debug('Deactivate mask: %s' % self.current_mask)
            self.current_mask.on_deactivate(self)
        self.logger.debug('Activate mask: %s' % i)
        mask = MASKS[i]
        # TODO: Animate mask change
        self.current_mask = mask
        mask.on_activate(self)

    @isalive
    def kill(self):
        self.dead = True

    @isalive
    def move(self, *args, **kwargs):
        res = super(Player, self).move(*args, **kwargs)
        if res:
            blackmango.sprites.set_translation_offset(*args)
        return res

    @isalive
    def turn(self, *args, **kwargs):
        return super(Player, self).turn(*args, **kwargs)

    @isalive
    def tick(self):
        """
        Called on every tick by the GameView object.
        """

        if self.current_mask:
            self.current_mask.tick(self)

