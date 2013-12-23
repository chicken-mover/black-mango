
import pyglet

import blackmango.configure
import blackmango.sprites
mobs_batch = pyglet.graphics.Batch()


class BasicMobileSprite(blackmango.sprites.BaseSprite):
    
    def __init__(self, image = None,
            x = 0,
            y = 0,
            z = 0,
            color = None,
        ):

        color = color or (0,0,255,255)
        group = blackmango.configure.ORDERED_GROUPS.get('mobs')

        super(BasicMobileSprite, self).__init__(image, x, y, z,
                mobs_batch, group, color)

        self.is_solid = 1
        self.is_mover = 1
        self.is_portal = 0
        self.opacity = 0


class Player(BasicMobileSprite):

    current_level = None
    
    def __init__(self, x = 0, y = 0, z = 0):

        color = (0,255,0, 255)
        group = blackmango.configure.ORDERED_GROUPS.get('player')

        super(Player, self).__init__(None, x, y, z,
                color)

    def move(self, delta_x, delta_y, delta_z):

        dest = (
            self.world_location[0] + delta_x,
            self.world_location[1] + delta_y,
            self.world_location[2] + delta_z,
        )

        if self.current_level:
            block = self.current_level.get_block(*dest)
            print block
            if block and block.is_solid:
                return
            else:
                
                self.current_level.set_block(None, *self.world_location)
                self.current_level.set_block(self, *dest)
                self.world_location = dest
                self.translate()


MATERIALS = {
    0: None,
    1: blackmango.materials.Wall,
}
