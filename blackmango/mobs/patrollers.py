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
