"""
Defines the BaseSprite class, from which mobs and materials inherit.
"""

import pyglet

import blackmango.app
import blackmango.configure
import blackmango.ui

from blackmango.configure import ORDERED_GROUPS

sprite_batch = pyglet.graphics.Batch()

color_cache = {}

class BaseSprite(pyglet.sprite.Sprite):
    
    is_solid = 0
    is_mover = 0
    is_portal = 0
    opacity = 0

    is_pushable = 0
    weight = 0
    pushes = {}

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
            render_group = 'mobs',
            fill_color = (255,255,255, 255),
            width = blackmango.configure.GRID_SIZE,
            height = blackmango.configure.GRID_SIZE,
        ):

        if not image:
            if fill_color not in color_cache:
                i = pyglet.image.SolidColorImagePattern(color=fill_color)
                i = i.create_image(width, height)
                color_cache[fill_color] = i
            image = color_cache[fill_color]

        group = ORDERED_GROUPS.get(render_group)

        super(BaseSprite, self).__init__(image,
                batch = sprite_batch, group = group)

        self.world_location = (x, y, z)
            
        if blackmango.configure.DEBUG:

            self.debug_label = pyglet.text.Label('',
                    color = (255,0,255,255),
                    font_size = 8,
                    batch = sprite_batch,
                    group = ORDERED_GROUPS.get('foreground'))

    def push(self, pusher, force):
        """
        Receive a push from <pusher>. Called when something is trying to move to
        this object's location, but can't.
        """
        # TODO: 'force' should escalate as long as the pusher hasn't moved and
        # this object is pushable. When it surpasses the weight of the object,
        # this method should run it's logic
        pass

    def set_position(self, x, y):
        if blackmango.configure.DEBUG and hasattr(self, 'direction'):
            d = self.direction
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
