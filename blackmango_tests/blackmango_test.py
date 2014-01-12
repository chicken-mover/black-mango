"""
This is where we will add all unit tests.

The `mock` module will allow us to replace Pyglet with a fake replacement that
we can inspect to ensure that it is being called correctly, without having to
actually fire up the GUI to run tests or deal with Pyglet's poor threading
compatability.

The hope is to eventually start using something like TravisCI to automate tests
on every commit.
"""

import threading
import time
import unittest

import blackmango_tests.mock_pyglet

# Placeholder until the mock has been created
blackmango = None
pyglet = None


class AppTestSuite(unittest.TestCase):
    
    def setUp(self):
        """
        Set up the app and test that the startup sequence occurred correctly.
        """
        global pyglet, blackmango
        blackmango_tests.mock_pyglet.patch()
        import blackmango.app
        patcher = mock.patch.object(blackmango.app.BlackMangoApp, '__bases__', (mock.Mock,))
        patcher.is_local = True
        import pyglet
        import blackmango
        self.assertIsInstance(blackmango.blackmangoapp, pyglet.app.EventLoop)
        self.assertIsNotNone(blackmango.engine)
        self.assertIsInstance(blackmango.main_window, pyglet.window.Window)
        blackmango.blackmangoapp.run()
        #self.appthread = threading.Thread(
        #        target = blackmango.blackmangoapp.run)
        self.appthread.start()
        self.assertTrue(self.appthread.is_alive())

    def test_game_start(self):
        """
        Run the user input for starting a new game
        """
        blackmango.main_window.keyboard[pyglet.window.key.N] = True
        time.sleep(1)
        blackmango.main_window.keyboard[pyglet.window.key.N] = False
        self.assertEqual(blackmango.main_window.mode, 'game')
