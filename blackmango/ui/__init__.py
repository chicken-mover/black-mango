"""
The user interface for the game.

Defines the GameWindow class, which delegates events to the rest of the app,
including the GameEngine.
"""

import pyglet
import sys

import blackmango.configure

game_window = None

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

    draw_events = []
    dispatch_engine_draw = False

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

    def show_menu(self):

        self.main_title = blackmango.ui.labels.MainTitleCard('BLACK MANGO')
        self.sub_title = blackmango.ui.labels.SubTitleCard(
                'press N to start a new game')
        self.register_draw(
            blackmango.ui.labels.titles_batch
        )

    def hide_menu(self):
        self.unregister_draw(blackmango.ui.labels.titles_batch)
        self.main_title.delete()
        self.sub_title.delete()

    def show_titlecard(self, text):
        self.titlecard = blackmango.ui.labels.MainTitleCard(text)
        self.register_draw(
            blackmango.ui.labels.titles_batch
        )

    def hide_titlecard(self):
        self.titlecard.delete()
        self.unregister_draw(
            blackmango.ui.labels.titles_batch
        )

    def register_draw(self, b):
        """
        Add a batch <b> to be called when the GameEngine's `on_draw` handler
        is triggered.
        """
        blackmango.configure.logger.info('Registering ui draw: %s' % repr(b))
        self.draw_events.append(b)

    def unregister_draw(self, b):
        """
        Remove a batch <b> from the pool of draw events.
        """
        blackmango.configure.logger.info('Unregistering ui draw: %s' % repr(b))
        self.draw_events = filter(lambda x: x is not b, self.draw_events)
        
    def on_draw(self):
        self.clear()
        for b in self.draw_events:
            b.draw()
        if self.dispatch_engine_draw:
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

            self.dispatch_engine_draw = True
            blackmango.engine.game_engine.input_tick(self.keyboard)
            blackmango.engine.game_engine.game_tick()
