"""
This should be pretty self-explanitory. This format may end up not being fit
for purpose, but I'm gunning for something easy to write when it comes time to
start doing intensive level building.

Somehow we will need to work in level scripting as well, possibly as a seperate
LevelBehavior class?
"""

from blackmango.levels.test_level2.triggers import LevelTriggers

LEVEL_DATA = {

    'title_card': 'The Inner Court',

    # X, Y, Z
    'level_size': (10, 10, 1),
    'starting_location': (5, 5, 0),

    'next_level': None,
    'previous_level': None,

    'triggers': LevelTriggers(),

    'blocks': {
    
        0: [
      
            [1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
            [0, 1, 1, 0, 0, 0, 0, 1, 1, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 1, 1, 0, 0, 0, 0, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            
        ],

    },

    'mobs': {
    
        0: [
      
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            
        ],

    },

}
