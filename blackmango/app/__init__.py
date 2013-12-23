
import pyglet

class BlackMangoApp(pyglet.app.EventLoop):

    def __init__(self, main_window):

        super(BlackMangoApp, self).__init__()
        self.main_window = main_window

        pyglet.clock.schedule(main_window.tick)

    def idle(self):
        """
        Potentially very useful. Fires on any kind of input, including OS-level
        key repeats
        """
        return super(BlackMangoApp, self).idle()


