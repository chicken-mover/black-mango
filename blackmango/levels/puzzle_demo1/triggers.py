"""
This is the class that governs events in the level. Anything that triggers a
level-wide state change should call methods on the object that this class
produces.
"""

import blackmango.levels
import blackmango.ui

class LevelTriggers(blackmango.levels.BasicLevelTriggers):

    def __init__(self): 
        self.triggers_initialized = False
    
    def init_triggers(self, level, player):
        from blackmango.mobs.patrollers import ClockwisePatroller
        
        ks = sorted(level.mobs.keys())
        d = [2, 1, 3, 4]
        x = 0
        for i, k in enumerate(ks):
            mob = level.mobs[k]
            if isinstance(mob, ClockwisePatroller) and mob.world_location[2] == 0:
                mob.turn(d[x])
                x += 1

        self.triggers_initialized = True

    def tick(self, level, player):
        if player.world_location[0]&1:
            import blackmango.ui.labels
            if hasattr(self, 'title') and self.title:
                self.title.delete()
#            self.title = blackmango.ui.labels.TextBox('Testing', position = 'bottom')
