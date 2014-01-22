"""
Defines the BaseSprite class, from which mobs and materials inherit.
"""

import pyglet

import blackmango.app
import blackmango.configure
import blackmango.ui

debug_batch = pyglet.graphics.Batch()

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
            
        if blackmango.configure.DEBUG:
            self.debug_label = pyglet.text.Label('',
                    color = (255,0,255,255),
                    font_size = 8,
                    batch = debug_batch)

    def set_position(self, x, y):
        if blackmango.configure.DEBUG:
            if hasattr(self, 'direction'):
                d = self.direction
            else:
                d = ''
            self.debug_label.x = x + blackmango.configure.GRID_SIZE + 3
            self.debug_label.y = y - 3
            self.debug_label.text = '%s %s' % (repr(self.world_location), d)
        return super(BaseSprite, self).set_position(x, y)

    def translate(self):
        """
        Translate the current game world coordinates into the screen position
        for the current sprite object.
        """
        w, h = blackmango.ui.game_window.get_size()

        scale = blackmango.configure.GRID_SIZE
        w_w = self.world_location[0] * scale
        w_h = h - (self.world_location[1] + 1) * scale
        self.set_position(w_w, w_h)

    def animate(self, dt, callback = None, t = .025):
        """
        Iterate the animation queue for the current object and execute
        everything we find there.
        """

        for idx, fargs in enumerate(self.animations):
            timer = t * idx
            args = [fargs[0], timer] + list(fargs[1:])
            pyglet.clock.schedule_once(*args)

        if callback:
            pyglet.clock.schedule_once(lambda dt: callback(), timer)

        pyglet.clock.schedule_once(self.reset_animations,
                timer)

    def reset_animations(self, dt):
        """
        A wrapper to reset self.animations, with an argspec appropriate for the
        pyglet.clock.schedule* family of methods.
        """
        self.animations = []
