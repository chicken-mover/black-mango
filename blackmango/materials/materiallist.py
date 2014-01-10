
import blackmango.materials
import blackmango.materials.architecture

# Global dict for lookups by the levels module
MATERIALS = {
    -1: blackmango.materials.VoidMaterial,
    0: None,
    1: blackmango.materials.architecture.Wall,
    7: blackmango.materials.architecture.Door,
    8: blackmango.materials.architecture.StairUp,
    9: blackmango.materials.architecture.StairDown,
}
