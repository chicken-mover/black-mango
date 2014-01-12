"""
This module's patch() function will cause all subsequent Pyglet imports in the
process to return a mocked version of Pyglet. This is to allow for testing,
when we might want to inspect how Pyglet is being called, but we don't want it
to actually draw any graphics or do any work.

In order for this to work, mock_pyglet must be imported and patch() called
before any Pyglet imports are called.

>>> import mock_pyglet
>>> mock_pyglet.patch()
>>> import pyglet
>>> print repr(pyglet)
<Mock id='167071564'>
>>> a = pyglet.sprites.Sprite()
>>> print repr(a)
<Mock name='mock.sprites.Sprite()' id='167050604'>
"""

import ctypes
import importlib
import mock
import pkgutil
import pyglet
import re
import sys
import time

def patch(print_debug = False):
    if print_debug:
        print "Generating a mocked Pyglet module, please be patient ..."
        time.sleep(2)

    try:
        # If we come to rely on PIL we should take this out
        import Image
    except ImportError:
        Image = None

    # Fix error thrown on non-Windows systems when we iterate pyglet
    #ctypes.oledll = mock.Mock()

    mocks = {
        'pyglet': mock.Mock()        
    }

    for i in pkgutil.walk_packages(pyglet.__path__, pyglet.__name__ + '.'):
        loader, name, ispkg = i
        #print name

        # Platform-specific stuff will, naturally, fail across platforms as we try
        # to blindly import it with pkgutil. Instead, skip the platform specific
        # stuff that the app shouldn't be calling anyway.
        #
        # This module will have to be run on several different setups before this
        # list is definitive, because I'm too lazy to dig through all of Pyglet's
        # code to do it in advance.
        #
        # If we end up needing some of these missing, unmocked modules for testing,
        # probably best to put them back in manually.
        #
        if 'win32' in name or 'carbon' in name or \
           'media.drivers' in name or \
           name.startswith('pyglet.gl.') or \
           name.startswith('pyglet.com') or \
           name.endswith('.gdiplus') or \
           name.endswith('.quicktime') or \
           name.endswith('.avbin') or \
           (not Image and '.pil' in name):
            if print_debug:
                print "  (Skipping", name, ")"
            continue

        m = importlib.import_module(name)
        mockedmod = mock.create_autospec(m)
        c = 0
        for prop in dir(m):
            # Don't mock 'private' props or 'constant' props
            if prop.startswith('_'):
                continue
            if re.match(r'[A-Z_]+', prop):
                continue
            # There are eight bajillion glSometing props, none of which need a mock
            if re.match(r'gl[A-Za-z0-9]+', prop):
                continue
            if print_debug:
                print '  -',prop
            mockedprop = mock.create_autospec(getattr(m, prop))
            setattr(mockedmod, prop, mockedprop)
            c += 1
        if print_debug:
            print "  Set %s mocked props" % c

        mocks[name] = mockedmod

        hierarchy = name.split('.')
        thisname = hierarchy[-1]
        parent = '.'.join(hierarchy[:-1])
        if parent in mocks:
            setattr(mocks[parent], thisname, mockedmod)

    mock_pyglet = mocks['pyglet']
    sys.modules['pyglet'] = mock_pyglet
