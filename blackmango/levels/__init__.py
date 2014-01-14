"""
A simple level object for loading level data and tracking stuff that's
happening inside the level.

This class also controls what part of the level we're looking at at any given
moment, and keeps references to mobs and blocks for quick collision lookup.

The level's `tick` method is used to iterate and call the `behavior` method on
each mob in the level.
"""

import cPickle

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
    # location, but we can always change it in the future.
    blocks = None
    mobs = None

    scheduled_destroy = False

    def __init__(self, level_data):
        """
        Read in the level data, and translate the lists of block ids in the
        floor data into instances of materials classes.
        """

        self.starting_location = level_data['starting_location']
        self.current_floor = self.starting_location[2]
        self.level_size = level_data['level_size']

        blockdata = level_data['blocks']
        mobdata = level_data['mobs']

        self.blocks = {}
        self.mobs = {}

        # Load all of the material and mob objects by iterating the data for
        # each floor
        for floor in xrange(self.level_size[2]):
            for y in xrange(self.level_size[1]):
                for x in xrange(self.level_size[0]):
                    try:
                        v = blockdata[floor][y][x]
                    except (IndexError, ValueError):
                        v = None
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
                        self.set_block(block, x, y, floor)
                    # Check to see if there is a mob for this location
                    try:
                        v = mobdata[floor][y][x]
                    except (IndexError, KeyError):
                        v = None
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
                        self.set_mob(mob, x, y, floor)


    def switch_floor(self, new_floor):
        """
        Set which floor we're on. This currently iterates every block and mob 
        for the current and new floor, and re-sets their visibility flag as
        appropriate.
        """
        for f in [self.blocks, self.mobs]:
            for floor in [self.current_floor, new_floor]:
                d = f[floor]
                for coords, m in d.items():
                    if floor != new_floor:
                        m.visible = False
                    else:
                        m.visible = True
        self.current_floor = new_floor

    def set_block(self, block, x, y, floor):
        """
        Set the location of a block for quick collision lookup.
        """
        block.visible = floor == self.current_floor
        block.translate()
        if not floor in self.blocks:
            self.blocks[floor] = {}
        self.blocks[floor][(x, y)] = block

    def get_block(self, x, y, floor):
        """
        Get the material at <x>, <y>, <floor>. If the provided coordinates are
        invalid, returns an instance of VoidMaterial.
        """
        try:
            return self.blocks[floor][(x, y)]
        except (IndexError, KeyError):
            return None

    def set_mob(self, mob, x, y, floor):
        """
        Set the location of a mob for quick collision lookup.
        """
        mob.visible = floor == self.current_floor
        mob.translate()
        if not floor in self.mobs:
            self.mobs[floor] = {}
        self.mobs[floor][(x, y)] = mob

    def get_mob(self, x, y, floor):
        """
        Get the mob at <x>, <y>, <floor>. If the provided coordinates are
        invalid, returns None.
        """
        try:
            return self.mobs[floor][(x, y)]
        except (IndexError, KeyError):
            return None

    def tick(self):
        if self.scheduled_destroy:
            return
        for mob in self.moblist:
            mob.behavior(self)

    def serialize(self, player):
        """
        Return a cPickle-encodable object that represents the current level
        state.

        Saved levels look a lot like standard levels, with a couple of extra
        attributes.
        """

        saved_level = {
            'level_size': self.level_size,
            'starting_location': player.world_location,

            'next_level': self.next_level,
            'previous_level': self.previous_level,

            'blocks': {},
            'mobs': {},

            'triggers': self.triggers,
        }

        # Fill out the blocks and mobs dicts. This is in the LEVEL_DATA format,
        # not in the internally stored format.
        x, y, floor = self.level_size
        for map in (saved_level['blocks'], saved_level['mobs']):
            for floor in xrange(floor):
                if not floor in map:
                    map[floor] = []
                for y in xrange(y):
                    while len(map[floor]) < y + 1:
                        map[floor].append([])
                    for x in xrange(x):
                        while len(map[floor][y]) < x + 1:
                            map[floor][y].append(None)

        # Now read the current block and mob states and record them
        for itemlist in ('blocks', 'mobs'):
            items = getattr(self, itemlist)
            for floor, spritelist in items.items():
                for item in spritelist:
                    x, y, floor = item.world_location
                    if itemlist == 'blocks':
                        lookup_dict = blackmango.materials.materiallist.MATERIALS
                        v = self.get_block(x, y, floor) or 0
                    elif itemlist == 'mobs':
                        lookup_dict = blackmango.mobs.moblist.MOBS
                        v = self.get_mob(x, y, floor) or 0
                    for k, t in lookup_dict.items():
                        if t and isinstance(item, t):
                            v = k

                # For re-initializing blocks later. Retrieve the stored kwargs
                # that they were intialized with.
                if hasattr(item, 'kwargs'):
                    v = (v, getattr(item, 'kwargs'))
                    
                # Save the item in the map
                saved_level[itemlist][floor][y][x] = v

        return saved_level

    def destroy(self):
        self.scheduled_destroy = True
        for lookuplist in [self.mobs, self.blocks]:
            for floor, listitems in lookuplist.items():
                for coords, sprite in listitems.items():
                    sprite.delete()
            

class BasicLevelTriggers(object):

    pass
