"""
Base view class. Should be inherited and methods overridden, rather than copied
out when creating view modules, in case the spec changes or new view methods
are added universally.
"""

class BaseView(object):

    def __init__(self):
        pass

    def destroy(self):
        """
        Called when the view is switched away from this view.
        """
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

    def on_mouse_motion(self, x, y, dx, dy):
        """
        Called by the window during mouse movement.
        """
        pass

    def on_key_press(self, key, modifiers):
        """
        Called by the window on every key press
        """
        pass

    def tick(self):
        """
        Called on every window tick
        """
        pass
