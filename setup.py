"""
Basic setup file. Temporary.
"""

import setuptools

version = '0.0.0'

if __name__ == "__main__":

    setuptools.setup(
        name = 'blackmango',
        version = '0.0.0',
        py_modules = [
            'blackmango',
            'blackmango_tests',
        ],
        install_requires = [
            'pyglet>=1.1.4',
        ],
        tests_require = [
            'mock>=1.0.1',
        ],
        test_suite = 'blackmango_tests.TestSuite',
    )
