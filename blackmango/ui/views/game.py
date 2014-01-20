"""
Active view during gameplay.
"""

import cPickle
import datetime
import errno
import os
import pyglet

from pyglet.window import key

import blackmango.configure
import blackmango.levels
import blackmango.materials
import blackmango.mobs
import blackmango.mobs.player
import blackmango.system
import blackmango.ui

from blackmango.levels.levellist import LEVELS
from blackmango.ui.views import BaseView

def loading_halt(f):
    def wrapped(self, *args, **kwargs):
        if self.loading:
            return
        else:
            return f(self, *args, **kwargs)
    return wrapped

class GameView(BaseView):

    logger = blackmango.configure.logger

    def __init__(self, level = None):

        self.current_level = None
        self.player = None

        self.loading = False

        level_data = LEVELS.get(level)
        
        if level_data:
            self.logger.debug("Starting new game at level %s" % level)
            self.start_level(level_data)
        elif level.endswith('.blackmango'):
            self.logger.debug("Loading game from file %s" % level)
            self.load_level(level)
        else:
            raise ValueError("Invalid argument passed to GameView.__init__: %s"\
                                % level)

    def destroy(self):
        self.level_teardown()

    def level_teardown(self):
        if self.current_level:
            self.current_level.destroy()
            self.current_level = None

    @loading_halt
    def save_level(self, filepath = None):
        if not filepath:
            filepath = 'autosave.%s.blackmango' % str(datetime.datetime.now())
        self.loading = True
        stored_level = self.current_level.serialize(self.player)
        f = os.path.join(blackmango.system.DIR_SAVEDGAMES, filepath)
        d = os.path.dirname(f)
        self.logger.debug("Saving game: %s" % f)
        try:
            os.makedirs(d)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(d):
                pass
            else:
                raise
        with open(f, 'w') as fp:
            fp.write(blackmango.configure.SAVE_GAME_VERSION + '\n')
            fp.write(cPickle.dumps(stored_level))
        self.loading = False

    def load_level(self, filepath):
        self.loading = True
        self.logger.debug("Scheduling load game...")
        current_save_vesion = blackmango.configure.SAVE_GAME_VERSION

        def loader(dt):
            self.logger.debug("Loading game: %s" % filepath)
            with open(filepath) as f:
                version, _, leveldata = f.read().partition('\n')
                if version != current_save_vesion:
                    raise IOError("Version mismatch trying to load saved game"
                       " data: %s:%s" % (version, current_save_vesion))
                stored_level = cPickle.loads(leveldata)
            self.start_level(stored_level)

        # Don't load the next level until the current update has completed
        # (otherwise Pyglet will barf when you start to tear down Sprites that
        # it is in the middle of updating).
        pyglet.clock.schedule_once(loader, 1)

    def start_level(self, level_data):

        self.loading = True
        self.level_teardown()

        # Initialize level and player
        self.current_level = blackmango.levels.BasicLevel(level_data)
        self.player = blackmango.mobs.player.Player()

        # Place the player into the level
        starting_location = self.current_level.starting_location
        self.current_level.set_mob(self.player, *starting_location)
        self.player.world_location = starting_location
        self.player.translate()

        self.loading = False
        self.logger.debug("Game started: %s" % repr(self.current_level))

    def next_level(self):
        self.loading = True
        def loader(dt):
            next_level_str = self.current_level.next_level
            self.logger.debug("Loading next level: %s" % next_level_str)
            level_data = LEVELS.get(self.current_level.next_level)
            self.start_level(level_data)
        # Don't load the next level until the current update has completed
        # (otherwise Pyglet will barf when you start to tear down Sprites that
        # it is in the middle of updating).
        pyglet.clock.schedule_once(loader, 1)

    def quit_to_main_menu(self):
        self.loading = True
        def loader(dt):
            from blackmango.ui.views.main_menu import MainMenuView
            blackmango.ui.game_window.set_view(MainMenuView())
        # Don't load the next level until the current update has completed
        # (otherwise Pyglet will barf when you start to tear down Sprites that
        # it is in the middle of updating).
        pyglet.clock.schedule_once(loader, 1)

    @loading_halt
    def on_draw(self):
        """
        Called on every window draw (unless the window isn't drawing views for
        some reason, like during loading of new games).
        """
        blackmango.materials.materials_batch.draw()
        blackmango.mobs.mobs_batch.draw()

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
    def on_key_press(self, key, modifiers, keyboard):
        """
        Called by the window on every key press
        """
        pass

    @loading_halt
    def tick(self, keyboard):
        """
        Called on every window tick
        """
        # The order of these things may need adjustment at some point
        self.player.user_input(keyboard, self.current_level)

        # View-level actions. These should go into some sort of overlay menu
        # that pauses the game when active.
        if keyboard[key.S]:
            self.save_level()
        elif keyboard[key.L]:
            self.load_level()
        elif keyboard[key.ESCAPE]:
            self.quit_to_main_menu()

        if self.current_level:
            self.current_level.tick(self.player)
