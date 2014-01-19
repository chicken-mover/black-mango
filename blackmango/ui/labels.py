
import pyglet
        
import blackmango.ui

TITLE_FONT_NAME = 'Menuetto'
TITLE_FONT_SIZE = 48
TITLE_COLOR = (255, 255, 255, 255)

class MainTitleCard(pyglet.text.Label):

    def __init__(self, title, offset = 0, batch = None):

        x, y = blackmango.ui.game_window.get_size()

        super(MainTitleCard, self).__init__(
            title,
            font_name = TITLE_FONT_NAME,
            font_size = TITLE_FONT_SIZE,
            x = x // 2,
            y = y - (y // 4) - offset,
            anchor_x = 'center',
            anchor_y = 'center',
            batch = batch,
            color = TITLE_COLOR,
        )

class SubTitleCard(pyglet.text.Label):

    def __init__(self, title, batch):

        x, y = blackmango.ui.game_window.get_size()

        super(SubTitleCard, self).__init__(
            title,
            font_name = 'Chapbook',
            font_size = 12,
            x = x // 2,
            y = y // 2 - (y // 4),
            anchor_x = 'center',
            anchor_y = 'center',
            batch = batch,
            color = TITLE_COLOR,
        )


