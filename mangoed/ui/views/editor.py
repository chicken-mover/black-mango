
import cPickle
import datetime
import errno
import os
import pyglet

from pyglet.window import key
from pyglet.window import mouse

import blackmango.levels
import blackmango.materials
import blackmango.mobs
import blackmango.mobs.player
import blackmango.sprites
import blackmango.system
import mangoed.app
import mangoed.configure
import mangoed.lib
import mangoed.sprites
import mangoed.ui

from blackmango.blocks.blocklist import BLOCKS
from blackmango.levels.levellist import LEVELS
from blackmango.mobs.moblist import MOBS
from mangoed.ui.views import BaseView

MODE_SELECT = 'SELECT_ED'
MODE_BLOCK = 'BLOCK_ED'
MODE_MOB = 'MOB_ED'

SECONDARY_MODE_START = 'SECONDARY_MODE_START'

class EditorView(BaseView):

    logger = mangoed.configure.logger

    def __init__(self, level = None):

        self.current_level = None
        self.player = None

        self.mode = MODE_SELECT
        self.secondary_mode = None
        self.secondary_mode_buffer = ''
        
        self.background_image = None
        self.background = None

        level = mangoed.lib.name_cleanup(level)
        self.level_ref = level
        level_data = LEVELS.get(level)
        
        self.batch = pyglet.graphics.Batch()
        self.cursor = mangoed.sprites.GridCursor()
        self.cursorinfo = CursorInfo(repr(self.cursor.world_location),
            self.batch)

        if level_data:
            self.logger.debug("Editing level: %s" % level)
            self.load_level(level_data)
        else:
            self.logger.debug("New level: %s" % level)
            self.new_level()

    def new_level(self):
        level = blackmango.levels.SavedLevel()
        self.load_level(level)

    def load_level(self, leveldata):
        self.current_level = blackmango.levels.BasicLevel(leveldata)

    def save_level(self):
        serialized_data = self.current_level.serialize()
        dir = os.dirpath(blackmango.levels.__file__)
        dir = os.path.join(dir, self.level_ref)
        with open(os.path.join(dir, '__init__.py'), 'w') as f:
            f.write(serialized_data)
        triggers = os.path.join(dir, 'triggers.py')
        if not os.path.exists(triggers):
            with open(triggers, 'w') as f:
                f.write(mangoed.configure.TRIGGER_TEMPLATE)

    def switch_floor(self, floor):
        self.current_level.switch_floor(floor)

    def quit(self):
        mangoed.app.app.user_quit()

    def clear_selections(self):
        self.secondary_mode = None
        self.secondary_mode_buffer = ''
        self.selected_key = None
        print "Selections cleared."

    def set_mode(self, mode):
        self.clear_selections()
        self.mode = mode
        print "Mode set:", mode

    def select_action(self):
        try:
            k = int(self.secondary_mode_buffer)
        except ValueError:
            print 'Not an integer:', self.secondary_mode_buffer
            return
        finally:
            self.secondary_mode_buffer = ''
            
        self.selected_key = k
        if self.mode == MODE_BLOCK:
            if k in BLOCKS:
                print "Selected block:", repr(BLOCKS[k])
            else:
                print "No such block:", k
                self.selected_key = None
        elif self.mode == MODE_MOB:
            if k in MOBS:
                print "Selected mob:", repr(MOBS[k])
            else:
                print "No such mob:", k
                self.selected_key = None
        elif self.mode == MODE_SELECT:
            self.switch_floor(k)

    def select_existing(self, x, y, z):
        if self.mode == MODE_SELECT:
            sel = self.current_level.get_mob(x, y, z)
            if sel:
                self.set_mode(MODE_MOB)
            else:
                sel = self.current_level.get_block(x, y, z)
                if self:
                    self.set_mode(MODE_BLOCK)
        elif self.mode == MODE_BLOCK:
            sel = self.current_level.get_block(x, y, z)
        elif self.mode == MODE_MOB:
            sel = self.current_level.get_mob(x, y, z)
        for d in (BLOCKS, MOBS):
            for k, v in d.items():
                if isinstance(sel, v):
                    self.selected_key = k
            

    def delete_existing(self, x, y, z):
        if self.mode == MODE_BLOCK:
            b = self.current_level.get_block(*coords)
            self.current_level.unset_block(*coords)
            b.delete()
        elif self.mode == MODE_MOB:
            m = self.current_level.get_mob(*coords)
            self.current_level.unset_mob(*coords)
            m.delete()

    def edit_obj(self, obj):
        args = ()
        kwargs = {}

        # Blocks!
        if isinstance(obj, blackmango.materials.BasePortalMaterial):
            try:
                inp = input('Enter the portal destinaton (x, y, z):')
                inp = tuple([int(i) for i in inp])
            except SyntaxError, ValueError, TypeError as e:
                print e
                print 'Invalid input, detination not set.'
                return
            kwargs.update({'destination': inp})
        elif isinstance(obj, blackmango.materials.BaseMaterial):
            print "Nothing to edit."

        # Mobs!
        elif isinstance(obj, blackmango.sprites.BasicMobileSprite):
            try:
                inp = input('Enter the direction the mob faces (1,2,3,4) [3]:')
                inp = int(inp)
            except SyntaxError, ValueError as e:
                print e
                print '(Direction set to default, 3)'
                inp = 3
            kwargs.update({'direction': inp})
        else:
            print "Nothing to edit."
            return

        coords = obj.world_location
        cls = obj.__class__
        obj.delete()
        # Replace it
        obj = cls(*args, **kwargs)
        if self.mode = MODE_BLOCK:
            self.current_level.set_block(obj, *coords)
        elif self.mode = MODE_MOB:
            self.current_level.set_mob(obj, *mob)

    def on_draw(self):
        """
        Called on every window draw (unless the window isn't drawing views for
        some reason, like during loading of new games).
        """
        background = self.current_level.get_background()
        if background:
            background.draw()
        blackmango.sprites.sprite_batch.draw()
        self.batch.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called by the window on mouse clicks.
        """
        if button == mouse.LEFT:
            self.select_existing(*self.cursor.world_location)

    def on_mouse_motion(self, x, y, dx, dy):
        """
        Called by the window during mouse movement.
        """
        self.cursor.untranslate(x, y)
        self.cursorinfo.text = repr(self.cursor.world_location)

    def on_key_press(self, keypress, modifiers):
        """
        Called by the window on every key press
        """

        # Mode switching
        if keypress == key.ESCAPE:
            if self.secondary_mode == SECONDARY_MODE_START:
                self.clear_selections
                self.secondary_mode = None
            else:
                self.set_mode(MODE_SELECT)
        elif keypress == key.M:
            self.set_mode(MODE_MOB)
        elif keypress == key.B:
            self.set_mode(MODE_BLOCK)

        # Save and quit
        elif keypress == key.Q:
            self.quit()
        elif keypress == key.W:
            self.save_level()

        # Delete and select
        elif keypress == key.E:
            self.select_existing(*self.cursor.world_location)
        elif keypress in [key.DELETE, key.BACKSPACE]:
            self.delete_existing(*self.cursor.world_location)

        # Handle block selection sequences or floor switching sequences
        elif keypress == key.COLON and self.seconary_mode is None:
            self.secondary_mode = SECONDARY_MODE_START
        elif keypress in [key.ENTER, key.NUM_ENTER] and \
            self.secondary_mode == SECONDARY_MODE_START:
            self.secondary_mode = None
            self.select_action()
        elif self.secondary_mode == SECONDARY_MODE_START:
            self.secondary_mode_buffer += key.symbol_string(keypress)

class CursorInfo(pyglet.text.Label):

    def __init__(self, text, batch):
        _win_x, _win_y = mangoed.ui.editor_window.get_size()
        super(CursorInfo, self).__init__(
            text,
            font_size = 15,
            x = _win_x - 50,
            y = 50,
            anchor_x = 'left',
            anchor_y = 'bottom',
            batch = batch,
            color = (255,255,255,150)
        )
