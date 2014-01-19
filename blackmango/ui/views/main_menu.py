"""
Initial title menu view
"""

MENU_OPTIONS = {
    'New game': blackmango.engine.game_engine.new_game,
    'Load game': None, # Set the 'load_game' view
    'Quit': blackmango.app.user_quit
}

class BaseView(object):

    def __init__(self):
        self.menu_options = MENU_OPTIONS

    def on_draw(self):
        """
        Called on every window draw (unless the window isn't drawing views for
        some reason, like during loading of new games).
        """
        pass

    def tick(self, keyboard):
        """
        Called on every window tick
        """
        pass
