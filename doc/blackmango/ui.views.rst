:mod:`blackmango.ui.views` --- View objects
===========================================

.. automodule:: blackmango.ui.views

.. autoclass:: BaseView
    :members:
    :private-members:
    :special-members:


Derived views
-------------

The main views that are derived from this base class are as follows:

* :class:`blackmango.ui.views.credits.CreditsView` -- Handles the display of the
  scrolling credits screen.

* :class:`blackmango.ui.views.game.GameView` -- Main view while in-game.

* :class:`blackmango.ui.views.load_game.LoadGameView` -- Menu for selecting a
  game to load, accessed from the main menu.

* :class:`blackmango.ui.views.main_menu.MainMenuView` -- Main menu. This is the
  first views which is loaded on startup.