
import blackmango.mobs

class PatrollerV(blackmango.mobs.SimpleMob):

    direction = (0,1,0)

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

