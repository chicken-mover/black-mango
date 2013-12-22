
import blackmango.materials


class BasicLevel(object):

    level_size = None,
    starting_location = None
    
    next_level = None
    previous_level = None

    floors = None

    def __init__(self, level_data):
        """
        Load the data in <level_data> into a BasicLevel instance. 
        
        This parses the map data into actual materials objects and calls the 
        .translate() method on each material object so that it is assigned a 
        screen position. (That may need to change in the future)

        Material blocks on other floors have their visibility setting set to
        False.
        """

        # This is lazy because it isn't doing any error checking, and is very
        # breakage-prone
        for k, v in level_data.items():
            setattr(self, k, v)

        self.current_floor = self.starting_location[2]

        # Load all of the materials objects by iterating the data for each
        # floor
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


    def place_player(self, player, x = 0, y = 0, floor = 0):
        """
        Place the player in the game world, at position <x>, <y>, <floor>, or
        (if coordinates aren't provided) at the starting location.
        """
        floor = floor or self.starting_location[2]
        x = x or self.starting_location[0]
        y = y or self.starting_location[1]

        self.set_block(player, x, y, floor)
        player.world_location = (x, y, floor)
        player.translate()
        player.current_level = self

    
    def set_block(self, block, x, y, floor):
        """
        Set the location of a block for quick collision lookup.
        """
        self.floors[floor][y][x] = block

    def get_block(self, x, y, floor):
        """
        Get the material at <x>, <y>, <floor>. If the provided coordinates are
        invalid, returns an instance of VoidMaterial.
        """
        try:
            if x < 0 or y < 0 or floor < 0:
                raise IndexError("Bad level coordinates")
            return self.floors[floor][y][x]
        except IndexError:
            return blackmango.materials.MATERIALS[-1]()

