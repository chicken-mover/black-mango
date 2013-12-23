
import pyglet

import blackmango.engine
import blackmango.ui.window

class BlackMangoApp(pyglet.app.EventLoop):

    def __init__(self):

        super(BlackMangoApp, self).__init__()

        self.engine = blackmango.engine.GameEngine()
        self.main_window = blackmango.ui.window.GameWindow(self.engine)

        pyglet.clock.schedule(self.main_window.tick)

    def idle(self):
        """
        Potentially very useful. Fires on any kind of input, including OS-level
        key repeats
        """
        return super(BlackMangoApp, self).idle()


