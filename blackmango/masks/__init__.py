"""
The masks worn by the player
"""

import blackmango.ui

class BaseMask(object):
    """
    Define the interface
    """

    def __init__(self):
        pass

    def on_activate(self, player):
        pass

    def on_deactivate(self, player):
        pass

    def move_hook(self, destination, player):
        """
        If a hook returns False, the rest of the default method on the player
        object will not execute.
        """
        return True

    def teleport_hook(self, destination, player):
        """
        If a hook returns False, the rest of the default method on the player
        object will not execute.
        """
        return True

    def tick_hook(self, player):
        """
        If a hook returns False, the rest of the default method on the player
        object will not execute.
        """
        return True

# TODO: Move these to seperate submodules

class MaskOfAgammemnon(BaseMask):
    """
    Looking at an enemy freezes them in place.
    """

    def on_deactivate(self, player):
        level = blackmango.ui.game_window.view.current_level
        for mob in level.mobs.values():
            if hasattr(mob, 'frozen_by') and mob.frozen_by is self:
                mob.is_frozen = False

    def tick(self, player):
        level = blackmango.ui.game_window.view.current_level
        for mob in level.mobs.values():
            if mob is not player and player.can_see(mob) \
               and not mob.is_frozen:
                mob.is_frozen = True
                mob.frozen_by = self
        return True

class NohMask(BaseMask):
    """
    Renders the player invisible
    """

    def on_activate(self, player):
        self.player.opacity = 0

    def on_deactivate(self, player):
        self.player.opacity = 1

class PlagueDoctorMask(BaseMask):
    pass
