"""
This module provides the :class:`BaseView` class, from which all other views
inherit. The base class also establishes the interface that all view classes
should adhere to.
"""

class BaseView(object):

    def __init__(self): pass

    def load(self):
        """
        Some initialization has to be deffered until the view object exists and
        is set properly on the parent :class:`blackmango.ui.GameWindow` object.

        Once the object exists, this method is called immediately.
        """
        pass

    def destroy(self):
        """
        Called when the view is switched away from this view. Tears down the
        view and clears anything which should no longer be drawn.
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
        Called by the :class:`blackmango.ui.GameWindow` instance when this event
        occurs. The arguments passed in are identical to the ones received by
        the :class:`blackmango.ui.GameWindow` method, and are documented by
        :class:`pyglet.window.Window`.
        """
        pass

    def on_mouse_motion(self, x, y, dx, dy):
        """
        Called by the :class:`blackmango.ui.GameWindow` instance when this event
        occurs. The arguments passed in are identical to the ones received by
        the :class:`blackmango.ui.GameWindow` method, and are documented by
        :class:`pyglet.window.Window`.
        """
        pass

    def on_key_press(self, key, modifiers):
        """
        Called by the :class:`blackmango.ui.GameWindow` instance when this event
        occurs. The arguments passed in are identical to the ones received by
        the :class:`blackmango.ui.GameWindow` method, and are documented by
        :class:`pyglet.window.Window`.
        """
        pass

    def tick(self):
        """
        Called on every window tick.
        """
        pass
