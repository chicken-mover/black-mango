"""
Materials for rooms and buildings.
"""

import blackmango.materials

class Wall(blackmango.materials.BaseMaterial):
    pass

class StairUp(blackmango.materials.BasePortalMaterial):
    pass

class StairDown(blackmango.materials.BasePortalMaterial):
    pass

class Door(blackmango.materials.BasePortalMaterial):
    pass