
import pyglet

import blackmango.mobs

class Mirror(blackmango.mobs.SimpleMob):
    """
    As long as it can see the player, Mirror will try to mirror it's movements.
    """

    def __init__(self, *args, **kwargs):

        self.last_player_position = None

        #self.vertex_list = vertex_list
        super(Mirror, self).__init__(*args, **kwargs)

    def behavior(self, level):

        if self.can_see(level.player, level):
            if not self.last_player_position:
                self.last_player_position = level.player.world_location
            if self.last_player_position != level.player.world_location:
                # Get the delta between the last and the next player position,
                # and move in a similar manner
                ox, oy, oz = self.last_player_position
                px, py, pz = level.player.world_location
                delta = self._path_delta((ox, oy, oz), (px, py, pz))
                self.move(level, *delta)
        else:
            # Don't try to mimic movement if there has been a gap in tracking
            # the player
            self.last_player_position = None
