
import pyglet

import blackmango.configure
import blackmango.levels
import blackmango.levels.testlevel
import blackmango.materials
import blackmango.mob

class GameEngine(object):

    level = None
    player = None

    def __init__(self):
        pass

    def new_game(self):
        """
        Start a new game. (Update this documentation when the function is more
        meaningful.)
        """
        blackmango.configure.logger.info('Initializing new game')
        level = blackmango.levels.BasicLevel(
            blackmango.levels.testlevel.TEST_LEVEL        
        )
        player = blackmango.mob.Player()
        level.place_player(player)

        self.level = level
        self.player = player

    def on_draw(self, window):
        """
        To be called by the GameWindow object when it triggers the on_draw
        event. The GameEngine is delegated the task of calling draws for the
        sprites/sprite batches it is tracking.

        <window> should be an instance of the GameWindow object.
        """
        window.clear()
        blackmango.materials.materials_batch.draw()
        blackmango.mob.mobs_batch.draw()

    def tick(self, keyboard):

        if self.player:

            if keyboard[pyglet.window.key.UP]:
                self.player.move(0, -1, 0)
            elif keyboard[pyglet.window.key.DOWN]:
                self.player.move(0, 1, 0)
            elif keyboard[pyglet.window.key.LEFT]:
                self.player.move(-1, 0, 0)
            elif keyboard[pyglet.window.key.RIGHT]:
                self.player.move(1, 0, 0)
