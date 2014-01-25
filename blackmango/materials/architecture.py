"""
Materials for rooms and buildings.
"""

import blackmango.materials

img_brick = blackmango.assetloader.load_image('placeholders/brick.gif')

class Wall(blackmango.materials.BaseMaterial):
    def __init__(self, x, y, z):
        super(Wall, self).__init__(img_brick, x, y, z)

class StairUp(blackmango.materials.BasePortalMaterial):
    pass

class StairDown(blackmango.materials.BasePortalMaterial):
    pass

class Door(blackmango.materials.BasePortalMaterial):
    pass
