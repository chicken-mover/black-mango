"""
A set of simple example patroller mobs for development and testing.
"""

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

        self.walk_counter = 0

        #self.vertex_list = vertex_list
        super(ClockwisePatroller, self).__init__(*args, **kwargs)

    def behavior(self, level):
        
        if self.animations:
            return
        
        if self.walk_counter < 6:
            if self.direction == 1:
                d = (0, -1)
            elif self.direction == 2:
                d = (1, 0)
            elif self.direction == 3:
                d = (0, 1)
            else:
                d = (-1, 0)
            self.move(level, *d)
            self.walk_counter += 1
        else:
            self.walk_counter = 0
            if self.direction < 4:
                self.turn(self.direction + 1)
            else:
                self.turn(1)
            return self.behavior(level)

class Chaser(blackmango.mobs.SimpleMob):

    def __init__(self, *args, **kwargs):

        #self.vertex_list = vertex_list
        super(Chaser, self).__init__(*args, **kwargs)

    def behavior(self, level):
        pass
