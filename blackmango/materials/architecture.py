"""
Materials for rooms and buildings.
"""

import blackmango.materials

class Wall(blackmango.materials.BaseMaterial):
    def __init__(self, x, y, z):
        image = blackmango.assetloader.load_image('placeholders/brick.gif')
        super(Wall, self).__init__(image, x, y, z)

class StairUp(blackmango.materials.BasePortalMaterial):
    pass

class StairDown(blackmango.materials.BasePortalMaterial):
    pass

class Door(blackmango.materials.BasePortalMaterial):
    pass
