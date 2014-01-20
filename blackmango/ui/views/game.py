
import cPickle
import errno
import os

from pyglet.window import key

import blackmango.configure
import blackmango.levels
import blackmango.materials
import blackmango.mobs
import blackmango.mobs.player
import blackmango.system
import blackmango.ui

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

        if level == 'new':
            import blackmango.levels.test_level
            self.logger.debug("Starting new game...")
            self.start_game(
                    blackmango.levels.test_level.LEVEL_DATA)
        elif level.endswith('.blackmango'):
            self.load_game(level)
        else:
            raise ValueError("Invalid argument passed to GameView.__init__: %s"\
                                % level)

    def destroy(self):
        self.game_teardown()

    def game_teardown(self):
        if self.current_level:
            self.current_level.destroy()
            self.current_level = None
        # Clean up the player if it wasn't cleaned up by the level teardown.
        if self.player and hasattr(self.player, 'delete'):
            self.player.delete()

    def save_game(self, filepath = 'autosave.blackmango'):
        stored_level = self.current_level.serialize(self.player)
        f = os.path.join(blackmango.system.DIR_SAVEDGAMES, filepath)
        d = os.path.dirname(f)
        self.logger.debug("Saving game: %s" % f)
        try:
            os.makedirs(d)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(dir):
                pass
            else:
                raise
        with open(f, 'w') as fp:
            fp.write(blackmango.configure.SAVE_GAME_VERSION + '\n')
            fp.write(cPickle.dumps(stored_level))
        return True

    def load_game(self, filepath = 'autosave.blackmango'):
        self.loading = True
        self.logger.debug("Scheduling load game...")
        current_save_vesion = blackmango.configure.SAVE_GAME_VERSION

        def loader(dt):
            file = os.path.join(blackmango.system.DIR_SAVEDGAMES, filepath)
            self.logger.debug("Loading game: %s" % file)
            with open(file) as f:
                version, _, leveldata = f.read().partition('\n')
                if version != current_save_vesion:
                    raise IOError("Version mismatch trying to load saved game"
                       " data: %s:%s" % (version, current_save_vesion))
                stored_level = cPickle.loads(leveldata)
            self.loading = False
            self.start_game(stored_level)

        # Don't load the next level until the current update has completed
        # (otherwise Pyglet will barf when you start to tear down Sprites that
        # it is in the middle of updating).
        pyglet.clock.schedule_once(loader, 1)

    def start_game(self, level_data):

        self.loading = True
        self.game_teardown()

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
            self.save_game()
        elif keyboard[key.L]:
            self.load_game()
        elif keyboard[key.ESC]:
            from blackmango.ui.views.main_menu import MainMenuView
            blackmango.ui.game_window.set_view(MainMenuView())

        if self.current_level:
            self.current_level.tick()