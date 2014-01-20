
import os
import pyglet

import blackmango.system
import blackmango.ui.views
import blackmango.ui.views.game
import blackmango.ui.views.main_menu

from blackmango.configure import COLORS

loading_menu_batch = pyglet.graphics.Batch()

TITLE_COLOR = COLORS['secondary-a-5']
MENU_ITEM_COLOR = COLORS['primary-4']
SELECTED_COLOR = COLORS['secondary-b-5']

class LoadGameView(blackmango.ui.views.BaseView):
    
    def __init__(self):

        savedir = blackmango.system.DIR_SAVEDGAMES
        savefiles = os.listdir(savedir)
        savefiles = filter(lambda x: x.endswith('.blackmango'), savefiles)

        self.menu_options = []
        for f in savefiles:
            self.menu_options.append((f[:-11], f))
        self.menu_items = []

        self.title = MenuTitle('Load game')
        offset = 0
        for option, s in self.menu_options:
            label = MenuLabel(option, offset)
            label.action = lambda : self.load_game(s)
            self.menu_items.append(label)
            offset += 1

        cancel = MenuLabel('Cancel', offset)
        cancel.action = self.cancel_action
        self.menu_items.append(cancel)

        self.selected = 0
        self.set_selected(0)

    def destroy(self):
        for i in self.menu_items:
            i.delete()
        self.title.delete()

    def load_game(self, savefile):
        from blackmango.ui.views.game import GameView
        blackmango.ui.game_window.set_view(GameView(savefile))

    def cancel_action(self):
        from blackmango.ui.views.main_menu import MainMenuView
        blackmango.ui.game_window.set_view(MainMenuView())
           
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
        loading_menu_batch.draw()

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

class MenuTitle(pyglet.text.Label):

    def __init__(self, title):

        x, y = blackmango.ui.game_window.get_size()

        super(MenuTitle, self).__init__(
            title,
            font_name = 'Chapbook',
            font_size = 52,
            x = x // 2,
            y = y - (y // 4),
            anchor_x = 'right',
            anchor_y = 'center',
            batch = loading_menu_batch,
            color = TITLE_COLOR,
        )

class MenuLabel(pyglet.text.Label):

    def __init__(self, title, offset = 0):

        x, y = blackmango.ui.game_window.get_size()

        offset += 1
        offset *= .5

        super(MenuLabel, self).__init__(
            title,
            font_name = 'Prociono TT',
            font_size = 18, 
            x = x - 140,
            y = y - 180 - 100*offset,
            anchor_x = 'right',
            anchor_y = 'top',
            batch = loading_menu_batch,
            color = MENU_ITEM_COLOR,
        )
