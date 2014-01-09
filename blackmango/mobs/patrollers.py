"""
A set of simple example patroller mobs for development and testing.
"""

import blackmango.mobs

class PatrollerV(blackmango.mobs.SimpleMob):

    direction = (0,1)

    previous_location = None
    next_location = None


    def behavior(self, level):

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

        self.move(level, *self.direction)
