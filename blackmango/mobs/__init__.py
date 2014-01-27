"""
Sprites that move. Players and NPCs.

This file should contain only the base mob classes. Subclasses of the
base mobs should be divided out into logically appropriate submodules.
"""

import blackmango.sprites

def notfrozen(f):
    def wrapped(self, *args, **kwargs):
        if self.is_frozen:
            return False
        else:
            return f(self, *args, **kwargs)
    return wrapped

class SimpleMob(blackmango.sprites.BasicMobileSprite):

    def __init__(self, *args, **kwargs):
        super(SimpleMob, self).__init__(*args, **kwargs)
        self.is_frozen = False

    @notfrozen
    def teleport(self, *args, **kwargs):
        super(SimpleMob, self).teleport(*args, **kwargs)

    @notfrozen
    def turn(self, *args, **kwargs):
        super(SimpleMob, self).turn(*args, **kwargs)

    @notfrozen
    def move(self, *args, **kwargs):
        super(SimpleMob, self).move(*args, **kwargs)

    @notfrozen
    def do_behavior(self, level):
        """
        This method is called by the level and will determine if the sub-class's
        actual 'behavior' method should be called. This method should not be
        subclassed unless you know what you are doing.
        """
        return self.behaviour(level)

    def behavior(self, level): pass
