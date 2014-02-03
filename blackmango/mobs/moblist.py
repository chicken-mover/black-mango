
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

for v in MOBS.values():
    v.__init__ = blackmango.sprites.storecall(v.__init__)


