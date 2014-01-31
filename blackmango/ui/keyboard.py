"""
A module for simplifying control binding and keyboard lookups
"""

import blackmango.ui

from pyglet.window import key

bindings = {

    # Movement and player control
    'switch_mask_1': [key._1, key.NUM_1],
    'switch_mask_2': [key._2, key.NUM_2],
    'switch_mask_3': [key._3, key.NUM_3],
    'switch_mask_4': [key._4, key.NUM_4],
    'switch_mask_5': [key._5, key.NUM_5],
    'switch_mask_6': [key._6, key.NUM_6],

    'move_up': [key.UP, key.NUM_UP, key.W],    
    'move_down': [key.DOWN, key.NUM_DOWN, key.S],    
    'move_left': [key.LEFT, key.NUM_LEFT, key.A],    
    'move_right': [key.RIGHT, key.NUM_RIGHT, key.D],    

    # Program control
    'game_quit': [key.ESCAPE],
    'game_save': [],
    'game_load': [],
    'prog_quit': [(key.Q, key.MOD_ACCEL|key.MOD_SHIFT),],

    # Menus
    'menu_select': [key.ENTER,],
    'menu_cancel': [key.ESCAPE,],
    'menu_move_up': [key.UP, key.NUM_UP],
    'menu_move_down': [key.DOWN, key.NUM_DOWN],
}

def check(binding):
    possible_keys = bindings.get(binding)
    for keyset in possible_keys:
        try:
            sym, mods = keyset
        except TypeError:
            sym = keyset
            mods = 0
        allk = [sym,]
        # TODO: the modifiers code isn't working properly
        mods = key.modifiers_string(mods)
        for m in filter(None, mods.split('|')):
            allk.append(getattr(key, m))
        pressedk = filter(lambda x: blackmango.ui.game_window.keyboard[x], allk)
        return pressedk == allk
