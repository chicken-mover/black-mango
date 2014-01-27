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
    pass

class StairDown(blackmango.materials.BasePortalMaterial):
    opacity = 1
    pass

class Door(blackmango.materials.BasePortalMaterial):
    opacity = 1
    pass
