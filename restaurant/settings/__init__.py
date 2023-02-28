from .production import *
try:
    from .local_settings import *
except ImportError:
    print('No local_settings.py was found. You must be on production.')
