
import functools
import pyglet

import blackmango.configure
import blackmango.sprites

mobs_batch = pyglet.graphics.Batch()

class BasicMobileSprite(blackmango.sprites.BaseSprite):
    
    def __init__(self, image = None,
            x = 0,
            y = 0,
            z = 0,
            color = None,
        ):

        color = color or (0,0,255,255)
        group = blackmango.configure.ORDERED_GROUPS.get('mobs')

        super(BasicMobileSprite, self).__init__(image, x, y, z,
                mobs_batch, group, color)

        self.is_solid = 1
        self.is_mover = 1
        self.is_portal = 0
        self.opacity = 0

        self.animations = []

    def teleport(self, x, y, z):
        dest = (x, y, z)
        self.current_level.set_mob(None, *self.world_location)
        self.current_level.set_mob(self, *dest)
        self.world_location = dest
        if self.current_level.current_floor != z:
            self.visible = False
        else:
            self.visible = True
        self.translate()

    def move(self, delta_x, delta_y, delta_z):

        if self.animations:
            return

        callback = None

        dest = (
            self.world_location[0] + delta_x,
            self.world_location[1] + delta_y,
            self.world_location[2] + delta_z,
        )

        print dest

        if self.current_level:
            block = self.current_level.get_block(*dest)
            if block and block.is_solid:
                return
            elif block and hasattr(block, 'interaction_callback'):
                callback = functools.partial(block.interaction_callback,
                        self)
        
            mob = self.current_level.get_mob(*dest)
            if mob and mob.is_solid:
                return
            
            self.current_level.set_mob(None, *self.world_location)
            self.current_level.set_mob(self, *dest)

            self.world_location = dest
            self.smooth_translate(callback = callback)

    def scheduled_set_position(self, dt, *args):
        self.set_position(*args)

    def smooth_translate(self, callback = None):

        w, h = blackmango.ui.window.game_window_size
        scale = blackmango.configure.GRID_SIZE

        cur_x, cur_y = self.x, self.y
        dest_x, dest_y = (
            self.world_location[0] * scale,
            h - (self.world_location[1] + 1) * scale,
        )

        frames = blackmango.configure.BASE_ANIMATION_FRAMES
        delta_x = (dest_x - cur_x)/frames
        delta_y = (dest_y - cur_y)/frames

        for i in xrange(1, frames + 1):
            self.animations.append((
                self.scheduled_set_position,
                cur_x + delta_x * i,
                cur_y + delta_y * i,
            ))
        
        pyglet.clock.schedule_once(self.animate, .001, callback)

    def animate(self, dt, callback = None, t = .025):
        
        frames = blackmango.configure.BASE_ANIMATION_FRAMES
        for idx, fargs in enumerate(self.animations):
            timer = t * idx
            args = [fargs[0], timer] + list(fargs[1:])
            pyglet.clock.schedule_once(*args)
        
        if callback:
            pyglet.clock.schedule_once(lambda dt: callback(), timer)

        pyglet.clock.schedule_once(self.reset_animations,
                timer)

    def reset_animations(self, dt):
        self.animations = []


class Player(BasicMobileSprite):

    current_level = None
    
    def __init__(self, x = 0, y = 0, z = 0):

        color = (0,255,0, 255)
        group = blackmango.configure.ORDERED_GROUPS.get('player')

        super(Player, self).__init__(None, x, y, z,
                color)

    def teleport(self, x, y, z):
        dest = (x, y, z)
        self.current_level.set_mob(None, *self.world_location)
        self.current_level.set_mob(self, *dest)
        self.world_location = dest
        if self.current_level.current_floor != z:
            self.current_level.switch_floor(z)
        self.translate()

