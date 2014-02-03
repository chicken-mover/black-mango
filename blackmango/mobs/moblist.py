
import blackmango.mobs
import blackmango.mobs.dancers
import blackmango.mobs.patrollers
import blackmango.sprites

MOBS = {
    0: None,
    1: blackmango.mobs.SimpleMob,
    2: blackmango.mobs.patrollers.PatrollerV,
    3: blackmango.mobs.patrollers.ClockwisePatroller,
    4: blackmango.mobs.patrollers.Chaser,
    5: blackmango.mobs.dancers.Mirror,
}

# Wrap the __init__ functions of each class so that we can easily retrieve the
# settings they were initialized with.
for v in MOBS.values():
    if v:
        v.__init__ = blackmango.sprites.storecall(v.__init__)


