
import re

def name_cleanup(name):
    name = name.lower()
    name = re.sub(r'[^a-zA-Z0-9]', '_', name)
    if name[0].isdigit():
        raise ValueError('Name can\'t start with a number.')