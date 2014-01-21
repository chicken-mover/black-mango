"""
This is the class that governs events in the level. Anything that triggers a
level-wide state change should call methods on the object that this class
produces.
"""

import blackmango.levels
import blackmango.ui

class LevelTriggers(blackmango.levels.BasicLevelTriggers):

    def tick(self, level, player):
        pass
