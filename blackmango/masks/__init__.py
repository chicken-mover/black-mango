"""
The masks worn by the player
"""

class BaseMask(object):
    """
    Define the interface
    """

    def __init__(self):
        pass

    def on_activate(self, thismob):
        pass

    def on_deactivate(self, thismob):
        pass

    def move_hook(self, level, destination, thismob):
        pass

    def teleport_hook(self, level, destination, thismob):
        pass

## TODO: Move these to seperate submodules

class MaskOfAgammemnon(BaseMask):
    pass

class NohMask(BaseMask):
    pass

class PlagueDoctorMask(BaseMask):
    pass