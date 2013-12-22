
import pyglet

class BlackMangoApp(pyglet.app.EventLoop):

    def __init__(self, main_window):

        super(BlackMangoApp, self).__init__()
        self.main_window = main_window

    def idle(self):

        self.main_window.tick()
        return super(BlackMangoApp, self).idle()

