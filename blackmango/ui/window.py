
import pyglet
import sys

import blackmango.configure
import blackmango.engine
import blackmango.materials
import blackmango.mob

game_window_size = None

class GameWindow(pyglet.window.Window):

    def __init__(self):

        global game_window_size

        self.label = pyglet.text.Label(
                blackmango.configure.MAIN_WINDOW_TITLE)

        if blackmango.configure.FULLSCREEN:
            super(GameWindow, self).__init__(
                    fullscreen = blackmango.configure.FULLSCREEN)
        else:
            width, height = blackmango.configure.SCREEN_SIZE
            super(GameWindow, self).__init__(
                    width = width,
                    height = height)

        #self.set_exclusive_mouse()

        self.logger = blackmango.configure.logger

        self.mode = 'menu'
        self.engine = blackmango.engine.GameEngine()

        game_window_size = self.get_size()
        self.resizeable = False

    def on_draw(self):
        self.clear()
        self.label.draw()

        blackmango.materials.materials_batch.draw()
        blackmango.mob.mobs_batch.draw()

    def on_key_press(self, symbol, modifiers):
        
        self.logger.debug('%s.on_key_press(%s, %s)' % (self, symbol, modifiers))
        
        if symbol == pyglet.window.key.Q:
            sys.exit(0)

        if self.mode == 'menu':
            if symbol == pyglet.window.key.N:
                self.engine.new_game()
                self.mode = 'game'
        elif self.mode == 'game':
            pass
