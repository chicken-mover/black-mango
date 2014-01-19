"""
The user interface for the game.

Defines the GameWindow class, which delegates events to the rest of the app,
including the GameEngine.
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
    global blackmango
    global game_window
    # Prevent circular imports
    import blackmango.engine
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

        self.mode = 'menu'
        
        self.resizeable = False
        self.set_location(1, 1)

        self.fps_display = pyglet.clock.ClockDisplay()

    def set_view(self, view):
        # make sure __del__ gets called now
        if self.view:
            self.view.destroy()
        self.view = view

    def show_menu(self):
        self.main_title = blackmango.ui.labels.MainTitleCard('BLACK MANGO')
        self.sub_title = blackmango.ui.labels.SubTitleCard(
                'press N to start a new game')

    def hide_menu(self):
        self.main_title.delete()
        self.sub_title.delete()

    def show_titlecard(self, text):
        self.titlecard = blackmango.ui.labels.MainTitleCard(text)

    def hide_titlecard(self):
        self.titlecard.delete()
        
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

        return

        if self.mode == 'menu':
        
            if self.keyboard[pyglet.window.key.N]:
                blackmango.engine.game_engine.new_game()
                self.mode = 'game'
        
        elif self.mode == 'game':

            self.dispatch_engine_draw = True
            blackmango.engine.game_engine.input_tick(self.keyboard)
            blackmango.engine.game_engine.game_tick()
