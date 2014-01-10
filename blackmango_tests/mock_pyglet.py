"""
Create a mock module for the entire Pyglet package.
"""

import ctypes
import mock
import pyglet

# Fix error thrown on non-Windows systems when we iterate pyglet
ctypes.oledll = mock.Mock()

mock_pyglet = {}

for i in pkgutil.walk_packages(pyglet.__path__, pyglet.__name__ + '.'):
    loader, name, ispkg = i
    # Fill out mock_pyglet with autospecc'ed modules then build the package mock