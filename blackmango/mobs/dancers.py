
import pyglet

import blackmango.mobs

class Chaser(blackmango.mobs.SimpleMob):

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

    def path_to_player(self, player):

        x, y, z = self.world_location
        px, py, pz = player.world_location

        if z != pz:
            return # Different room

        mx, my = px - x, py - y
        return int(mx > 0) or -1*int(mx < 0), \
               int(my > 0) or -1*int(my < 0)


