from .production import *
try:
    from .production import *
except ImportError:
    print('No local_settings.py was found. You must be on production.')
