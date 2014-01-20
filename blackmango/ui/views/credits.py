
import pyglet

import blackmango.assetloader
import blackmango.ui

from blackmango.ui.views import BaseView

credits_batch = pyglet.graphics.Batch()

class CreditsView(BaseView):

    def __init__(self):
        
        x, y = blackmango.ui.game_window.get_size()

        text = blackmango.assetloader.load_text('credits.html')
        document = pyglet.text.decode_html(text)
        self.layout = pyglet.text.layout.ScrollableTextLayout(document,
                width = x//3 * 2,
                height = y,
                batch = credits_batch,
                multiline = True)
        self.layout.x, self.layout.y = x//2, y//2
        self.layout.anchor_x, self.layout.anchor_y = 'center', 'center'

        self.delta = 0
        pyglet.clock.schedule_once(lambda dt: \
                pyglet.clock.schedule(self.scroll), 1)

    def destroy(self):
        pyglet.clock.unschedule(self.scroll)
        self.layout.delete()

    def scroll(self, dt):
        #print self.delta
        self.delta += dt
        if self.delta > .05:
            self.layout.view_y -= 1
            self.delta -= .05

    def on_draw(self):
        credits_batch.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        self.back_to_main_menu()

    def on_key_press(self, key, modifiers, keyboard):
        self.back_to_main_menu()

    def back_to_main_menu(self):
        from blackmango.ui.views.main_menu import MainMenuView
        blackmango.ui.game_window.set_view(MainMenuView())
