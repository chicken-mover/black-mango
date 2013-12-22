
import blackmango.configure
import blackmango.levels
import blackmango.levels.testlevel

class GameEngine(object):

    def __init__(self):
        pass

    def new_game(self):
        blackmango.configure.logger.info('Initializing new game')
        level = blackmango.levels.BasicLevel(
            blackmango.levels.testlevel.TEST_LEVEL        
        )
        import pprint
        pp = pprint.PrettyPrinter()
        pp.pprint(level.floors)

    def on_draw(self, window):
        window.clear()
        blackmango.sprites.materials.materials_batch.draw()
        blackmango.mob.mobs_batch.draw()
