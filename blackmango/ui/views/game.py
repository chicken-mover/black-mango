"""
Active view during gameplay.
"""

import cPickle
import datetime
import errno
import os
import pyglet

import blackmango.configure
import blackmango.levels
import blackmango.materials
import blackmango.mobs
import blackmango.mobs.player
import blackmango.sprites
import blackmango.system
import blackmango.ui
import blackmango.ui.keyboard as keyboard
import blackmango.ui.labels

from blackmango.levels.levellist import LEVELS
from blackmango.ui import keyboard
from blackmango.ui.views import BaseView

TITLE_CARD_COLOR = blackmango.configure.COLORS['secondary-a-5']

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

    logger = blackmango.configure.logger

    def __init__(self, level = None):

        self.current_level = None
        self.player = None

        self.mode = MODE_NORMAL
        self.background_image = None
        self.background = None

        self.level = level

    def load(self):

        level_data = blackmango.levels.load(self.level)
        
        if level_data:
            self.logger.debug("Starting new game at level %s" % self.level)
            self.start_level(level_data)
        elif self.level.endswith('.blackmango'):
            self.logger.debug("Loading game from file %s" % self.level)
            self.load_level(self.level)
        else:
            raise ValueError("Invalid argument passed to GameView.__init__: %s"\
                                % self.level)

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
        self.mode = MODE_LOADING
        stored_level = self.current_level.serialize()
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
        self.loading = MODE_PAUSE

    def load_level(self, filepath):
        self.mode = MODE_LOADING
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

        self.mode = MODE_LOADING
        self.level_teardown()

        # Initialize level and player
        self.player = blackmango.mobs.player.Player()
        self.current_level = blackmango.levels.BasicLevel(level_data, \
                                self.player)
        self.current_level.load()

        # Place the player into the level
        starting_location = level_data.PLAYER_START
        self.current_level.set_sprite(self.player, starting_location)
        # Set initial screen centering on player
        blackmango.sprites.current_translation_offset = tuple(starting_location[:2])

        self.mode = MODE_NORMAL
        self.logger.debug("Game started: %s" % repr(self.current_level))

        # Show the title card
        self.title_card = blackmango.ui.labels.TextBox(
            level_data.NAME,
            box_color = (0,0,0,255),
            text_color = TITLE_CARD_COLOR,
        )
        pyglet.clock.schedule_once(lambda dt: self.title_card.delete(), 2)


    def next_level(self):
        self.mode = MODE_LOADING
        def loader(dt):
            next_level_str = self.current_level.next_level
            self.logger.debug("Loading next level: %s" % next_level_str)
            level_data = blackmango.levels.load(next_level_str)
            self.start_level(level_data)
        # Don't load the next level until the current update has completed
        # (otherwise Pyglet will barf when you start to tear down Sprites that
        # it is in the middle of updating).
        pyglet.clock.schedule_once(loader, 1)

    def quit_to_main_menu(self):
        self.mode = MODE_LOADING
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

        # Make sure all sprites update thier screen coordinates.
        all_sprites = self.current_level.mobs.values() + \
                      self.current_level.blocks.values()
        for sprite in all_sprites:
            # Only update sprites in the current room, because none of the other
            # ones are visible.
            if sprite.world_location[2] == self.current_level.current_room:
                sprite.translate()

        # The background is blitted seperately, first. In the future if this
        # can be worked into one of the existing batches, that would be ideal.
        background = self.current_level.get_background()
        if background:
            # The background position has to be adjusted along with the window
            # scroll effect. It is only adjusted the minimal amount (the value
            # of the offset modulo the dimensions of the image) to keep the
            # movement smooth.
            background.draw(blackmango.sprites.current_translation_offset)

        # Draw everything else using the batches.
        blackmango.sprites.sprite_batch.draw()
        if self.title_card:
            blackmango.ui.labels.title_batch.draw()

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
        move = [0,0]
        if keyboard.check('move_up'):
            move[1] = -1
        elif keyboard.check('move_down'):
            move[1] = 1
        # Enable diagonals: change this 'elif' to 'if'
        elif keyboard.check('move_left'):
            move[0] = -1
        elif keyboard.check('move_right'):
            move[0] = 1

        elif keyboard.check('switch_mask_1'):
            self.player.activate_mask(1)
        elif keyboard.check('switch_mask_2'):
            self.player.activate_mask(2)
        elif keyboard.check('switch_mask_3'):
            self.player.activate_mask(3)
        elif keyboard.check('switch_mask_4'):
            self.player.activate_mask(4)

        if move != [0,0]:
            self.player.move(*move)

    @loading_halt
    def center_view_on_player(self):
        """
        Re-center the view on the player, if it has moved out into the middle
        of the room, and the room is larger than the screen view.
        """
        

    @loading_halt
    def tick(self):
        """
        Called on every window tick
        """
        if self.player.dead:
            return self.quit_to_main_menu()
            
        # The order of these things may need adjustment at some point
        if self.mode == MODE_NORMAL:
            self.player.tick()

        if self.current_level and self.mode == MODE_NORMAL:
            self.current_level.tick()

        # View-level actions. These should go into some sort of overlay menu
        # that pauses the game when active.
        if keyboard.check('game_save'):
            self.save_level()
            self.mode = MODE_NORMAL
        elif keyboard.check('game_load'):
            self.load_level()
        elif keyboard.check('game_quit'):
            self.quit_to_main_menu()

        self.center_view_on_player()

        return
