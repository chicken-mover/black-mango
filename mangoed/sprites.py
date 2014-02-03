
import blackmango.sprites
import mangoed.configure
import mangoed.ui


class GridCursor(blackmango.sprites.BaseSprite):
    """
    The grid cursor. Based on the BaseSprite object for convenience, but is not
    actually one of the objects tracked in the level object (to avoid confusion
    with materials and mobs). Instead, it is tracked and updated seperately by
    the EditorView.
    """

    def __init__(self):

        super(GridCursor, self).__init__(
            render_group = 'foreground',
            fill_color = (255, 0, 0, 150),
        )

        self.world_location = (0, 0, 0)
        self.translate()

    def untranslate(self, x, y):
        """
        Similar to the `translate()` method, but in reverse: given a set of on-
        screen corrdinates, position the sprite on the nearest grid vertex.

        So given the grid below:

              0,0 1,0 2,0
                +-+-+
                |A|B|
            0,1 +-+-+
                |C|D|
            0,2 +-+-+
                    2,2

        An (x, y) in quadrant D positions the sprite at (1, 1), anywhere in A at
        (0, 0), etc.

        """
        w, h = mangoed.ui.editor_window.get_size()

        scale = mangoed.configure.GRID_SIZE

        world_x = x / scale
        world_y = -1 * (y / scale - h) - 1

        self.world_location = (
            math.floor(world_x),
            math.floor(world_y),
            self.world_location[2]
        )
        self.translate()