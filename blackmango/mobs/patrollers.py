"""
A set of simple example patroller mobs for development and testing.
"""

import pyglet

import blackmango.mobs

class PatrollerV(blackmango.mobs.SimpleMob):
    """
    Walk up and down the screen, turning around every time an obstable is
    encountered.
    """

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
    """
    Move in a clockwise square of a set size (currently 6)
    """

    def __init__(self, *args, **kwargs):

        self.old_location = None

        #self.vertex_list = vertex_list
        super(ClockwisePatroller, self).__init__(*args, **kwargs)

    def behavior(self, level):

        if not self.old_location:
            self.old_location = self.world_location

        if self.can_see(level.player, level):
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
    """
    If another mob sets this mob's chase_active attribute to True, run towards
    the player until it is set to False.
    """

    def __init__(self, *args, **kwargs):

        self.chase_active = False

        #self.vertex_list = vertex_list
        super(Chaser, self).__init__(*args, **kwargs)

    def behavior(self, level):

        if not self.chase_active:
            return
        if self.animations:
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


