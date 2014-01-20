"""
This is the class that governs events in the level. Anything that triggers a
level-wide state change should call methods on the object that this class
produces.
"""

import blackmango.levels
import blackmango.ui

class LevelTriggers(blackmango.levels.BasicLevelTriggers):

    def tick(self, level, player):
        if player.world_location == (1, 1, 2):
            # Make a call back to the GameView to trigger the next level
            blackmango.ui.game_window.view.next_level()