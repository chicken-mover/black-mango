"""
The main app class, a subclass of pyglet.app.EventLoop.

This class will initialize the main game window, as well as the main engine
class. They are both accessible as attributes of this class.
"""

import pyglet

import blackmango.engine
import blackmango.ui

class BlackMangoApp(pyglet.app.EventLoop):

    def __init__(self):

        super(BlackMangoApp, self).__init__()

        self.engine = blackmango.engine.GameEngine()
        self.main_window = blackmango.ui.GameWindow(self.engine)

        pyglet.clock.schedule(self.main_window.tick)
