Getting started with Black Mango
================================

Setting up a development environment
------------------------------------

Requirements
~~~~~~~~~~~~

Before you start developming Black Mango you will need to satisfy the following
requirements:

+ You should be working in an environment that has bash available (if you want
  any of the included scripts to work). If you are on Windows, Cygwin is fine.
+ Python 2.7 must be installed and available in your ``$PATH`` as either
  ``python``, ``python2`` or ``python2.7``. The scripts will attempt to select
  the proper executable automatically.
+ You will need a version of
  `Python Image Library <http://www.pythonware.com/products/pil/>`_ installed.
  The  `Pillow <https://pypi.python.org/pypi/Pillow/>`_ fork is fine (this is
  the version of PIL that gets installed if you do
  ``sudo pacman -S python2-imaging`` on Arch Linux). Most flavors of Linux have
  a version of PIL in their repositories (although on distros that use Python 3
  as the default, you will need to specify the Python 2 version of the package).
  Failing that, ``sudo pip install pillow`` should sort you out.
+ The `setuptools 
  <https://pythonhosted.org/setuptools/setuptools.html#installing-setuptools>`_
  module should be installed before you begin. (``sudo pip install setuptools``)

Setup instructions
~~~~~~~~~~~~~~~~~~

The first step is to clone the repository from Github:

.. code-block:: bash

    $ git clone git@github.com:chicken-mover/black-mango.git

You will then want to install the project as a development module:

.. code-block:: bash

    $ cd black-mango
    $ sudo python2.7 setup.py develop

Optionally, you can activate the project's custom git hooks by doing the
following:

.. code-block:: bash

    $ cd .git
    $ mv hooks hooks-backup
    $ ln -s ../scripts/hooks hooks
    $ chmod u+x hooks/*


Building distributions
~~~~~~~~~~~~~~~~~~~~~~

This section will be fleshed out when it comes time to actually work on
distribution stuff.


Structure of the code
---------------------

How the engine works
--------------------

User interface and input
~~~~~~~~~~~~~~~~~~~~~~~~

Levels and level triggers
~~~~~~~~~~~~~~~~~~~~~~~~~

Sprites and rendering
~~~~~~~~~~~~~~~~~~~~~