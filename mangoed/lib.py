
import re

def name_cleanup(name):
    """
    Simple pass of re.replace() to make sure that <name> conforms to the style
    and practical strictures of Python module names.
    """
    name = name.lower()
    name = re.sub(r'[^a-z0-9]', '_', name)
    if name[0].isdigit():
        raise ValueError('Name can\'t start with a number.')
    return name
