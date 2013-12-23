
import pyglet
import sys

import blackmango.configure
import blackmango.engine

game_window_size = None

class GameWindow(pyglet.window.Window):

    def __init__(self, engine):

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

        #self.set_exclusive_mouse()

        self.keyboard = pyglet.window.key.KeyStateHandler()
        self.push_handlers(self.keyboard)

        self.logger = blackmango.configure.logger

        self.mode = 'menu'
        self.engine = engine

        game_window_size = self.get_size()
        
        self.resizeable = False
        self.set_location(1, 1)

        self.current_key_symbol = None,
        self.current_key_modifiers = None,

    def on_draw(self):
        self.clear()

        self.engine.on_draw(self)

    def tick(self, dt):

        if self.keyboard[pyglet.window.key.Q]:
            sys.exit(0)

        if self.mode == 'menu':
        
            if self.keyboard[pyglet.window.key.N]:
                self.engine.new_game()
                self.mode = 'game'
        
        elif self.mode == 'game':

            self.engine.tick(self.keyboard)
