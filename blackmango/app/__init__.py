"""
The main app class, a subclass of pyglet.app.EventLoop.

This class will initialize the main game window, as well as the main engine
class. They are both accessible as attributes of this class.
"""

import pyglet

import blackmango.configure

game_app = None

def init(*args, **kwargs):
    """
    Called by the central startup routine during initialization.
    """
    global game_app
    blackmango.configure.logger.info("Initializing BlackMangoApp as game_app")
    game_app = BlackMangoApp(*args, **kwargs)

class BlackMangoApp(pyglet.app.EventLoop):

    def __init__(self, *args):

        super(BlackMangoApp, self).__init__()

    def schedule(self, f):
        """
        Schedule a callable <f> to be called at every Pyglet clock tick, using
        `pyglet.clock.schedule`. Any callable scheduled this way must accept a
        single argument (the number of ticks that have passed since the previous
        call).
        """
        pyglet.clock.schedule(f)
