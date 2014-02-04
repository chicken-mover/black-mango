"""
Sprites that move. Players and NPCs.

This file should contain only the base mob classes. Subclasses of the
base mobs should be divided out into logically appropriate submodules.
"""

import blackmango.sprites

def notfrozen(f):
    """
    A decorator for skipping certain methods when a mob's is_frozen flag is set.
    """
    def wrapped(self, *args, **kwargs):
        if self.is_frozen:
            return False
        else:
            return f(self, *args, **kwargs)
    return wrapped

class SimpleMob(blackmango.sprites.BasicMobileSprite):
    """
    This is a class meant to be used as a subclass for all mob objects. It
    specifies the interface for mobs, and sets the @notfrozen decorator up on
    each method of the superclass(es) that should be skipped if the mob's frozen
    flag gets set.
    """

    def __init__(self, *args, **kwargs):
        super(SimpleMob, self).__init__(*args, **kwargs)
        self.is_frozen = False

    @notfrozen
    def turn(self, *args, **kwargs):
        super(SimpleMob, self).turn(*args, **kwargs)

    @notfrozen
    def move(self, *args, **kwargs):
        super(SimpleMob, self).move(*args, **kwargs)

    @notfrozen
    def do_behavior(self):
        """
        This method is called by the level and will determine if the sub-class's
        actual 'behavior' method should be called. This method should not be
        subclassed unless you know what you are doing.
        """
        if self.animations:
            return
        return self.behavior()

    def behavior(self):
        """
        A placeholder method to be implemented by subclasses.
        """
        pass
