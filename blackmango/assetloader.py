"""
This module provides utility functions for loading static assets from the
project's asset directory tree.

.. _asset-tree:

The asset directory structure
-----------------------------

All assets belong in the ``asset`` directory, which should reside next to the
main source directory.

The overall structure looks like this:

.. code-block:: text

    black-mango/                    Top-level tree
        assets/
            fonts/                  One directory per font, with a TTF file in
                                    each font directory.
                chapbook/
                    Chapbook.ttf
                    ...
                prociono/
                    ...
            images/                 The image organization is generally
                                    arbitrary, but you should try to follow the
                                    format already preent.
                placeholders/       Temporary images
                levels/             Level-specific images, like backgrounds and
                    <level-name-1>/ scenery
                    <level-name-2>/
                materials/          Material/architectural
                mobs/               Mob sprites
                player/             Player sprites
                ...
            text/                   Text files used inside the program
                credits.html
                ...
        blackmango/                 Python source files
            ...


Module contents
-----------------------------
"""

import os
import pyglet
import xmltodict

import blackmango.configure
import blackmango.system

def load_image(fname):
    """
    Return a Pyglet image object loaded from the file specified by *fname*. The
    path specified by *fname* should be relative to the image asset directory.
    For example, a player sprite might be specified as
    ``'player/somesprite.png'``.
    """
    return pyglet.image.load(load('images', fname))

def load_text(fname):
    """
    Load a text file and return its contents. The path specified by **fname** is
    relative to the text asset directory.
    """
    p = load('text', fname)
    return open(p).read()

def load_fonts():
    """
    Install fonts so that Pyglet can use them. This walks the font asset
    directory and loads every TTF file it finds using
    :py:func:`pyglet.font.add_file`.
    """
    fontsdir = os.path.join(blackmango.system.DIR_ASSETS, 'fonts')
    for dirpath, dirnames, filenames in os.walk(fontsdir):
        for f in filenames:
            if not f.endswith('.ttf'):
                continue
            fontfile = os.path.join(dirpath, f)
            blackmango.configure.logger.debug(" - loading %s" % fontfile)
            pyglet.font.add_file(fontfile)

def load_colordata():
    """
    Parse the colorscheme.xml asset (in the top level of the asset directory
    tree) and return the colors as a simplified Python dict. This is basically
    just here so that colors can be conveniently shared and updated from one
    file, rather than having to manually maintain RGB hex values in the source
    code.
    """
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
    """
    Generic load function to simplify grabbing file paths by asset type.
    *asset_type* specifies the first directory within assets to look in, and
    *filename* specifies the remainder of the path.

    Returns an absolute path to the resource, or None if it does not exist.
    """
    path = os.path.join(blackmango.system.DIR_ASSETS, asset_type, filename)
    if os.path.exists(path):
        return path
    else:
        return None
