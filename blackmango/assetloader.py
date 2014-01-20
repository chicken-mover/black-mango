"""
Module for loading assets
"""

import os
import pyglet
import xmltodict

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
            blackmango.configure.logger.debug(" - loading %s" % fontfile)
            pyglet.font.add_file(fontfile)

def load_colordata():
    f = os.path.join(blackmango.system.DIR_ASSETS, 'colorscheme.xml')
    blackmango.configure.logger.debug(" - loading %s" % f)
    outcolors = {}
    with open(f) as fd:
        d = fd.read()
        colordata = xmltodict.parse(d)
        palette = colordata.get('palette')
        colorsets = palette.get('colorset')
        for colorset in colorsets:
            if hasattr(colorset, 'items'):
                colors = colorset.get('color')
                for c in colors:
                    rgba = [int(i) for i in \
                                (c.get('@r'), c.get('@g'), c.get('@b'), '255')]
                    outcolors[c.get('@id')] = tuple(rgba)
    return outcolors

def load(asset_type, filename):
    path = os.path.join(blackmango.system.DIR_ASSETS, asset_type, filename)
    if os.path.exists(path):
        return path
    else:
        return None
