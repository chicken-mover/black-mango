"""
Base view class
"""

class BaseView(object):

    def __init__(self):
        pass

    def on_draw(self):
        """
        Called on every window draw (unless the window isn't drawing views for
        some reason, like during loading of new games).
        """
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called by the window on mouse clicks.
        """
        pass

    def tick(self, keyboard):
        """
        Called on every window tick
        """
        pass
