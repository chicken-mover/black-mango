
import pyglet

import blackmango.ui

titles_batch = pyglet.graphics.Batch()
labels_batch = pyglet.graphics.Batch()

TITLE_FONT_NAME = 'Times New Roman'
TITLE_FONT_SIZE = 12
TITLE_COLOR = (255, 255, 255, 255)

class TitleCard(pyglet.text.Label):

    def __init__(self, title):

        x, y = blackmango.ui.game_window.get_size()

        super(TitleCard, self).__init__(
            title,
            font_name = FONT_NAME,
            font_size = FONT_SIZE,
            x = x // 2,
            y = y // 2,
            anchor_x = 'center',
            anchor_y = 'center',
            batch = titles_batch,
            color = TITLE_COLOR,
        )