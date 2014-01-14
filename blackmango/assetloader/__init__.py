"""
Module for loading assets
"""

import os

import blackmango.system

def load_image(fname):
    return load('images', fname)

def load(asset_type, filename):
    path = os.path.join(blackmango.system.DIR_ASSETS, asset_type, filename)
    #print path
    if os.path.exists(path):
        return path
    else:
        return None
