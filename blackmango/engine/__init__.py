"""
This module governs the core GameEngine class.

The GameEngine handles things like game state, the current level, loading and
saving the game, etc. Basically, anything that isn't at GameWindow level is
delegated to the GameEngine for dealing with.

GameEngine does NOT handle anything outside of the ongoing game. So the
initial load/save/new game/credits splash menu shouldn't be dealt with here.
"""

import cPickle
import errno
import os
import pyglet

import blackmango.configure
import blackmango.levels
import blackmango.levels.test_level
import blackmango.mobs.player
import blackmango.system

game_engine = None
logger = blackmango.configure.logger

# There is only one GameEngine object active at any one time.
def init(*args, **kwargs):
    """
    Called by the central startup routine during initialization.
    """
    global game_engine
    global blackmango
    # Prevent circular imports
    import blackmango.ui
    blackmango.configure.logger.info("Initializing GameEngine as game_engine")
    game_engine = GameEngine(*args, **kwargs)

class GameEngine(object):

    current_level = None
    player = None

    # During loading events, we don't want to tick the game or perform certain
    # other actions on running event loops. See the @loading_pause decorator.
    loading = False

    def __init__(self): pass

    def save_game(self, filepath = 'autosave.blackmango'):

        stored_level = self.current_level.serialize(self.player)

        file = os.path.join(blackmango.system.DIR_SAVEDGAMES, filepath)
        dir = os.path.dirname(file)
        
        blackmango.configure.logger.info("Saving game: %s" % file)
        
        try:
            os.makedirs(dir)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(dir):
                pass
            else:
                raise

        with open(file, 'w') as f:
            f.write(blackmango.configure.SAVE_GAME_VERSION + '\n')
            f.write(cPickle.dumps(stored_level))
        return True

    def load_game(self, filepath = 'autosave.blackmango'):

        self.loading = True
        blackmango.configure.logger.info("Scheduling load game...")

        current_save_vesion = blackmango.configure.SAVE_GAME_VERSION

        def loader(dt):
            file = os.path.join(blackmango.system.DIR_SAVEDGAMES, filepath)
            blackmango.configure.logger.info("Loading game: %s" % file)
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

        if self.current_level:
            self.current_level.destroy()
            self.current_level = None

        # Initialize level and player
        self.current_level = blackmango.levels.BasicLevel(level_data)
        self.player = blackmango.mobs.player.Player()

        # Place the player into the level
        starting_location = self.current_level.starting_location
        self.current_level.set_mob(self.player, *starting_location)
        self.player.world_location = starting_location
        self.player.translate()

        self.loading = False

        blackmango.configure.logger.info("Game started: %s" % 
                repr(self.current_level))

    def input_tick(self, keyboard):
        """
        On each input tick, pass the current keyboard state in for the engine
        to handle (obviously, only if the engine should be dealing with that
        sort of thing at the time).
        """

        if keyboard[pyglet.window.key.UP]:
            self.player.move(self.current_level, 0, -1)
        elif keyboard[pyglet.window.key.DOWN]:
            self.player.move(self.current_level, 0, 1)
        elif keyboard[pyglet.window.key.LEFT]:
            self.player.move(self.current_level, -1, 0)
        elif keyboard[pyglet.window.key.RIGHT]:
            self.player.move(self.current_level, 1, 0)

        elif keyboard[pyglet.window.key.S]:
            self.save_game()
        elif keyboard[pyglet.window.key.L]:
            self.load_game()

    def game_tick(self):

        if self.current_level:
            self.current_level.tick()
