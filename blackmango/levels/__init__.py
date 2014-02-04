"""
A simple level object for loading level data and tracking stuff that's
happening inside the level.

This class also controls what part of the level we're looking at at any given
moment, and keeps references to mobs and blocks for quick collision lookup.

The level's `tick` method is used to iterate and call the `behavior` method on
each mob in the level.
"""

import pprint

import blackmango.materials
import blackmango.scenery
import blackmango.sprites

from blackmango.materials.materiallist import MATERIALS
from blackmango.mobs.moblist import MOBS

class BasicLevel(object):

    # Blocks and mobs are tracked seperately. I don't know if this is a good
    # idea or a terrible one. It seems like it might not be super extensible in
    # the future, because it means not having more than one mob at each world
    # location, but we can always change it in the future.

    def __init__(self, level_data, player = None):
        """
        Read in the level data, and translate the lists of block ids in the
        room data into instances of materials classes.
        """

        self.init_data = level_data

        self.current_room = level_data.PLAYER_START[2]
        self.size = level_data.SIZE

        self.scheduled_destroy = False
        
        # Probably being loaded by the level editor. Ignore triggers
        if level_data.TRIGGERS:
            self.triggers = level_data.TRIGGERS()

        self.background_images = {}
        for k, v in level_data.BACKGROUNDS.items():
            if v:
                # Make only one Background object per image, to keep things
                # reasonably efficient.
                img_values = self.background_images.values()
                existing = filter(lambda x: x.image == v, img_values)
                if len(existing):
                    self.background_images[k] = existing[0]
                else:
                    self.background_images[k] = blackmango.scenery.Background(v)

        self.blocks = {}
        self.mobs = {}

        self.player = player

    def load(self):

        for data, lookuplist in [
            (self.init_data.BLOCKS, MATERIALS)
            (self.init_data.MOBS, MOBS)
        ]:
            for coords, blockinfo in data.items():
                id, args, kwargs = blockinfo
                sprite = lookuplist[id]
                sprite = sprite(*args, **kwargs)
                self.set_sprite(sprite, coords)

        # If the player object isn't present, ignore triggers, since this is
        # probably being loaded by the level editor.
        if self.player and not self.triggers.triggers_initialized:
            self.triggers.init_triggers(self, self.player)

    def get_background(self):
        """
        Get the background object for the current room
        """
        return self.background_images.get(self.current_room)

    def switch_room(self, new_z):
        """
        Set which room we're in. This currently iterates every block and mob
        for the current and new room, and re-sets their visibility flag as
        appropriate.
        """
        for f in [self.blocks, self.mobs]:
            for z in [self.current_room, new_z]:
                items = filter(lambda s: s[0][2] == z, f.items())
                for k, m in items:
                    if z != new_z:
                        m.visible = False
                    else:
                        m.visible = True
        self.current_room = new_z


    def set_sprite(self, sprite, coords, translate = True):
        """
        Set the location of a material block or mob for quick collision lookup.
        """
        if not (isinstance(coords, (tuple, list)) and len(coords) == 3):
            raise ValueError("'coords' must be a tuple or list of "
                    "three coordinates")
                    
        if isinstance(sprite, blackmango.materials.BaseMaterial):
            d = self.blocks
        elif isinstance(sprite, blackmango.sprites.BasicMobileSprite):
            d = self.mobs

        if coords in d:
            raise ValueError("Cannot set %s to %s, an object of "
                "the same tracked class exists there already" % \
                sprite, coords)
        else:
            # If the sprite exists in another location, clear the index
            for k, v in d.items():
                if v is sprite:
                    del d[k]
            # Set the new index and update the sprite's world_location attrib.
            d[coords] = sprite
            sprite.world_location = coords
            # If it's the player, the view moves with the sprite. Otherwise we
            # hide it when it goes off screen.
            if sprite is self.player:
                self.switch_room(coords[2])
            else:
                sprite.visible = coords[2] == self.current_room
            if translate:
                sprite.translate()

    def get_sprites(self, coords):
        """
        Get the existing material block and mob at the specified location,
        returned as a 2-tuple of (block, mob). If either (or both) don't exist,
        their value will be returned as None, or, in the case of material
        blocks, as a VoidMaterial when the specified coordinates are out of
        bounds.
        """
        if not (isinstance(coords, (tuple, list)) and len(coords) == 3):
            raise ValueError("'coords' must be a tuple or list of "
                    "three coordinates")

        block, mob = self.blocks.get(coords), self.mobs.get(coords)
        if block is None and (self.player):
            x, y, z = coords
            # If we're retriveing a material that's out of bounds,
            # return an instance of VoidMaterial
            if x < 0 or x > self.size[0] - 1 or \
               y < 0 or y > self.size[1] - 1 or \
               z < 0 or z > self.size[2] - 1:
                block = MATERIALS[-1]()

        return block, mob

    def tick(self):
        """
        Called by the window object, this method calls individual mob behvaiour
        ticks and level trigger ticks
        """
        if self.scheduled_destroy:
            return
        for _, mob in self.mobs.items():
            if mob is not self.player:
                mob.do_behavior()
        self.triggers.tick(self, self.player)

    def serialize(self):
        """
        Return a string that represents the curret level state.
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
            "NAME": self.init_data.NAME,
            "BACKGROUNDS": self.init_data.BACKGROUNDS,
            "PLAYER_START": self.init_data.PLAYER_START,
            "BLOCKS": repr(blocks),
            "MOBS": repr(mobs),
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
