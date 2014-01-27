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

class BasicMobileSprite(blackmango.sprites.BaseSprite):
    
    def __init__(self, image = None,
            x = 0,
            y = 0,
            z = 0,
            color = None,
        ):

        color = color or (0,0,255,255)

        super(BasicMobileSprite, self).__init__(image, x, y, z,
                'mobs', color)

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
            # Interact with whatever you're pushing
            ##block.interaction_callback(level, self)
            # and whatever you're standing on
            block = level.get_block(*self.world_location)
            if block:
                block.interaction_callback(level, self)
            return
        elif block:
            callback = functools.partial(block.interaction_callback, level,
                    self)

        mob = level.get_mob(*dest)
        if mob and mob.is_solid:
            mob.push(self, self.world_location)
            return

        level.unset_mob(*self.world_location)
        level.set_mob(self, *dest)

        self.world_location = dest
        self.smooth_translate(callback = callback)

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
                lambda dt, *args: self.set_position(*args),
                cur_x + delta_x * i,
                cur_y + delta_y * i,
            ))
        
        pyglet.clock.schedule_once(self.animate, .001, callback)

    def can_see(self, mob, level):
        """
        Check to see if this mob can see the target <mob>.
        """
        x, y, z = self.world_location
        px, py, pz = mob.world_location

        if z != pz: return False

        # Check to see if the target mob is aligned with our field of view
        if x != px and y != py:
            return False

        elif x == px:
            if y < py and self.direction == 3:
                coords = [(x, y, z) for y in xrange(y, py)]
            elif py < y and self.direction == 1:
                coords = [(x, y, z) for y in xrange(py, y)]
            else:
                return False
        elif y == py:
            if x < px and self.direction == 2:
                coords = [(x, y, z) for x in xrange(x, px)]
            elif px < x and self.direction == 4:
                coords = [(x, y, z) for x in xrange(px, x)]
            else:
                return False

        # Get all of the blocks between this mob and <mob>, and check opacity
        # values. If the total opacity hits 1, sight is blocked.
        opacity = 0
        for coord in coords:
            b = level.get_block(coord)
            m = level.get_mob(coord)
            if b:
                opacity += b.opacity
            if m:
                opacity += m.opacity
            if opacity >= 1:
                return False

        return True

    def path_to(self, mob, level):
        """
        Give the next movement delta to apply to move towards <mob>.
        """
        x, y, z = self.world_location
        px, py, pz = mob.world_location

        if z != pz:
            return # Different room

        mx, my = px - x, py - y

        delta_x, delta_y = int(mx > 0) or -1*int(mx < 0), \
                           int(my > 0) or -1*int(my < 0)

        # Don't try to move onto blocks that are occupied by solids
        if delta_x:
            next_pos = (x + delta_x, y, z)
            block = level.get_block(next_pos)
            if block.is_solid:
                delta_x = 0
        if delta_y:
            next_pos = (x, y + delta_y, z)
            block = level.get_block(next_pos)
            if block.is_solid:
                delta_y = 0

        # Don't return diagonal paths
        if delta_x:
            return (delta_x, 0)
        else:
            return (0, delta_y)


class SimpleMob(BasicMobileSprite):

    def behavior(self, level):
        pass
