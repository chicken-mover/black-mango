
import pyglet

import blackmango.ui
import blackmango.ui.views

# This should eventually contain a complete set of acknowledgements for all of
# the open-source bits and pieces used in the project.

import pyglet

import blackmango.ui
import blackmango.ui.views

# This should eventually contain a complete set of acknowledgements for all of
# the open-source bits and pieces used in the project.
CREDITS = """
<br>
<br>
<br>
<br>
<br>
<br>
<center>
    <font color="#FFFFFF" face="Chapbook" size="+4">
        Black Mango
    </font>
    <br>
    <font color="white" face="Prociono TT" size="+1">
        Copyright &copy;2014 Chicken Mover
        <br>
        <br>
        ...
        <br>
        <br>
        ...
        <br>
        <br>
        ...
        <br>
        <br>
        ...
    </font>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
</center>
"""

credits_batch = pyglet.graphics.Batch()

class CreditsView(blackmango.ui.views.BaseView):

    def __init__(self):
        
        x, y = blackmango.ui.game_window.get_size()

        document = pyglet.text.decode_html(CREDITS)
        document.color = (255,255,255,255)
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
        """
        Called on every window draw (unless the window isn't drawing views for
        some reason, like during loading of new games).
        """
        credits_batch.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        self.back_to_main_menu()

    def on_mouse_motion(self, x, y, dx, dy):
        """
        Called by the window during mouse movement.
        """
        pass

    def on_key_press(self, key, modifiers, keyboard):
        self.back_to_main_menu()

    def back_to_main_menu(self):
        blackmango.ui.game_window.set_view(
                blackmango.ui.views.main_menu.MainMenu())

    def tick(self, keyboard):
        """
        Called on every window tick
        """
        pass
