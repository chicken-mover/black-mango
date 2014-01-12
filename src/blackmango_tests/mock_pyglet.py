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

The patch() function is aware of whether it has been called before, and
will return immediately if Pyglet has already been mocked.
"""

import ctypes
import importlib
import inspect
import mock
import pkgutil
import pyglet
import re
import sys
import time

__all__ = ['__patch__']

class ExtendedMagicMock(mock.MagicMock):

    def __init__(self, *args, **kwargs):
        # Absorb whatever weird args and kwargs the app will try to instatiate
        # these classes with.
        super(ExtendedMagicMock, self).__init__()
        

def patch(print_debug = False):
    """
    Obtain a spec of the `pyglet` package recursively, and replace it with a
    series of `mock.create_autospec()`-generated Mock objects.

    May be called as many times as desired, as this function will return
    immediately if it detects that Pyglet has already been mocked.
    """
    global pyglet

    if isinstance(pyglet, mock.Mock):
        if print_debug:
            print "Pyglet has already been mocked, skipping patch."
        return

    if print_debug:
        print "Generating a mocked Pyglet module, please be patient ..."
        time.sleep(2)

    try:
        # If we come to rely on PIL we should take this out
        import Image
    except ImportError:
        Image = None

    # Fix error thrown on non-Windows systems when we iterate pyglet
    ctypes.oledll = mock.Mock()

    mocks = {
        'pyglet': mock.Mock()        
    }

    for i in pkgutil.walk_packages(pyglet.__path__, pyglet.__name__ + '.'):
        loader, name, ispkg = i
        if print_debug:
            print name

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
            if re.match(r'^[A-Z_]+$', prop) or prop.startswith('c_') or \
               prop.startswith('struct_'):
                if print_debug:
                    print "    (Skipping c/const/struct prop %s)" % prop
                continue
            # There are eight bajillion glSometing props, none of which need a mock
            if re.match(r'gl[A-Za-z0-9]+', prop):
                continue
            p = getattr(m, prop)
            # Pyglet submodules will get loaded as we iterate. Builtins and
            # foreign modules shouldn't be mocked, as they won't be accessed
            # by our program via this package.
            if inspect.isbuiltin(p) or inspect.ismodule(p):
                if print_debug:
                    print "    (Skipping builtin or module %s)" % prop
                continue
            if print_debug:
                print '  -',prop
            if inspect.isclass(p):
                # If it's a class, don't instantiate a mock
                mockedprop = ExtendedMagicMock
                # We still have to mock individual properties if they aren't
                # callables
                for subprop in dir(p):
                    if subprop.startswith('_'):
                        continue
                    sp = getattr(p, subprop)
                    if callable(sp):
                        continue
                    setattr(mockedprop, subprop, mock.create_autospec(sp))
            else:
                mockedprop = mock.create_autospec(p)
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
    pyglet = mock_pyglet
