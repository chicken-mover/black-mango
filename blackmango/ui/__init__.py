"""
The user interface for the game.

Defines the GameWindow class, which delegates events to the rest of the app,
including the GameEngine.
"""

import pyglet
import sys

import blackmango.configure
import blackmango.engine

game_window = None

# There is only one GameWindow object active at any one time.
def init(*args, **kwargs):
    global game_window
    game_window = GameWindow(*args, **kwargs)

class GameWindow(pyglet.window.Window):

    def __init__(self):

        global game_window_size

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
        
    def on_draw(self):
        self.clear()
        blackmango.engine.game_engine.on_draw()
        if blackmango.configure.DEBUG:
            self.fps_display.draw()
        
    def tick(self, dt):

        if self.keyboard[pyglet.window.key.Q]:
            sys.exit(0)

        if self.mode == 'menu':
        
            if self.keyboard[pyglet.window.key.N]:
                blackmango.engine.game_engine.new_game()
                self.mode = 'game'
        
        elif self.mode == 'game':

            blackmango.engine.game_engine.input_tick(self.keyboard)
            blackmango.engine.game_engine.game_tick()
