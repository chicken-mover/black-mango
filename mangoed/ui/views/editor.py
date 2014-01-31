"""
Active view during gameplay.
"""

import cPickle
import datetime
import errno
import os
import pyglet

import blackmango.levels
import blackmango.materials
import blackmango.mobs
import blackmango.mobs.player
import blackmango.sprites
import blackmango.system
import mangoed.ui
import mangoed.configure

from blackmango.levels.levellist import LEVELS
from mangoed.ui import keyboard
from mangoed.ui.views import BaseView

MODE_LOADING = 'MODE_LOADING'
MODE_NORMAL = 'MODE_NORMAL'
MODE_PAUSE = 'MODE_PAUSE'

def loading_halt(f):
    def wrapped(self, *args, **kwargs):
        if self.mode == MODE_LOADING:
            return
        else:
            return f(self, *args, **kwargs)
    return wrapped

class GameView(BaseView):

    logger = mangoed.configure.logger

    def __init__(self, level = None):

        self.current_level = None
        self.player = None

        self.mode = MODE_NORMAL
        self.background_image = None
        self.background = None

        level_data = LEVELS.get(level)

        if level_data:
            self.logger.debug("Editing level: %s" % level)
            self.start_level(level_data)
        else:
            self.logger.debug("New level.")
            self.new_level()

    def destroy(self):
        self.level_teardown()

    def level_teardown(self):
        if self.current_level:
            self.current_level.destroy()
            self.current_level = None

    def new_level(self):
        """
        Create a new level
        """
        pass

    @loading_halt
    def save_level(self, filepath = None):
        """
        Save an edited level to a file
        """
#        if not filepath:
#            filepath = 'autosave.%s.blackmango' % str(datetime.datetime.now())
#        self.mode = MODE_LOADING
#        stored_level = self.current_level.serialize()
#        f = os.path.join(blackmango.system.DIR_SAVEDGAMES, filepath)
#        d = os.path.dirname(f)
#        self.logger.debug("Saving game: %s" % f)
#        try:
#            os.makedirs(d)
#        except OSError as exc:
#            if exc.errno == errno.EEXIST and os.path.isdir(d):
#                pass
#            else:
#                raise
#        with open(f, 'w') as fp:
#            fp.write(mangoed.configure.SAVE_GAME_VERSION + '\n')
#            fp.write(cPickle.dumps(stored_level))
#        self.loading = MODE_PAUSE

    def load_level(self, filepath):
        """
        Load a level for editing
        """
#        self.mode = MODE_LOADING
#        self.logger.debug("Scheduling load game...")
#        current_save_vesion = mangoed.configure.SAVE_GAME_VERSION
#
#        def loader(dt):
#            self.logger.debug("Loading game: %s" % filepath)
#            with open(filepath) as f:
#                version, _, leveldata = f.read().partition('\n')
#                if version != current_save_vesion:
#                    raise IOError("Version mismatch trying to load saved game"
#                       " data: %s:%s" % (version, current_save_vesion))
#                stored_level = cPickle.loads(leveldata)
#            self.start_level(stored_level)
#
#        # Don't load the next level until the current update has completed
#        # (otherwise Pyglet will barf when you start to tear down Sprites that
#        # it is in the middle of updating).
#        pyglet.clock.schedule_once(loader, 1)

    def start_level(self, level_data):
        """
        Start editing
        """
#
#        self.mode = MODE_LOADING
#        self.level_teardown()
#
#        # Initialize level and player
#        self.player = blackmango.mobs.player.Player()
#        self.current_level = blackmango.levels.BasicLevel(level_data, \
#                                self.player)
#
#        # Place the player into the level
#        starting_location = self.current_level.starting_location
#        self.current_level.set_mob(self.player, *starting_location)
#        self.player.world_location = starting_location
#        self.player.translate()
#
#        self.mode = MODE_NORMAL
#        self.logger.debug("Game started: %s" % repr(self.current_level))

    @loading_halt
    def on_draw(self):
        """
        Called on every window draw (unless the window isn't drawing views for
        some reason, like during loading of new games).
        """
        background = self.current_level.get_background()
        if background:
            background.draw()
        blackmango.sprites.sprite_batch.draw()

    @loading_halt
    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called by the window on mouse clicks.
        """
        pass

    @loading_halt
    def on_mouse_motion(self, x, y, dx, dy):
        """
        Called by the window during mouse movement.
        """
        pass

    @loading_halt
    def on_key_press(self, key, modifiers):
        """
        Called by the window on every key press
        """
        pass

    @loading_halt
    def tick(self):
        """
        Called on every window tick
        """
#        if self.player.dead:
#            return self.quit_to_main_menu()
#
#        # The order of these things may need adjustment at some point
#        if self.mode == MODE_NORMAL:
#            self.player.tick()
#
#        if self.current_level and self.mode == MODE_NORMAL:
#            self.current_level.tick()
#
#        # View-level actions. These should go into some sort of overlay menu
#        # that pauses the game when active.
#        if keyboard.check('game_save'):
#            self.save_level()
#            self.mode = MODE_NORMAL
#        elif keyboard.check('game_load'):
#            self.load_level()
#        elif keyboard.check('game_quit'):
#            self.quit_to_main_menu()
#
#        return
