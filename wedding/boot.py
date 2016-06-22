import sys
from os.path import dirname, abspath, join, exists

PROJECT_DIR = dirname(dirname(abspath(__file__)))
SITEPACKAGES_DIR = join(PROJECT_DIR, "sitepackages")
APPENGINE_DIR = join(SITEPACKAGES_DIR, "google_appengine")


def fix_path():
    if exists(APPENGINE_DIR) and APPENGINE_DIR not in sys.path:
        sys.path.insert(1, APPENGINE_DIR)

    if SITEPACKAGES_DIR not in sys.path:
        sys.path.insert(1, SITEPACKAGES_DIR)


def get_app_config():
    """Returns the application configuration, creating it if necessary."""
    from django.utils.crypto import get_random_string
    from google.appengine.ext import ndb

    class Config(ndb.Model):
        """A simple key-value store for application configuration settings."""
        secret_key = ndb.StringProperty()

    # Create a random SECRET_KEY hash
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    secret_key = get_random_string(50, chars)

    key = ndb.Key(Config, 'config')
    entity = key.get()
    if not entity:
        entity = Config(key=key)
        entity.secret_key = str(secret_key)
        entity.put()
    return entity

def register_custom_checks():
    from . import checks
    from django.core.checks import register, Tags
    register(checks.check_csp_sources_not_unsafe, Tags.security, deploy=True)
    register(checks.check_session_csrf_enabled, Tags.security)
    register(checks.check_csp_is_not_report_only, Tags.security)
