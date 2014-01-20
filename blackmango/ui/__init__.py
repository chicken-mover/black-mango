"""
The user interface for the game.
"""

import pyglet
import sys

import blackmango.configure

game_window = None

game_platform = pyglet.window.get_platform()
game_display = game_platform.get_default_display()
game_screen = game_display.get_default_screen()

# There is only one GameWindow object active at any one time.
def init(*args, **kwargs):
    """
    Called by the central startup routine during initialization.
    """
    global game_window
    # Prevent circular imports
    blackmango.configure.logger.info("Initializing GameWindow as game_window")
    game_window = GameWindow(*args, **kwargs)

class GameWindow(pyglet.window.Window):

    view = None

    def __init__(self):

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

        # Might turn this on later, or depending on the DEBUG flag.
        #self.set_exclusive_mouse()

        self.keyboard = pyglet.window.key.KeyStateHandler()
        self.push_handlers(self.keyboard)

        self.logger = blackmango.configure.logger
        
        self.resizeable = False
        self.set_location(1, 1)

        self.fps_display = pyglet.clock.ClockDisplay()

    def set_view(self, view):
        if self.view:
            self.view.destroy()
        self.view = view
        
    def on_draw(self):
        self.clear()
        if self.view:
            self.view.on_draw()
        if blackmango.configure.DEBUG:
            self.fps_display.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        if self.view:
            self.view.on_mouse_press(x, y, button, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        if self.view:
            self.view.on_mouse_motion(x, y, dx, dy)

    def on_key_press(self, key, modifiers):

        if self.view and hasattr(self.view, 'on_key_press'):
            self.view.on_key_press(key, modifiers, self.keyboard)
        
    def tick(self, dt):

        if blackmango.configure.DEBUG and self.keyboard[pyglet.window.key.Q]:
            sys.exit(0)

        if self.view:
            self.view.tick(self.keyboard)
