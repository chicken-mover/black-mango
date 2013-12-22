
import blackmango.materials

class BasicLevel(object):

    level_size = None,
    starting_location = None
    
    next_level = None
    previous_level = None

    floors = None

    def __init__(self, level_data):

        for k, v in level_data.items():
            setattr(self, k, v)

        self.current_floor = self.starting_location[2]

        for floor, floor_data in self.floors.items():
            for y, row in enumerate(floor_data):
                for x, v in enumerate(row):
                    material = blackmango.materials.MATERIALS[v]
                    if material:
                        m = material(x = x, y = y, 
                                z = floor)
                        self.floors[floor][y][x] = m
                        if self.current_floor == floor:
                            m.visible = True
                        else:
                            m.visible = False
                        m.translate()
                    else:
                        self.floors[floor][y][x] = None


    def place_player(self, player, x, y, floor):
        self.floors[floor][y][x] = player
        player.world_location = (x, y, floor)
        player.update_location()

