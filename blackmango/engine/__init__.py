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

import blackmango.assets
import blackmango.configure
import blackmango.levels
import blackmango.levels.test_level
import blackmango.mobs.player
import blackmango.system

game_engine = None

# There is only one GameEngine object active at any one time.
def init(*args, **kwargs):
    global game_engine
    game_engine = GameEngine(*args, **kwargs)

class GameEngine(object):

    current_level = None
    player = None

    draw_events = set()

    def __init__(self):
        pass
    
    def new_game(self):
        """
        Start a new game. (Update this documentation when the function is more
        meaningful.)

        Right now this just initializes a test level.
        """
        blackmango.configure.logger.info('Initializing new game')
        self.start_game(blackmango.levels.test_level.LEVEL_DATA)

    def save_game(self, filepath = 'autosave.blackmango'):

        stored_level = self.current_level.serialize(self.player)
        file = os.path.join(blackmango.system.DIR_SAVEDGAMES, filepath)
        dir = os.path.dirname(file)
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

        file = os.path.join(blackmango.system.DIR_SAVEDGAMES, filepath)
        with open(file) as f:
            version, _, leveldata = f.read().partition('\n')
            if version != blackmango.configure.SAVE_GAME_VERSION:
                raise IOError("Version mismatch trying to load saved game data:"
                   " %s %s" % (version, blackmango.configure.SAVE_GAME_VERSION))
            stored_level = cPickle.loads(leveldata)
        self.start_game(stored_level)

    def start_game(self, level_data):

        if self.current_level:
            oldlevel = self.current_level
            self.current_level = None
            oldlevel.destroy()

        # Initialize level and player
        self.current_level = blackmango.levels.BasicLevel(
            level_data
        )
        self.player = blackmango.mobs.player.Player()

        # Place the player into the level
        starting_location = self.current_level.starting_location
        self.current_level.set_mob(self.player, *starting_location)
        self.player.world_location = starting_location
        self.player.translate()


    def register_draw(self, f):
        """
        Add a callable <f> to be called when the GameEngine's `on_draw` handler
        is triggered.
        """
        self.draw_events.add(f)

    def on_draw(self):
        """
        To be called by the GameWindow object when it triggers the on_draw
        event. The GameEngine is delegated the task of calling draws for the
        sprites/sprite batches it is tracking.
        """
        # Fire the registered draw events
        for f in self.draw_events:
            f()

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
