"""
Module for loading assets
"""

import os
import pyglet

import blackmango.configure
import blackmango.system

def load_image(fname):
    return load('images', fname)

def load_text(fname):
    p = load('text', fname)
    return open(p).read()

def load_fonts():
    fontsdir = os.path.join(blackmango.system.DIR_ASSETS, 'fonts')
    for dirpath, dirnames, filenames in os.walk(fontsdir):
        for f in filenames:
            if not f.endswith('.ttf'):
                continue
            fontfile = os.path.join(dirpath, f)
            blackmango.configure.logger.info("- loading %s" % fontfile)
            pyglet.font.add_file(fontfile)


def load(asset_type, filename):
    path = os.path.join(blackmango.system.DIR_ASSETS, asset_type, filename)
    #print path
    if os.path.exists(path):
        return path
    else:
        return None
