
import blackmango.mobs
import blackmango.ui

class Mirror(blackmango.mobs.SimpleMob):
    """
    As long as it can see the player, Mirror will try to mirror it's movements.
    """

    def __init__(self, *args, **kwargs):

        self.last_player_position = None

        #self.vertex_list = vertex_list
        super(Mirror, self).__init__(*args, **kwargs)

    def behavior(self):

        player = blackmango.ui.game_window.view.current_level.player

        if not player.world_location[2] == self.world_location[2]:
            return

        if self.last_player_position and \
           self.last_player_position != player.world_location:
            # Get the delta between the last and the next player position,
            # and move in a similar manner
            ox, oy, oz = self.last_player_position
            px, py, pz = player.world_location
            delta = self._path_delta((ox, oy, oz), (px, py, pz))
            self.move(*delta)
        

        self.last_player_position = player.world_location
        
