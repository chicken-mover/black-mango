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

    returncode = None

    def __init__(self, *args):

        super(BlackMangoApp, self).__init__()

    def user_quit(self):
        """
        Should be called whenever the user asks the app to quit. Stops the app
        loop so that cleanup processes can run before the program exits.
        """
        self.exit()
        self.returncode = 0
