"""
Defines the BaseSprite class, from which mobs and materials inherit.
"""

import functools
import pyglet
import random

import blackmango.app
import blackmango.configure
import blackmango.ui

from blackmango.configure import ORDERED_GROUPS

sprite_batch = pyglet.graphics.Batch()

color_cache = {}

def notfrozen(f):
    def wrapped(self, *args, **kwargs):
        if self.is_frozen:
            return False
        else:
            return f(self, *args, **kwargs)
    return wrapped


class BaseSprite(pyglet.sprite.Sprite):

    is_solid = False
    is_mover = False
    is_portal = False
    opacity = 0

    is_pushable = False
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
        if blackmango.configure.DEBUG:
            if hasattr(self, 'direction') and \
               self.visible:
                d = self.direction
                self.debug_label.x = x + blackmango.configure.GRID_SIZE + 3
                self.debug_label.y = y - 3
                self.debug_label.text = '%s %s' % (repr(self.world_location), d)
            elif hasattr(self, 'direction') and not self.visible:
                self.debug_label.delete()
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

        pyglet.clock.schedule_once(lambda dt: self.reset_animations(),
                timer)

    def reset_animations(self):
        """
        Clear all pending animation frames.
        """
        self.animations = []


class BasicMobileSprite(BaseSprite):

    def __init__(self, image = None,
            x = 0,
            y = 0,
            z = 0,
            color = None,
        ):

        color = color or (0,0,255,255)

        super(BasicMobileSprite, self).__init__(image, x, y, z,
                'mobs', color)

        self.is_solid = True
        self.is_mover = True
        self.is_portal = False
        self.opacity = .1

        self.direction = 3

        self.animations = []

    def teleport(self, x, y, z):
        """
        Change the position of the sprite in the game world instantly.
        """
        dest = (x, y, z)
        level = blackmango.ui.game_window.view.current_level

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

    def move(self, delta_x = 0, delta_y = 0, strafe = False):
        """
        Move the sprite in the game world with an accompanying animation.
        """
        # TODO: Animate actual image frames
        if self.animations:
            return

        level = blackmango.ui.game_window.view.current_level

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
            ##block.interaction_callback( self)
            # and whatever you're standing on
            block = level.get_block(*self.world_location)
            if block:
                block.interaction_callback(self)
            return
        elif block:
            callback = functools.partial(block.interaction_callback, self)

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

    def can_see(self, mob):
        """
        Check to see if this mob can see the target <mob>.
        """
        
        level = blackmango.ui.game_window.view.current_level
        
        if mob.opacity == 0: return # Invisible mobs

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
            b = level.get_block(*coord)
            m = level.get_mob(*coord)
            if b:
                opacity += b.opacity
            if m:
                opacity += m.opacity
            if opacity >= 1:
                print opacity
                return False

        return True

    def _path_delta(self, c1, c2):
        """
        Return the next delta between three-tuple coordinates <c1> and <c2>
        according to the pathing algo.
        """

        level = blackmango.ui.game_window.view.current_level

        x, y, z = c1
        px, py, pz = c2

        if z != pz:
            return (0,0)# Different room

        mx, my = px - x, py - y

        delta_x, delta_y = int(mx > 0) or -1*int(mx < 0), \
                           int(my > 0) or -1*int(my < 0)

        # Don't try to move onto blocks that are occupied by solids
        if delta_x:
            next_pos = (x + delta_x, y, z)
            block = level.get_block(*next_pos)
            if block and block.is_solid:
                delta_x = 0
        if delta_y:
            next_pos = (x, y + delta_y, z)
            block = level.get_block(*next_pos)
            if block and block.is_solid:
                delta_y = 0

        # Don't return diagonal paths
        if delta_x and delta_y:
            # To keep pathing from being boring, randomly choose between which
            # axis gets moved along first
            delta = [delta_x, delta_y]
            delta[random.choice((0, 1))] = 0
            delta_x, delta_y = delta

        if delta_x:
            return (delta_x, 0)
        else:
            return (0, delta_y)

    def path_to(self, mob):
        """
        Give the next movement delta to apply to move towards <mob>.
        """
        x, y, z = self.world_location
        px, py, pz = mob.world_location

        if z != pz:
            return # Different room

        return self._path_delta((x, y, z), (px, py, pz))
