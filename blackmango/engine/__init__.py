"""
This module governs the core GameEngine class.

The GameEngine handles things like game state, the current level, loading and
saving the game, etc. Basically, anything that isn't at GameWindow level is
delegated to the GameEngine for dealing with.

GameEngine does NOT handle anything outside of the ongoing game. So the
initial load/save/new game/credits splash menu shouldn't be dealt with here.
"""

import pyglet

import blackmango.configure
import blackmango.levels
import blackmango.levels.test_level
import blackmango.materials
import blackmango.mob.player

class GameEngine(object):

    current_level = None
    player = None

    def __init__(self):
        pass

    def new_game(self):
        """
        Start a new game. (Update this documentation when the function is more
        meaningful.)

        Right now this just initializes a test level.
        """

        blackmango.configure.logger.info('Initializing new game')
        
        # Initialize level and player
        current_level = blackmango.levels.BasicLevel(
            blackmango.levels.test_level.LEVEL_DATA        
        )
        player = blackmango.mob.player.Player()

        # Place the player into the level
        starting_location = current_level.starting_location
        current_level.set_mob(player, *starting_location)
        player.world_location = starting_location
        player.translate()

        # Store the initialized objects
        self.current_level = current_level
        self.player = player

    def on_draw(self):
        """
        To be called by the GameWindow object when it triggers the on_draw
        event. The GameEngine is delegated the task of calling draws for the
        sprites/sprite batches it is tracking.
        """
        # Fire the draw for material and mob batches.
        blackmango.materials.materials_batch.draw()
        blackmango.mob.mobs_batch.draw()

    def input_tick(self, keyboard):
        """
        On each input tick, pass the current keyboard state in for the engine
        to handle (obviously, only if the engine should be dealing with that
        sort of thing at the time).
        """

        if self.player:

            """
            # Diagonal movement?
            if keyboard[pyglet.window.key.UP] and \
               keyboard[pyglet.window.key.LEFT]:
                self.player.move(-1, -1, 0)
            elif keyboard[pyglet.window.key.UP] and \
               keyboard[pyglet.window.key.RIGHT]:
                self.player.move(1, -1, 0)
            elif keyboard[pyglet.window.key.DOWN] and \
               keyboard[pyglet.window.key.LEFT]:
                self.player.move(-1, 1, 0)
            elif keyboard[pyglet.window.key.DOWN] and \
               keyboard[pyglet.window.key.RIGHT]:
                self.player.move(1, 1, 0)
            """
            
            if keyboard[pyglet.window.key.UP]:
                self.player.move(0, -1, 0)
            elif keyboard[pyglet.window.key.DOWN]:
                self.player.move(0, 1, 0)
            elif keyboard[pyglet.window.key.LEFT]:
                self.player.move(-1, 0, 0)
            elif keyboard[pyglet.window.key.RIGHT]:
                self.player.move(1, 0, 0)

    def game_tick(self):

        if self.current_level:
            self.current_level.tick()
