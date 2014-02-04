"""
Materials for rooms and buildings.
"""

import blackmango.materials

img_brick = blackmango.assetloader.load_image('placeholders/brick.gif')
img_platform = blackmango.assetloader.load_image('placeholders/platform.gif')

class Wall(blackmango.materials.BaseMaterial):
    def __init__(self, x, y, z):
        super(Wall, self).__init__(img_brick, x, y, z)
        self.opacity = 1

class StairUp(blackmango.materials.BasePortalMaterial):
    def __init__(self, x, y, z, destination = (0,0,0)):
        super(StairUp, self).__init__(None, x, y, z, destination = destination)
        self.opacity = 1

class StairDown(blackmango.materials.BasePortalMaterial):
    def __init__(self, x, y, z, destination = (0,0,0)):
        super(StairDown, self).__init__(None, x, y, z, destination = destination)
        self.opacity = 1

class Door(blackmango.materials.BasePortalMaterial):
    def __init__(self, x, y, z, destination = (0,0,0)):
        super(Door, self).__init__(None, x, y, z, destination = destination)
        self.opacity = 1


class Platform(blackmango.materials.BaseMaterial):
    def __init__(self, x, y, z):
        super(Platform, self).__init__(img_platform, x, y, z)
        self.is_solid = False
        self.world_height = 1
