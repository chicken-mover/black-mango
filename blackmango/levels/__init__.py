"""
A simple level object for loading level data and tracking stuff that's
happening inside the level.

This class also controls what part of the level we're looking at at any given
moment, and keeps references to mobs and blocks for quick collision lookup.

The level's `tick` method is used to iterate and call the `behavior` method on
each mob in the level.
"""

import blackmango.materials
import blackmango.materials.materiallist
import blackmango.mobs
import blackmango.mobs.moblist

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
    blocklist = []

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
        self.blocklist = []

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
                            material = blackmango.materials.materiallist.MATERIALS[v[0]]
                            kwargs = v[1]
                            kwargs.update({
                                'x': x,
                                'y': y,
                                'z': floor,
                            })
                            block = material(**kwargs)
                        else:
                            # basic block init.
                            material = blackmango.materials.materiallist.MATERIALS[v]
                            block = material(x = x, y = y, z = floor)
                        self.blocks[floor][y][x] = block
                        block.visible = floor == self.current_floor
                        block.translate()
                        self.blocklist.append(block)
                    # Check to see if there is a mob for this location
                    try:
                        v = self.mobs[floor][y][x]
                    except (IndexError, KeyError):
                        continue
                    if v:
                        if isinstance(v, tuple):
                            mob = blackmango.mobs.moblist.MOBS[v[0]]
                            kwargs = v[1]
                            kwargs.update({
                                'x': x,
                                'y': y,
                                'z': floor,
                            })
                            m = mob(**kwargs)
                        else:
                            m = blackmango.mobs.moblist.MOBS[v]
                            mob = m(x = x, y = y, z = floor)
                        self.mobs[floor][y][x] = mob
                        mob.visible = floor == self.current_floor
                        mob.world_location = (x, y, floor)
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
            return blackmango.materials.materiallist.MATERIALS[-1]()

    def set_mob(self, mob, x, y, floor):
        """
        Set the location of a mob for quick collision lookup.
        """
        if not floor in self.mobs:
            self.mobs[floor] = []
        while y + 1 > len(self.mobs[floor]):
            self.mobs[floor].append([])
        while x + 1 > len(self.mobs[floor][y]):
            self.mobs[floor][y].append(None)
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
            mob.behavior(self)

    def serialize(self):
        """
        Return a cPickle-encodable object that represents the current level
        state.

        Saved levels look a lot like standard levels, with a couple of extra
        attributes.
        """

        saved_level = {
            'level_size': self.level_size,
            'starting_location': self.starting_location,

            'next_level': self.next_level,
            'previous_level': self.previous_level,

            # Get this by testing for instances of player when iterating the
            # moblist? Or as an argument passed in
            'current_location': None,

            'blocks': {},
            'mobs': {},
        }

        # Now read the current block and mob states and record them
        for itemlist in ('blocklist', 'moblist'):
            items = getattr(self, itemlist)
            for item in items:
                x, y, floor = item.world_location
                v = 0
                if d == 'blocklist':
                    map = 'blocks'
                    lookup_dict = blackmango.materials.materiallist.MATERIALS
                elif d == 'moblist':
                    map = 'mobs'
                    lookup_dict = blackmango.mobs.moblist.MOBS
                for k, t in lookup_dict.items():
                    if isinstance(v, t):
                        v = k

                # Make sure the floor exists in the map
                if not floor in saved_level[map]:
                    saved_level[map][floor] = []

                # Make sure the maps have enough slots
                while len(saved_level[map][floor]) < x - 1:
                    saved_level[map][floor].append([])
                while len(saved_level[map][floor][x]) < y - 1:
                    saved_level[map][floor][x].append(None)
                    
                # Save the item in the map
                saved_level[d][floor][x][y] = v

        return saved_level

class BasicLevelBehavior(object):

    pass
