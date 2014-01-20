"""
Initial title menu view
"""

import pyglet

import blackmango.app
import blackmango.configure
import blackmango.engine
import blackmango.ui.views
import blackmango.ui.views.credits
import blackmango.ui.views.game
import blackmango.ui.views.load_game

main_menu_batch = pyglet.graphics.Batch()

TITLE_COLOR = (110, 25, 71, 255)
MENU_ITEM_COLOR = (80, 30, 102, 255)
SELECTED_COLOR = (86, 117, 26, 255)

class MainMenu(blackmango.ui.views.BaseView):
    
    def __init__(self):
        
        self.menu_options = [
            ('New game', self.new_game_action),
            ('Load game', self.load_game_action),
            ('Options & controls', None),
            ('Credits', lambda : blackmango.ui.game_window.set_view(
                    blackmango.ui.views.credits.CreditsView()
                )),
            ('Quit', blackmango.app.game_app.user_quit),
        ]
        self.menu_items = []

        self.title = MainMenuTitle('Black Mango', main_menu_batch)
        self.versioninfo = VersionInfo(blackmango.configure.VERSION)
        offset = 0
        for option, action in self.menu_options:
            label = MainMenuLabel(option, offset, main_menu_batch)
            label.action = action
            self.menu_items.append(label)
            offset += 1

        self.selected = 0
        self.set_selected(0)

    def new_game_action(self):
        blackmango.ui.game_window.set_view(
            blackmango.ui.views.game.GameView('new')        
        )

    def load_game_action(self):
        blackmango.ui.game_window.set_view(
            blackmango.ui.views.load_game.LoadGameView()        
        )

    def destroy(self):
        for i in self.menu_items:
            i.delete()
        self.title.delete()
        self.versioninfo.delete()

    def set_selected(self, i):
        self.menu_items[self.selected].color = MENU_ITEM_COLOR
        self.selected = i
        if i > -1:
            self.menu_items[i].color = SELECTED_COLOR

    def select_next(self):
        s = self.selected
        s += 1
        if s > len(self.menu_items) - 1:
            s = 0
        self.set_selected(s)

    def select_prev(self):
        s = self.selected
        s -= 1
        if s < 0:
            s = len(self.menu_items) - 1
        self.set_selected(s)

    def on_draw(self):
        main_menu_batch.draw()

    def get_intersecting_menu_item(self, x, y):
        # If the mouse intersects with any menu items, select them
        for idx, item in enumerate(self.menu_items):
            # Assuming menu items are top- and right-anchored, but if that 
            # changes then we need to change this line
            if x < item.x + 1 and x > item.x - item.content_width - 1 and \
               y < item.y + 1 and y > item.y - item.content_height - 1:
                return idx, item
        else:
            return -1, None

    def on_mouse_motion(self, x, y, dx, dy):
        idx, item = self.get_intersecting_menu_item(x, y)
        if item:
            self.set_selected(idx)
        return

    def on_mouse_press(self, x, y, button, modifiers):
        idx, item = self.get_intersecting_menu_item(x, y)
        if button == 1 and item:
            item.action()

    def tick(self, keyboard):
        pass

    def on_key_press(self, key, modifiers, keyboard):
        
        if keyboard[pyglet.window.key.UP] or \
           keyboard[pyglet.window.key.W] or \
           keyboard[pyglet.window.key.LEFT] or \
           keyboard[pyglet.window.key.A]:
            self.select_prev()
        
        elif keyboard[pyglet.window.key.DOWN] or \
           keyboard[pyglet.window.key.RIGHT] or \
           keyboard[pyglet.window.key.S] or \
           keyboard[pyglet.window.key.D]:
            self.select_next()

        elif keyboard[pyglet.window.key.ENTER]:
            self.menu_items[self.selected].action()

class MainMenuTitle(pyglet.text.Label):

    def __init__(self, title, batch):

        x, y = blackmango.ui.game_window.get_size()

        super(MainMenuTitle, self).__init__(
            title,
            font_name = 'Chapbook',
            font_size = 52,
            x = x // 2,
            y = y - (y // 4),
            anchor_x = 'right',
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
            #font_name = 'Prociono TT',
            font_name = 'Chapbook',
            font_size = 18, 
            x = x - 140,
            y = y - 180 - 100*offset,
            anchor_x = 'right',
            anchor_y = 'top',
            batch = batch,
            color = MENU_ITEM_COLOR,
        )

class VersionInfo(pyglet.text.Label):

    def __init__(self, title):
        x, y = blackmango.ui.game_window.get_size()
        super(VersionInfo, self).__init__(
            'v-%s' % title,
            font_name = 'Prociono TT',
            font_size = 8,
            x = x - 20,
            y = 25,
            anchor_x = 'right',
            anchor_y = 'top',
            batch = main_menu_batch,
            color = (255,255,255,50)
        )
