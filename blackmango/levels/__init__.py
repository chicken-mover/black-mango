"""
A simple level object for loading level data and tracking stuff that's
happening inside the level.

This class also controls what part of the level we're looking at at any given
moment, and keeps references to mobs and blocks for quick collision lookup.

The level's `tick` method is used to iterate and call the `behavior` method on
each mob in the level.
"""

import blackmango.scenery

from blackmango.materials.materiallist import MATERIALS
from blackmango.mobs.moblist import MOBS

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

    def __init__(self, level_data, player):
        """
        Read in the level data, and translate the lists of block ids in the
        floor data into instances of materials classes.
        """

        self.title_card = level_data['title_card']
        self.starting_location = level_data['starting_location']
        self.current_floor = self.starting_location[2]
        self.size = level_data['level_size']
        self.triggers = level_data['triggers']()
        self.next_level = level_data['next_level']
        self.backgrounds = level_data['backgrounds'].copy()
        for k, v in self.backgrounds.items():
            if v:
                self.backgrounds[k] = blackmango.scenery.Background(v)

        blockdata = level_data['blocks']
        mobdata = level_data['mobs']

        self.blocks = {}
        self.mobs = {}

        self.player = player

        # Load all of the material and mob objects by iterating the data for
        # each floor
        for floor in xrange(self.size[2]):
            for y in xrange(self.size[1]):
                for x in xrange(self.size[0]):
                    try:
                        v = blockdata[floor][y][x]
                    except (IndexError, ValueError):
                        v = None
                    if v:
                        if isinstance(v, tuple):
                            # This is for portals, but might be useful for
                            # other special cases in the future.
                            material = MATERIALS[v[0]]
                            kwargs = v[1]
                            kwargs.update({
                                'x': x,
                                'y': y,
                                'z': floor,
                            })
                            block = material(**kwargs)
                        else:
                            # basic block init.
                            material = MATERIALS[v]
                            block = material(x = x, y = y, z = floor)
                        self.set_block(block, x, y, floor)
                    # Check to see if there is a mob for this location
                    try:
                        v = mobdata[floor][y][x]
                    except (IndexError, KeyError):
                        v = None
                    if v:
                        if isinstance(v, tuple):
                            mob = MOBS[v[0]]
                            kwargs = v[1]
                            kwargs.update({
                                'x': x,
                                'y': y,
                                'z': floor,
                            })
                            m = mob(**kwargs)
                        else:
                            m = MOBS[v]
                            mob = m(x = x, y = y, z = floor)
                        self.set_mob(mob, x, y, floor)

        if not self.triggers.triggers_initialized:
            self.triggers.init_triggers(self, self.player)

    def get_background(self):
        return self.backgrounds.get(self.current_floor)

    def switch_floor(self, new_floor):
        """
        Set which floor we're on. This currently iterates every block and mob 
        for the current and new floor, and re-sets their visibility flag as
        appropriate.
        """
        for f in [self.blocks, self.mobs]:
            for floor in [self.current_floor, new_floor]:
                items = filter(lambda x: x[0][2] == floor, f.items())
                for k, m in items:
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
        self.blocks[(x, y, floor)] = block

    def unset_block(self, x, y, floor):
        k = (x, y, floor)
        if k in self.blocks:
            del self.blocks[k]

    def get_block(self, x, y, floor):
        """
        Get the material at <x>, <y>, <floor>. If the provided coordinates are
        invalid, returns an instance of VoidMaterial.
        """
        if x < 0 or x > self.size[0] - 1 or \
           y < 0 or y > self.size[1] - 1 or \
           floor < 0 or floor > self.size[2] - 1:
            return MATERIALS[-1]()
        try:
            return self.blocks[(x, y, floor)]
        except (IndexError, KeyError):
            return None

    def set_mob(self, mob, x, y, floor):
        """
        Set the location of a mob for quick collision lookup.
        """
        mob.visible = floor == self.current_floor
        mob.translate()
        self.mobs[(x, y, floor)] = mob

    def unset_mob(self, x, y, floor):
        k = (x, y, floor)
        if k in self.mobs:
            del self.mobs[k]

    def get_mob(self, x, y, floor):
        """
        Get the mob at <x>, <y>, <floor>. If the provided coordinates are
        invalid, returns None.
        """
        try:
            return self.mobs[(x, y, floor)]
        except (IndexError, KeyError):
            return None

    def tick(self):
        if self.scheduled_destroy:
            return
        for _, mob in self.mobs.items():
            if mob is not self.player:
                mob.do_behavior()
        self.triggers.tick(self, self.player)

    def serialize(self):
        """
        Return a pickleable object that represents the current level state.
        Saved level data should be identical in format to prepared level data.
        """

        saved_level = {
            'title_card': self.title_card,
            'level_size': self.size,
            'starting_location': self.player.world_location,

            'next_level': self.next_level,

            'backgrounds': {},

            'blocks': {},
            'mobs': {},

            'triggers': self.triggers,
        }

        for k, v in backgrounds:
            saved_level['backgrounds'][k] = v.image

        # Fill out the blocks and mobs dicts. This is in the LEVEL_DATA format,
        # not in the internally stored format.
        lx, ly, lfloor = self.size
        for map in (saved_level['blocks'], saved_level['mobs']):
            for floor in xrange(lfloor):
                if not floor in map:
                    map[floor] = []
                for y in xrange(ly):
                    while len(map[floor]) < y + 1:
                        map[floor].append([])
                    for x in xrange(lx):
                        while len(map[floor][y]) < x + 1:
                            map[floor][y].append(None)

        # Now read the current block and mob states and record them
        for lookup in ('blocks', 'mobs'):
            lookuplist = getattr(self, lookup)
            for coords, item in lookuplist.items():
                v = 0
                if lookuplist is self.blocks:
                    lookup_dict = MATERIALS
                elif lookuplist is self.mobs:
                    lookup_dict = MOBS
                for k, t in lookup_dict.items():
                    if t and isinstance(item, t):
                        v = k

                # For re-initializing blocks later. Retrieve the stored kwargs
                # that they were intialized with.
                if hasattr(item, 'kwargs'):
                    v = (v, getattr(item, 'kwargs'))

                # Save the item in the map
                x, y, floor = coords
                saved_level[lookup][floor][y][x] = v

        return saved_level

    def destroy(self):
        self.scheduled_destroy = True
        for lookuplist in [self.mobs, self.blocks]:
            for coords, sprite in lookuplist.items():
                sprite.delete()
            

class BasicLevelTriggers(object):

    def __init__(self): 
        self.triggers_initialized = False

    def init_triggers(self, level, player):
        self.triggers_initialized = True

    def tick(self, level, player):
        pass
