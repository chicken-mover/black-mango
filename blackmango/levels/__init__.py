"""
A simple level object for loading level data and tracking stuff that's
happening inside the level.
"""

import blackmango.materials

class BasicLevel(object):

    level_size = None,
    starting_location = None
    
    next_level = None
    previous_level = None

    blocks = None

    # Blocks and mobs are tracked seperately. I don't know if this is a good
    # idea or a terrible one. It seems like it might not be super extensible in
    # the future, because it means not having more than one mob at each world
    # location, but we can always change it in the future.but let's find out.
    blocks = None
    mobs = None

    moblist = []

    def __init__(self, level_data):
        """
        Read in the level data, and translate the lists of block ids in the
        floor data into instances of materials classes.
        """

        # This is lazy because it isn't doing any error checking, and is very
        # breakage-prone
        for k, v in level_data.items():
            setattr(self, k, v)

        self.current_floor = self.starting_location[2]

        # Important re-definition to prevent bugs
        self.moblist = []

        # Load all of the materials objects by iterating the data for each
        # floor and filling out the self.blocks object. As we work, we also
        # fill out the self.mobs one with None values, so we don't have to
        # init it seperately.
        for floor, block_data in self.blocks.items():
            for y, row in enumerate(block_data):
                for x, v in enumerate(row):
                    if v:
                        if isinstance(v, tuple):
                            # This is for portals, but might be useful for
                            # other special cases in the future.
                            material = blackmango.materials.MATERIALS[v[0]]
                            kwargs = v[1]
                            kwargs.update({
                                'x': x,
                                'y': y,
                                'z': floor,
                            })
                            m = material(**kwargs)
                        else:
                            # basic block init.
                            material = blackmango.materials.MATERIALS[v]
                            m = material(x = x, y = y, 
                                    z = floor)
                        self.blocks[floor][y][x] = m
                        m.visible = floor == self.current_floor
                        m.translate()
                    # Check to see if there is a mob for this location
                    try:
                        m = self.mobs[floor][y][x]
                    except IndexError:
                        continue
                    if m:
                        mob = m()
                        self.mobs[floor][y][x] = mob
                        mob.visible = floor == self.current_floor
                        mob.world_location = (x, y, floor)
                        mob.current_level = self
                        mob.translate()
                        self.moblist.append(mob)


    def switch_floor(self, new_floor):
        """
        Set which floor we're on. This currently iterates every block and mob 
        for the current and new floor, and re-sets their visibility flag as
        appropriate.
        """
        for f in [self.blocks, self.mobs]:
            for floor in [self.current_floor, new_floor]:
                d = f[floor]
                for row in d:
                    for m in row:
                        if m:
                            if floor != new_floor:
                                m.visible = False
                            else:
                                m.visible = True
        self.current_floor = new_floor

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
        """
        Set the location of a mob for quick collision lookup.
        """
        if mob:
            mob.current_level = self
        self.mobs[floor][y][x] = mob

    def get_mob(self, x, y, floor):
        """
        Get the mob at <x>, <y>, <floor>. If the provided coordinates are
        invalid, returns None.
        """
        try:
            if x < 0 or y < 0 or floor < 0:
                raise IndexError("Bad level coordinates")
            return self.mobs[floor][y][x]
        except IndexError:
            return None

    def tick(self):
        for mob in self.moblist:
            mob.behavior()
