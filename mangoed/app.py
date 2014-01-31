"""
The main app class, a subclass of pyglet.app.EventLoop.

This class will initialize the main game window, as well as the main engine
class. They are both accessible as attributes of this class.
"""

import pyglet

import mangoed.configure

app = None

def init(*args, **kwargs):
    """
    Called by the central startup routine during initialization.
    """
    global game_app
    mangoed.configure.logger.debug("Initializing MangoEd as app")
    app = MangoEd(*args, **kwargs)

class MangoEd(pyglet.app.EventLoop):

    returncode = None

    def user_quit(self):
        """
        Should be called whenever the user asks the app to quit. Stops the app
        loop so that cleanup processes can run before the program exits.
        """
        self.exit()
        self.returncode = 0
