
import pyglet

import blackmango.configure
import blackmango.ui.window

class BaseSprite(pyglet.sprite.Sprite):
    
    is_solid = 0
    is_mover = 0
    is_portal = 0
    opacity = 0

    portal_location = None

    def __repr__(self):

        vis = 'visible' if self.visible else 'hidden'
        name = self.__class__.__name__

        return '<%s %s at %s {%s,%s}>' % (
            vis, name, self.world_location, self.x, self.y        
        )

    def __init__(self, image = None,
            x = 0,
            y = 0,
            z = 0,
            render_batch = None,
            render_group = 0,
            fill_color = (255,255,255, 255),
            width = blackmango.configure.GRID_SIZE,
            height = blackmango.configure.GRID_SIZE,
        ):

        if not image:
            image = pyglet.image.SolidColorImagePattern(color=fill_color)
            image = image.create_image(width, height)

        group = blackmango.configure.ORDERED_GROUPS.get(render_group)
        group = pyglet.graphics.OrderedGroup(group)

        super(BaseSprite, self).__init__(image,
                batch = render_batch, group = group)

        self.world_location = (x, y, z)


    def translate(self):
      
        w, h = blackmango.ui.window.game_window_size

        scale = blackmango.configure.GRID_SIZE
        self.set_position(
            self.world_location[0] * scale,
            h - (self.world_location[1] + 1) * scale,
        )
