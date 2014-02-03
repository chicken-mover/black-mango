"""
These are tasks which must be run before anything else is executed.
"""

# Fix PIL import if Pillow is installed instead. This *must* happen before
# Pyglet is imported
import sys
try:
    import Image
except ImportError:
    from PIL import Image
    sys.modules['Image'] = Image