
import commands
import setuptools
import sys

import blackmango.configure

version = blackmango.configure.VERSION

if __name__ == "__main__":

    ## This is being used mostly to track dependencies and automate testing. I
    ## don't ever anticipate releasing this project as open source, although we
    ## could at some point generalize it into a simpler framework that we do
    ## release.

    setuptools.setup(
        name = 'blackmango',
        version = version,
        py_modules = [
            'blackmango',
#            'blackmango_tests',
        ],
        install_requires = [
            'pyglet>=1.1.4',
            'xmltodict>=0.8.3',
        ],
#        tests_require = [
#            'mock>=1.0.1',
#            'nose>=1.3.0',
#        ],
        test_suite = 'nose.collector',
    )

    if len(sys.argv) > 1 and sys.argv[1] == 'develop':

        print "\nInstalling git hooks"
        stat, output = commands.getstatusoutput('bash scripts/install-hooks.sh')
        print output
        if stat != 0:
            print >>sys.stderr, "Git hook installation failed!"
