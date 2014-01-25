"""
Sprites that move. Players and NPCs.

This file should contain only the base mob classes. Subclasses of the
base mobs should be divided out into logically appropriate submodules.
"""

import functools
import pyglet

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

        self.direction = 3

        self.animations = []

    def teleport(self, level, x, y, z):
        """
        Change the position of the sprite in the game world instantly.
        """
        dest = (x, y, z)

        block = level.get_block(*dest)
        # Don't check interaction callbacks during teleport (otherwise you'll
        # get endless loops on teleporters).
        if block and block.is_solid:
            return
        mob = level.get_mob(*dest)
        if mob and mob.is_solid:
            return

        level.unset_mob(*self.world_location)
        level.set_mob(self, *dest)
        self.world_location = dest
        
        if level.current_floor != z:
            self.visible = False
        else:
            self.visible = True
            
        self.translate()

    def turn(self, direction):
        """
        Set the turn direction in degrees, where 'direction' is [1, 2, 3, 4],
        with '1' being 'north' and proceeding clockwise.
        """
        # TODO: Reflect turn in sprite image
        self.direction = direction

    def move(self, level, delta_x = 0, delta_y = 0, strafe = False):
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

        if not strafe:
            if delta_y:
                self.turn(3 if delta_y > 0 else 1)
            elif delta_x:
                self.turn(2 if delta_x > 0 else 4)

        block = level.get_block(*dest)
        if block and block.is_solid:
            block.push(self, self.world_location)
            return
        elif block and hasattr(block, 'interaction_callback'):
            callback = functools.partial(block.interaction_callback,
                    level,
                    self)

        mob = level.get_mob(*dest)
        if mob and mob.is_solid:
            mob.push(self, self.world_location)
            return

        level.unset_mob(*self.world_location)
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
        w, h = blackmango.ui.game_window.get_size()
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


class SimpleMob(BasicMobileSprite):

    def behavior(self, level):
        pass
