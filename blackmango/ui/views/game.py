
import blackmango.configure
import blackmango.engine
import blackmango.materials
import blackmango.mobs
import blackmango.ui.views

def loading_halt(f):
    def wrapped(self, *args, **kwargs):
        if blackmango.engine.game_engine.loading:
            return
        else:
            return f(self, *args, **kwargs)
    return wrapped

class GameView(blackmango.ui.views.BaseView):

    def __init__(self, level = None):
        if level == 'new':
            import blackmango.levels.test_level
            blackmango.configure.logger.info("Starting new game...")
            blackmango.engine.game_engine.start_game(
                    blackmango.levels.test_level.LEVEL_DATA)
        elif level.endswith('autosave'):
            blackmango.engine.game_engine.load_game(level)

    def destroy(self):
        pass

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
        blackmango.engine.game_engine.input_tick(keyboard)
        blackmango.engine.game_engine.game_tick()
