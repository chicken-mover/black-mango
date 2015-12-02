
import commands
import os
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
            'mangoed',
        ],
        packages = setuptools.find_packages(exclude = ['blackmango_tests']),
        test_suite = 'nose.collector',
    )

    try:
        
        if len(sys.argv) > 1 and sys.argv[1] == 'develop' and os.uname():

            print "\nInstalling git hooks"
            stat, output = commands.getstatusoutput('bash scripts/install-hooks.sh')
            print output
            if stat != 0:
                print >>sys.stderr, "Git hook installation failed!"

    except AttributeError:
        # Non-Cygwin Windows environment
        print >>sys.stderr, """
WARNING: Can't auto-install git hooks, because this is a non-Cygwin Windows
         environment.
"""
