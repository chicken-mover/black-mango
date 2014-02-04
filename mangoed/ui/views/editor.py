"""
The main editor view. At present, the editor only has the one view class, since
it's pretty bare bones.
"""

import errno
import os
import pyglet
import traceback

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

from blackmango.materials.materiallist import MATERIALS
from blackmango.levels.levellist import LEVELS
from blackmango.mobs.moblist import MOBS
from blackmango.ui.views import BaseView

MODE_SELECT = 'SELECT_ED'
MODE_MATERIAL = 'MATERIAL_ED'
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

    def load(self):
        level_data = LEVELS.get(self.level_ref)
        
        self.batch = pyglet.graphics.Batch()
        self.cursor = mangoed.sprites.GridCursor()
        self.cursorinfo = CursorInfo(repr(self.cursor.world_location),
            self.batch)

        if level_data:
            self.logger.debug("Editing level: %s" % self.level_ref)
            self.load_level(level_data)
        else:
            self.logger.debug("New level: %s" % self.level_ref)
            self.new_level()

    def new_level(self):
        """
        Create a new empty level
        """
        level = blackmango.levels.SavedLevel()
        self.load_level(level)

    def load_level(self, leveldata):
        """
        Load an existing level from the main Black Mango source tree.
        """
        leveldata.LEVEL_NAME = self.level_ref
        self.current_level = blackmango.levels.BasicLevel(leveldata)
        self.current_level.load()

    def save_level(self):
        """
        Write a level directly to the Black Mango source tree.
        """
        serialized_data = self.current_level.serialize()
        dir = os.path.dirname(blackmango.levels.__file__)
        dir = os.path.join(dir, self.level_ref)
        try:
            os.makedirs(dir)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        with open(os.path.join(dir, '__init__.py'), 'w') as f:
            f.write(serialized_data)
        triggers = os.path.join(dir, 'triggers.py')
        if not os.path.exists(triggers):
            with open(triggers, 'w') as f:
                f.write(mangoed.configure.TRIGGER_TEMPLATE)
        print "Wrote level:", self.level_ref

    def switch_room(self, room):
        """
        Switch the view to another room/room
        """
        self.current_level.switch_room(room)

    def quit(self):
        """
        Quit the app (calls mangoed.app.app.user_quit())
        """
        mangoed.app.app.user_quit()

    def clear_selections(self):
        """
        Clear all selections and buffers
        """
        self.secondary_mode = None
        self.secondary_mode_buffer = ''
        self.selected_key = None
        print "Selections cleared."

    def set_mode(self, mode):
        """
        Set the mod and clear the selections of the current mode
        """
        self.clear_selections()
        self.mode = mode
        print "Mode set:", mode

    def select_action(self):
        """
        Depending on the mode, select a material/mob for placement, or switch room
        view.
        """
        try:
            k = int(self.secondary_mode_buffer)
        except ValueError:
            print 'Not an integer:', self.secondary_mode_buffer
            return
        finally:
            self.secondary_mode_buffer = ''
            
        self.selected_key = k
        if self.mode == MODE_MATERIAL:
            if k in MATERIALS:
                print "Selected material:", repr(MATERIALS[k])
            else:
                print "No such material:", k
                self.selected_key = None
        elif self.mode == MODE_MOB:
            if k in MOBS:
                print "Selected mob:", repr(MOBS[k])
            else:
                print "No such mob:", k
                self.selected_key = None
        elif self.mode == MODE_SELECT:
            self.switch_room(k)

    def select_existing(self, x, y, z):
        """
        Select an existing material or mob out of the specified coordinates,
        depending on which mode we are in.
        """
        sel = None
        if self.mode == MODE_SELECT:
            _, sel = self.current_level.get_sprites((x, y, z))
            if sel:
                self.set_mode(MODE_MOB)
            else:
                sel, _ = self.current_level.get_sprites((x, y, z))
                if self:
                    self.set_mode(MODE_MATERIAL)
        elif self.mode == MODE_MATERIAL:
            sel, _ = self.current_level.get_sprites((x, y, z))
        elif self.mode == MODE_MOB:
            _, sel = self.current_level.get_sprites((x, y, z))
        for d in (MATERIALS, MOBS):
            for k, v in d.items():
                if v and isinstance(sel, v):
                    self.selected_key = k
        return sel
            

    def delete_existing(self, x, y, z):
        """
        Depending on the mode, delete an existing material or mob from the
        specified grid square.
        """
        if self.mode == MODE_MATERIAL:
            b, _ = self.current_level.get_sprites((x, y, z))
            b.delete()
        elif self.mode == MODE_MOB:
            _, m = self.current_level.get_sprites((x, y, z))
            m.delete()

    def edit_obj(self, obj):
        """
        'Edit' a selected object by replacing it with another version of the
        same.
        """
        args, kwargs = obj._args, obj._kwargs 

        # materials!
        if isinstance(obj, blackmango.materials.BasePortalMaterial):
            try:
                inp = input('Enter the portal destinaton (x, y, z):')
                inp = tuple([int(i) for i in inp])
            except Exception as e:
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
            except Exception as e:
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
        if self.mode == MODE_MATERIAL:
            self.current_level.set_sprite(obj, coords)
        elif self.mode == MODE_MOB:
            self.current_level.set_sprite(obj, coords)

    def on_draw(self):
        """
        Performs the requisite draw operations delegated from the EditorWindow
        class
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
        cx, cy = self.cursor.world_location[:2]
        if button == mouse.LEFT:
            sel = self.select_existing(*self.cursor.world_location)
            if self.selected_key and not sel:
                if self.mode == MODE_MATERIAL:
                    d = MATERIALS
                elif self.mode == MODE_MOB:
                    d = MOBS
                try:
                    m = d[self.selected_key]()
                    coords = (cx, cy, self.current_level.current_room)
                    self.current_level.set_sprite(m, coords)
                    print 'Placed %s' % m
                except:
                    print traceback.format_exc()
            else:
                print 'Nothing selected to place'


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
            self.set_mode(MODE_MATERIAL)

        # Save and quit
        elif keypress == key.Q:
            self.quit()
        elif keypress == key.W:
            self.save_level()

        # Delete and select
        elif keypress == key.E:
            sel = self.select_existing(*self.cursor.world_location)
            if sel:
                self.edit_obj(sel)
        elif keypress in [key.DELETE, key.BACKSPACE]:
            self.delete_existing(*self.cursor.world_location)

        # Handle material selection sequences or room switching sequences
        elif keypress in [key.COLON, key.SEMICOLON] and self.secondary_mode is None:
            self.secondary_mode = SECONDARY_MODE_START
            print "(bufopen)"
        elif keypress in [key.ENTER, key.NUM_ENTER] and \
            self.secondary_mode == SECONDARY_MODE_START:
            self.secondary_mode = None
            print self.secondary_mode_buffer
            self.select_action()
        elif self.secondary_mode == SECONDARY_MODE_START:
            self.secondary_mode_buffer += key.symbol_string(keypress).strip('_')

class CursorInfo(pyglet.text.Label):

    def __init__(self, text, batch):
        super(CursorInfo, self).__init__(
            text,
            font_size = 15,
            x = 50,
            y = 50,
            anchor_x = 'left',
            anchor_y = 'bottom',
            batch = batch,
            color = (255,255,255,150)
        )
