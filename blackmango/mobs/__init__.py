"""
Sprites that move. Players and NPCs.
"""

import functools
import pyglet

import blackmango
import blackmango.configure
import blackmango.sprites
import blackmango.ui

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

    def teleport(self, level, x, y, z):
        """
        Change the position of the sprite in the game world instantly.
        """
        dest = (x, y, z)
        level.set_mob(None, *self.world_location)
        level.set_mob(self, *dest)
        self.world_location = dest
        if level.current_floor != z:
            self.visible = False
        else:
            self.visible = True
        self.translate()

    def move(self, level, delta_x, delta_y):
        """
        Move the sprite in the game world with an accompanying animation.
        """
        #TODO: Animate actual image frames
        if self.animations:
            return

        callback = None

        dest = (
            self.world_location[0] + delta_x,
            self.world_location[1] + delta_y,
            self.world_location[2],
        )

        if level:
            block = level.get_block(*dest)
            if block and block.is_solid:
                return
            elif block and hasattr(block, 'interaction_callback'):
                callback = functools.partial(block.interaction_callback,
                        self)
        
            mob = level.get_mob(*dest)
            if mob and mob.is_solid:
                return
            
            level.set_mob(None, *self.world_location)
            level.set_mob(self, *dest)

            self.world_location = dest
            self.smooth_translate(callback = callback)

    def scheduled_set_position(self, dt, *args):
        """
        A wrapper for self.set_position that has the write argspec for use
        with the pyglet.clock.schedule* family of methods.
        """
        self.set_position(*args)

    def smooth_translate(self, callback = None):
        """
        Like self.translate, but provides gradual movement between two 
        positions.

        The <callback> callable is called after the final animation frame.
        """
        w, h = blackmango.main_window.get_size()
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


class SimpleMob(BasicMobileSprite):

    def behavior(self):
        pass


class PatrollerV(SimpleMob):

    direction = (0,1)

    previous_location = None
    next_location = None


    def behavior(self):

        if self.animations:
            return

        if self.world_location == self.previous_location:
            self.direction = [-1*i for i in self.direction]
    
        self.previous_location = self.world_location
        l = [
            self.world_location,
            self.direction,
        ]
        self.next_location = [sum(i) for i in zip(*l)]

        self.move(*self.direction)


MOBS = {
    0: None,
    1: SimpleMob,
    2: PatrollerV,
}