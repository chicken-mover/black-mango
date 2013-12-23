
import pyglet
import sys

import blackmango.configure
import blackmango.engine

game_window_size = None

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

        #self.set_exclusive_mouse()

        self.logger = blackmango.configure.logger

        self.mode = 'menu'
        self.engine = blackmango.engine.GameEngine()

        game_window_size = self.get_size()
        
        self.resizeable = False
        self.set_location(1, 1)

        self.current_key_symbol = None,
        self.current_key_modifiers = None,

    def on_draw(self):
        self.clear()

        self.engine.on_draw(self)

    def on_key_press(self, symbol, modifiers):
        
        self.logger.debug('%s.on_key_press(%s, %s)' % (self, symbol, modifiers))

        self.current_key_symbol = symbol
        self.current_key_modifiers = modifiers

    def on_key_release(self, symbol, modifiers):

        self.logger.debug('%s.on_key_release(%s, %s)' % (self, symbol, modifiers))
        
        if self.current_key_symbol == symbol:
            self.current_key_symbol = None

        self.current_key_modifiers ^= modifiers


    def tick(self, dt):

        if self.current_key_symbol == pyglet.window.key.Q:
            sys.exit(0)

        if self.mode == 'menu':
        
            if self.current_key_symbol == pyglet.window.key.N:
                self.engine.new_game()
                self.mode = 'game'
        
        elif self.mode == 'game':

            self.engine.on_key_press(self.current_key_symbol,
                    self.current_key_modifiers)
