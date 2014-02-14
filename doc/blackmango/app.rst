:mod:`blackmango.app` --- Main application event loop management
=====================================================

.. automodule:: blackmango.app

.. autofunction:: init

.. autoclass:: BlackMangoApp
    :members:
    :private-members:
    :special-members:

    .. method:: run

        Inherited from :class:`pyglet.app.EventLoop`. Starts the repeating event
        loop until it is stopped with :meth:`exit` (which is what
        :meth:`user_quit` calls).