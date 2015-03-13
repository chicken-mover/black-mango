"""
The user interface for the game.
"""

import pyglet
import sys

import blackmango.configure

#: A global reference to the instance of :class:`GameWindow` created during
#: initialization. There is only one GameWindow object active at any one time.
game_window = None

#: An instance of :class:`pyglet.window.Platform` for the current platform.
#: This is initailized at import.
game_platform = pyglet.window.get_platform()
#: An instance of :class:`pyglet.window.Display` that represents the default
#: display according to pyglet. This is initailized at import.
game_display = game_platform.get_default_display()
#: An instance of :class:`pyglet.window.Screen` that represents the default
#: screen according to pyglet. This is initailized at import.
game_screen = game_display.get_default_screen()

def init(*args, **kwargs):
    """
    Called by the central startup routine during initialization. This creates an
    instance of :class:`GameWindow` in the module's global scope so that it
    can be accessed by other modules as `blackmango.app.game_window`.
    """
    global game_window
    # Prevent circular imports
    blackmango.configure.logger.debug("Initializing GameWindow as game_window")
    game_window = GameWindow(*args, **kwargs)

class GameWindow(pyglet.window.Window):
    """
    A subclass of :class:`pyglet.window.Window`. This class has two primary
    purposes:

    1. To track the current view, as represented by an object from one of the
       :mod:`blackmango.ui.views` submodules, and
    2. to delegate inputs and clock ticks from pyglet to the views and (through
       them) whatever the views are controlling.
    """

    #: A property storing a reference to the current view.
    view = None

    def __init__(self):
        """
        Set up the game view based on the current values in
        :mod:`blackmango.configure`.
        """

        if blackmango.configure.FULLSCREEN:
            super(GameWindow, self).__init__(
                    fullscreen = blackmango.configure.FULLSCREEN,
                    style = pyglet.window.Window.WINDOW_STYLE_BORDERLESS,
                    caption = blackmango.configure.MAIN_WINDOW_TITLE)
        else:
            width, height = blackmango.configure.SCREEN_SIZE
            super(GameWindow, self).__init__(
                    width = width,
                    height = height,
                    style = pyglet.window.Window.WINDOW_STYLE_BORDERLESS,
                    caption = blackmango.configure.MAIN_WINDOW_TITLE)

            # Center the window
            scr_w, scr_h = game_screen.width, game_screen.height
            self.set_location((scr_w - self.width) / 2,
                (scr_h - self.height) / 2)

        # Might turn this on later, or depending on the DEBUG flag.
        #self.set_exclusive_mouse()
        self.logger = blackmango.configure.logger

        self.keyboard = pyglet.window.key.KeyStateHandler()
        self.push_handlers(self.keyboard)
        
        self.resizeable = False

        self.fps_display = pyglet.clock.ClockDisplay()

    def set_view(self, view):
        """
        Set the current view to an instance of a view object that is a subclass
        of :class:`blackmango.ui.views.BaseView`.
        """
        if self.view:
            self.logger.debug("Tearing down view %s" %  repr(self.view))
            self.view.destroy()
        self.logger.debug("Setting view: %s" % repr(view))
        self.view = view
        self.view.load()
        
    def on_draw(self):
        """
        Triggered by the application event loop, this method delegates further
        draws to the current view.
        """
        self.clear()
        if self.view:
            self.view.on_draw()
        if blackmango.configure.DEBUG:
            self.fps_display.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Triggered by the application event loop, this method delegates further
        event calls to the current view.
        """
        if self.view:
            self.view.on_mouse_press(x, y, button, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        """
        Triggered by the application event loop, this method delegates further
        event calls to the current view.
        """
        if self.view:
            self.view.on_mouse_motion(x, y, dx, dy)

    def on_key_press(self, key, modifiers):
        """
        Triggered by the application event loop, this method delegates further
        event calls to the current view.
        """
        if self.view and hasattr(self.view, 'on_key_press'):
            self.view.on_key_press(key, modifiers)
        
    def tick(self, dt):
        """
        Triggered by the application event loop, this method delegates further
        event calls to the current view.
        """
        if self.view:
            self.view.tick()
