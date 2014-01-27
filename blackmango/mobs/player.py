"""
The main player class, a subclass of the BasicMobileSprite class.
"""

from pyglet.window import key

import blackmango.configure
import blackmango.sprites

from blackmango.masks.masklist import MASKS

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
    def activate_mask(self, id):

        if self.current_mask:
            self.logger.debug('Deactivate mask: %s' % self.current_mask)
            self.current_mask.on_deactivate()
        self.logger.debug('Activate mask: %s' % id)
        mask = MASKS[id]
        # TODO: Animate mask change
        self.current_mask(mask)
        mask.on_activate(self)

    @isalive
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
    def tick(self, keyboard, level):
        """
        Called on every tick by the GameView object.
        """

        if self.current_mask:
            self.current_mask.tick(self, level)
        
        move = [0,0]
        if keyboard[key.UP]:
            move[1] = -1
        elif keyboard[key.DOWN]:
            move[1] = 1
        elif keyboard[key.LEFT]: # enable diagonals: change this 'elif' to 'if'
            move[0] = -1
        elif keyboard[key.RIGHT]:
            move[0] = 1
        if move != [0,0]:
            self.move(level, *move)

        elif keyboard[key.NUM_1]:
            self.activate_mask(MASKS[1])
        elif keyboard[key.NUM_2]:
            self.activate_mask(MASKS[2])
        elif keyboard[key.NUM_3]:
            self.activate_mask(MASKS[3])

