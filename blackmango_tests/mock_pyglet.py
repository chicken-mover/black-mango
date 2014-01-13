"""
A mocked Pyglet module for use with unit testing.

We have to mock certain internals for the app to run.
"""

import copy
import importlib
import mock
import pyglet
import sys
import time

mock_classes = [
    'pyglet.clock.ClockDisplay',
    'pyglet.graphics.Batch',
    'pyglet.graphics.OrderedGroup',
    'pyglet.image.SolidColorImagePattern',
    'pyglet.sprite.Sprite',
    #'pyglet.window.Window',
]

mock_functions = [
    'pyglet.clock.schedule_once',
]

automock_modules = [
    #'pyglet.window.key',
]

mocks = {
    'pyglet': pyglet,
    'pyglet.app': pyglet.app,
    'pyglet.clock': pyglet.clock,
    'pyglet.graphics': pyglet.graphics,
    'pyglet.image': pyglet.image,
    'pyglet.sprite': pyglet.sprite,
    #'pyglet.window': pyglet.window,
}

scheduled = set()

class EventLoopMock(object):

    def __init__(self):
        self._run = True

    def run(self):
        global scheduled
        while self._run:
            for f in scheduled:
                f(1)
            time.sleep(.5)

class WindowMock(mock.MagicMock):

    WINDOW_STYLE_BORDERLESS = 1

    def __init__(self, *args, **kwargs):
        super(WindowMock, self).__init__()

    def get_size(self):
        return (800, 800)

    def push_handlers(self, *args, **kwargs):
        pass

def schedule(f):
    global scheduled
    scheduled.add(f)

pyglet.clock.schedule = schedule

pyglet.app.EventLoop = EventLoopMock
pyglet.window.Window = WindowMock

class ExtendedMagicMock(mock.MagicMock):
    pass

def create_subclassable_mock(cls):
    """
    Given a class <cls>, create a mock that can be subclassed and instantiated.
    """
    mockcls = copy.deepcopy(ExtendedMagicMock)
    proplist = dir(cls)
    for prop in proplist:
        # Ignore magic methods and 'protected' props.
        if prop.startswith('_'):
            continue
        p = mock.create_autospec(getattr(cls, prop))
        setattr(mockcls, prop, p)
    return mockcls

def set_mockobj(module_name, parent_name, mock_name, mockobj):
    global mocks
    if module_name in mocks:
        mockedmod = mocks[module_name]
    else:
        mockedmod = mock.Mock()
        mocks[module_name] = mockedmod
    setattr(mockedmod, mock_name, mockobj)
    setattr(mocks[parent_name], module_name, mockedmod)


def patch():
    """
    Replace parts of the Pyglet module with mocks for testing.
    """
    global mocks, pyglet

    for name in mock_classes:
        parts = name.split('.')
        parent = '.'.join(parts[:-2])
        module = '.'.join(parts[:-1])
        clsname = parts[-1]

        m = importlib.import_module(module)
        cls = getattr(m, clsname)
        mockedcls = create_subclassable_mock(cls)

        set_mockobj(module, parent, clsname, mockedcls)

    for name in mock_functions:
        parts = name.split('.')
        parent = '.'.join(parts[:-2])
        module = '.'.join(parts[:-1])
        fname = parts[-1]

        m = importlib.import_module(module)
        fn = getattr(m, fname)
        mockedfn = mock.create_autospec(fn)

        set_mockobj(module, parent, fname, mockedfn)

    for name in automock_modules:

        parts = name.split('.')
        parent = '.'.join(parts[:-1])
        thisname = parts[-1]
        module = name

        m = importlib.import_module(module)
        mockedmod = mock.create_autospec(m)

        mocks[name] = mockedmod
        setattr(mocks[parent], thisname, mockedmod)

    sys.modules['pyglet'] = mocks['pyglet']
    pyglet = mocks['pyglet']
    
    return mocks['pyglet']
