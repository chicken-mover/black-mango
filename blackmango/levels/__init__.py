"""
A simple level object for loading level data and tracking stuff that's
happening inside the level.

This class also controls what part of the level we're looking at at any given
moment, and keeps references to mobs and blocks for quick collision lookup.

The level's `tick` method is used to iterate and call the `behavior` method on
each mob in the level.
"""

import pprint

import blackmango.scenery

from blackmango.materials.materiallist import MATERIALS
from blackmango.mobs.moblist import MOBS

class BasicLevel(object):

    level_size = None,
    starting_location = None

    blocks = None

    # Blocks and mobs are tracked seperately. I don't know if this is a good
    # idea or a terrible one. It seems like it might not be super extensible in
    # the future, because it means not having more than one mob at each world
    # location, but we can always change it in the future.
    blocks = None
    mobs = None

    scheduled_destroy = False

    def __init__(self, level_data, player = None):
        """
        Read in the level data, and translate the lists of block ids in the
        floor data into instances of materials classes.
        """

        self.title_card = level_data.NAME
        self.starting_location = level_data.PLAYER_START
        self.current_floor = self.starting_location[2]
        self.size = level_data.SIZE
        # Probably being loaded by the level editor. Ignore triggers
        if level_data.TRIGGERS:
            self.triggers = level_data.TRIGGERS()
        self.backgrounds = level_data.BACKGROUNDS.copy()
        for k, v in self.backgrounds.items():
            if v:
                self.background_images[k] = blackmango.scenery.Background(v)

        self.blockdata = level_data.BLOCKS
        self.mobdata = level_data.MOBS

        self.blocks = {}
        self.mobs = {}

        self.player = player

    def load(self):

        for coords, blockinfo in self.blockdata.items():
            x, y, z = coords
            id, args, kwargs = blockinfo
            material = MATERIALS[id]
            block = material(*args, **kwargs)
            self.set_block(block, x, y, z)

        for coords, mobinfo in self.mobdata.items():
            x, y, z = coords
            id, args, kwargs = mobinfo
            mob = MOBS[id]
            mob = mob(*args, **kwargs)
            self.set_mob(mob, x, y, z)

        # If the player object isn't present, ignore triggers, since this is
        # probably being loaded by the level editor.
        if self.player and not self.triggers.triggers_initialized:
            self.triggers.init_triggers(self, self.player)

    def get_background(self):
        return self.background_images.get(self.current_floor)

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
        try:
            return self.blocks[(x, y, floor)]
        except (IndexError, KeyError):
            if not self.player:
                # Return None if the player object is not present, since that
                # probably means this is being run in the level editor.
                return None
            if x < 0 or x > self.size[0] - 1 or \
               y < 0 or y > self.size[1] - 1 or \
               floor < 0 or floor > self.size[2] - 1:
                return MATERIALS[-1]()
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
        Return a string that represents the current level state.
        Saved level data should be identical in format to prepared level data.
        """
        blocks = {}
        mobs = {}
        
        for k, v in self.blocks.items():
            for idx, cls in MATERIALS.items():
                if cls and isinstance(v, cls):
                    break
            else:
                continue
            blocks[k] = (idx, v._args, v._kwargs)
        for k, v in self.mobs.items():
            for idx, cls in MOBS.items():
                if cls and isinstance(v, cls):
                    break
            else:
                continue
            mobs[k] = (idx, v._args, v._kwargs)

        saved_level = SavedLevel({
            "PLAYER_START": self.starting_location,
            "NAME": self.title_card,
            "BLOCKS": repr(blocks),
            "MOBS": repr(mobs),
            "BACKGROUNDS": self.backgrounds,
            "SIZE": self.size,
        })
        return repr(saved_level)

    def destroy(self):
        self.scheduled_destroy = True
        for lookuplist in [self.mobs, self.blocks]:
            for coords, sprite in lookuplist.items():
                sprite.delete()

class SavedLevel(object):
    """
    A simple object interface over the top of a dictionary for storing level
    values.
    """
    _d = {
        "SIZE": (0,0,0),
        "NAME": '',
        "LEVEL_NAME": '',
        "BACKGROUNDS": {},
        "PLAYER_START": (0,0,0),
        "BLOCKS": {},
        "MOBS": {},
        "TRIGGERS": None,
    }
    def __repr__(self):
        formatd = self._d.copy()
        for k, v in formatd.items():
            if v and isinstance(v, BasicLevelTriggers):
                formatd[k] = 'LevelTriggers'
            else:
                formatd[k] = pprint.pformat(v) or repr(type(v)())
        return blackmango.configure.LEVEL_TEMPLATE % formatd
    def __init__(self, dictionary = {}, level_ref = None):
        self.level_ref = level_ref
        self._d.update(dictionary)
    def __getattr__(self, k):
        return self._d[k]
    def __setattr__(self, k, v):
        self._d[k] = v
    def _update(self, dictionary):
        self._d.update(dictionary)

class BasicLevelTriggers(object):

    def __init__(self):
        self.triggers_initialized = False

    def init_triggers(self, level, player):
        self.triggers_initialized = True

    def tick(self, level, player):
        pass
