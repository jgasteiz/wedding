import os
from .settings import *

os.environ['CURRENT_VERSION_ID'] = '1'

EXCLUDED_MIDDLEWARE = [
    'djangae.contrib.security.middleware.AppEngineSecurityMiddleware',
]

MIDDLEWARE_CLASSES = tuple([m for m in MIDDLEWARE_CLASSES if m not in EXCLUDED_MIDDLEWARE])
