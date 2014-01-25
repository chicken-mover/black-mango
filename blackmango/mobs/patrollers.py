"""
A set of simple example patroller mobs for development and testing.
"""

import pyglet

import blackmango.mobs

class PatrollerV(blackmango.mobs.SimpleMob):

    move_direction = (0,1)

    previous_location = None
    next_location = None


    def behavior(self, level):

        if self.animations:
            return

        if self.world_location == self.previous_location:
            self.move_direction = [-1*i for i in self.move_direction]

        self.previous_location = self.world_location
        l = [
            self.world_location,
            self.move_direction,
        ]
        self.next_location = [sum(i) for i in zip(*l)]

        self.move(level, *self.move_direction)

class ClockwisePatroller(blackmango.mobs.SimpleMob):

    def __init__(self, *args, **kwargs):

        self.old_location = None

        #self.vertex_list = vertex_list
        super(ClockwisePatroller, self).__init__(*args, **kwargs)

    def can_see_player(self, player):

        x, y, z = self.world_location
        px, py, pz = player.world_location

        if z != pz: return

        if x == px:
            if y < py and self.direction == 3:
                return True
            elif py < y and self.direction == 1:
                return True
        if y == py:
            if x < px and self.direction == 2:
                return True
            elif px < x and self.direction == 4:
                return True
        return False

    def behavior(self, level):

        if not self.old_location:
            self.old_location = self.world_location

        if self.can_see_player(level.player):
            chasers = filter(lambda x: isinstance(x, Chaser), \
                    level.mobs.values())
            for chaser in chasers:
                chaser.chase_active = True
                pyglet.clock.schedule_once(chaser.unchase, 1)
        
        if self.animations:
            return

        delta = self.old_location[0] - self.world_location[0] or \
                self.old_location[1] - self.world_location[1]
        delta = abs(delta)
        
        if delta < 6:
            if self.direction == 1:
                d = (0, -1)
            elif self.direction == 2:
                d = (1, 0)
            elif self.direction == 3:
                d = (0, 1)
            else:
                d = (-1, 0)
            self.move(level, *d)
        else:
            self.old_location = None
            if self.direction < 4:
                self.turn(self.direction + 1)
            else:
                self.turn(1)
            return self.behavior(level)

class Chaser(blackmango.mobs.SimpleMob):

    def __init__(self, *args, **kwargs):

        self.chase_active = False

        #self.vertex_list = vertex_list
        super(Chaser, self).__init__(*args, **kwargs)

    def behavior(self, level):

        if not self.chase_active:
            return

        next_move = self.path_to_player(level.player)
        if not next_move: return
        l = [
            self.world_location,
            next_move,
        ]
        next_location = [sum(i) for i in zip(*l)]
        if tuple(next_location) == level.player.world_location[:2]:
            level.player.kill()
        self.move(level, *next_move)

    def unchase(self, dt):
        self.chase_active = False

    def path_to_player(self, player):

        x, y, z = self.world_location
        px, py, pz = player.world_location

        if z != pz:
            return # Different room

        mx, my = px - x, py - y
        return int(mx > 0) or -1*int(mx < 0), \
               int(my > 0) or -1*int(my < 0)


