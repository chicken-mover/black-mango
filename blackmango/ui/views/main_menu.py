"""
Initial title menu view
"""

import pyglet

import blackmango.app
import blackmango.ui.labels
import blackmango.ui.views

main_menu_batch = pyglet.graphics.Batch()

TITLE_COLOR = (255, 255, 255, 255)

class MainMenu(blackmango.ui.views.BaseView):
    
    def __init__(self):
        
        self.menu_options = {
            'New game': blackmango.engine.game_engine.new_game,
            'Load game': None, # Set the 'load_game' view
            'Quit': blackmango.app.game_app.user_quit
        }
        self.menu_items = []

        self.selector = None

        self.title = MainMenuTitle('Black Mango', \
                batch = main_menu_batch)
        offset = 0
        for option in sorted(self.menu_options):
            action = self.menu_options[option]
            label = MainMenuLabel(option, offset, \
                    main_menu_batch)
            label.action = action
            self.menu_items.append(label)
            offset += 1

        self.selected = 0

    def on_draw(self):
        """
        Called on every window draw (unless the window isn't drawing views for
        some reason, like during loading of new games).
        """
        main_menu_batch.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called by the window on mouse clicks.
        """

    def tick(self, keyboard):
        """
        Called on every window tick
        """
        pass

class MainMenuTitle(pyglet.text.Label):

    def __init__(self, title, batch):

        x, y = blackmango.ui.game_window.get_size()

        super(MainMenuTitle, self).__init__(
            title,
            font_name = 'Chapbook',
            font_size = 52,
            x = x // 2,
            y = y - (y // 4),
            anchor_x = 'center',
            anchor_y = 'center',
            batch = batch,
            color = TITLE_COLOR,
        )

class MainMenuLabel(pyglet.text.Label):

    def __init__(self, title, offset = 0, batch = None):

        x, y = blackmango.ui.game_window.get_size()

        offset += 1
        offset *= .5

        super(MainMenuLabel, self).__init__(
            title,
            font_name = 'Prociono TT',
            font_size = 28, 
            x = x // 2,
            y = y // 2 - (y // 4)*offset,
            anchor_x = 'center',
            anchor_y = 'center',
            batch = batch,
            color = blackmango.ui.labels.TITLE_COLOR,
        )

