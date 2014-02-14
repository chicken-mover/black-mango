"""
:mod:`app` --- Main application event loop management
=====================================================

This module provides the :class:`BlackMangoApp` class, which manages the event
loop.
"""

import pyglet

import blackmango.configure

game_app = None

def init(*args, **kwargs):
    """
    Called by the central startup routine during initialization. This creates an
    instance of :class:`BlackMangoApp` in the module's global scope so that it
    can be accessed by other modules as `blackmango.app.game_app`.
    """
    global game_app
    blackmango.configure.logger.debug("Initializing BlackMangoApp as game_app")
    game_app = BlackMangoApp(*args, **kwargs)

class BlackMangoApp(pyglet.app.EventLoop):
    """
    A subclass of :py:class:`pyglet.app.EventLoop`. This manages the running
    loop and is responsible for setting an exit code when the loop quits.
    """

    #: Has a value of ``None`` until the event loop exits, at which point the
    #: value will match a suitable POSIX exit code (see
    #: :mod:`errno <python:errno>` in the stdlib). (0 for a normal exit, a
    #: positive integer for anything else.)
    returncode = None

    def user_quit(self):
        """
        Should be called whenever the user asks the app to quit. Stops the app
        loop so that cleanup processes can run before the program exits.

        Once the app has quit, this method will set the value of
        :attr:`returncode` so that the main program can use it to determine
        which exit code to quit with.
        """
        self.exit()
        self.returncode = 0
