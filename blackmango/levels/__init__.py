
import blackmango.materials


class BasicLevel(object):

    level_size = None,
    starting_location = None
    
    next_level = None
    previous_level = None

    floors = None
    blocks = None
    mobs = None

    def __init__(self, level_data):

        # This is lazy because it isn't doing any error checking, and is very
        # breakage-prone
        for k, v in level_data.items():
            setattr(self, k, v)

        self.current_floor = self.starting_location[2]

        # Load all of the materials objects by iterating the data for each
        # floor
        self.blocks = {}
        self.mobs = {}
        for floor, floor_data in self.floors.items():
            self.blocks[floor] = []
            self.mobs[floor] = []
            for y, row in enumerate(floor_data):
                self.blocks[floor].append([])
                self.mobs[floor].append([])
                for x, v in enumerate(row):
                    self.blocks[floor][y].append(None)
                    self.mobs[floor][y].append(None)
                    if v:
                        if isinstance(v, blackmango.materials.BaseMaterial):
                            m = v
                            self.blocks[floor][y][x] = v
                        else:
                            material = blackmango.materials.MATERIALS[v]
                            m = material(x = x, y = y, 
                                    z = floor)
                            self.blocks[floor][y][x] = m
                        m.visible = floor == self.current_floor
                        m.translate()

    
    def place_player(self, player, x = 0, y = 0, floor = 0):
        """
        Place the player in the game world, at position <x>, <y>, <floor>, or
        (if coordinates aren't provided) at the starting location.
        """
        floor = floor or self.starting_location[2]
        x = x or self.starting_location[0]
        y = y or self.starting_location[1]

        self.set_mob(player, x, y, floor)
        player.world_location = (x, y, floor)
        player.translate()
        player.current_level = self

    
    def set_block(self, block, x, y, floor):
        """
        Set the location of a block for quick collision lookup.
        """
        self.blocks[floor][y][x] = block

    def get_block(self, x, y, floor):
        """
        Get the material at <x>, <y>, <floor>. If the provided coordinates are
        invalid, returns an instance of VoidMaterial.
        """
        try:
            if x < 0 or y < 0 or floor < 0:
                raise IndexError("Bad level coordinates")
            return self.blocks[floor][y][x]
        except IndexError:
            return blackmango.materials.MATERIALS[-1]()

    def set_mob(self, mob, x, y, floor):
        self.mobs[floor][y][x] = mob

    def get_mob(self, x, y, floor):
        try:
            if x < 0 or y < 0 or floor < 0:
                raise IndexError("Bad level coordinates")
            return self.mobs[floor][y][x]
        except IndexError:
            return None
