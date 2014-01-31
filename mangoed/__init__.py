"""
A really fuckin' basic level editor for Black Mango
"""

import argparse
import sys

ARGUMENTS = (
    ('filepath', {
        'help': 'Filepath to load on startup and write to on completion.'
                ' Without a file specified, the program will just dump the '
                'final output to stdout when it exits.'
    }),)

def main(data):
    print data
    return 1, ''

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=__doc__.strip())

    for name, argspec in ARGUMENTS:
        parser.add_argument(name, **argspec)

    args = parser.parse_args()

    with open(args.filepath, 'w+') as f:
        exitcode, data = main(f.read())
        if not exitcode:
            f.seek(0).write(data)
        else:
            sys.exit(exitcode)
