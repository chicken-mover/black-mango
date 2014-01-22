"""
This is the class that governs events in the level. Anything that triggers a
level-wide state change should call methods on the object that this class
produces.
"""

import blackmango.levels
import blackmango.ui

class LevelTriggers(blackmango.levels.BasicLevelTriggers):

    def init_triggers(self, level, player):
        from blackmango.mobs.patrollers import ClockwisePatroller
        
        ks = sorted(level.mobs.keys())
        d = [2, 1, 3, 4]
        x = 0
        for i, k in enumerate(ks):
            mob = level.mobs[k]
            if isinstance(mob, ClockwisePatroller):
                mob.turn(d[x])
                x += 1

        self.triggers_initialized = True

    def tick(self, level, player):
        pass
