"""
Materials for rooms and buildings.
"""

import blackmango.materials

img_brick = blackmango.assetloader.load_image('placeholders/brick.gif')

class Wall(blackmango.materials.BaseMaterial):
    opacity = 1
    def __init__(self, x, y, z):
        super(Wall, self).__init__(img_brick, x, y, z)

class StairUp(blackmango.materials.BasePortalMaterial):
    opacity = 1
    def __init__(self, x, y, z, destination):
        super(StairUp, self).__init__(None, x, y, z, destination = destination)

class StairDown(blackmango.materials.BasePortalMaterial):
    opacity = 1
    def __init__(self, x, y, z, destination):
        super(StairDown, self).__init__(None, x, y, z, destination = destination)

class Door(blackmango.materials.BasePortalMaterial):
    opacity = 1
    def __init__(self, x, y, z, destination):
        super(Door, self).__init__(None, x, y, z, destination = destination)
