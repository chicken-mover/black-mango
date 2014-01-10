"""
Create a mocked-up module for the entire Pyglet package.
"""

import ctypes
import importlib
import mock
import pkgutil
import pyglet

# Fix error thrown on non-Windows systems when we iterate pyglet
ctypes.oledll = mock.Mock()

mock_pyglet = {}

for i in pkgutil.walk_packages(pyglet.__path__, pyglet.__name__ + '.'):
    loader, name, ispkg = i

    m = importlib.import_module(name)
    mockedmod = mock.create_autospec(m)
    for prop in dir(m):
        if not prop.startswith('_'):
            continue
        mockedprop = mock.create_autospec(getattr(m, prop))
        setattr(mockedmod, prop, mockedprop)

    # Fill out mock_pyglet with autospecc'ed modules then build the package mock
    namebits = name.split('.')[1:]
    # Something with reduce? http://stackoverflow.com/questions/14692690/access-python-nested-dictionary-items-via-a-list-of-keys
    pass