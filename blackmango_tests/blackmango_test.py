"""
This is where we will add all unit tests.

The `mock` module will allow us to replace Pyglet with a fake replacement that
we can inspect to ensure that it is being called correctly, without having to
actually fire up the GUI to run tests.

The hope is to eventually start using something like TravisCI to automate tests
on every commit.
"""

import unittest

# Global placeholder. Don't want to import this until setup is done.
blackmango = None
pyglet = None

class TestSuite(unittest.TestCase):
    
    def setUp(self):
        global blackmango
        global pyglet
        import blackmango
        import pyglet

    def test_startup(self):
        """
        Test that the startup sequence occurred correctly.
        """
        self.assertIsInstance(blackmango.blackmangoapp, pyglet.app.EventLoop)
        self.assertIsNotNone(blackmango.engine)
        self.assertIsInstance(blackmango.main_window, pyglet.window.Window)
