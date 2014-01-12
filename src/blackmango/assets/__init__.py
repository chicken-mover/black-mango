"""
Module for loading assets
"""

import os

import blackmango.utils

def load_image(fname):
    return load('images', fname)

def load(asset_type, filename):
    path = os.path.join(blackmango.utils.DIR_ASSETS, asset_type, filename)
    print path
    if os.path.exists(path):
        return path
    else:
        return None
