import os

from django.conf import settings
from django.test import TestCase, RequestFactory
from google.appengine.ext import testbed


sentinel = object()


class AppEngineTestCase(TestCase):
    _environ = {
        # Used by google.appengine.api.app_identity.
        'DEFAULT_VERSION_HOSTNAME': 'example.com',
    }
    # App Engine environ for the current user.
    _user_keys = ('USER_EMAIL', 'USER_ID', 'USER_IS_ADMIN')

    def setUp(self):
        super(AppEngineTestCase, self).setUp()

        self.factory = RequestFactory()

        self._save_user()

        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.setup_env(overwrite=True, **self._environ)
        self.testbed.init_app_identity_stub()
        self.testbed.init_user_stub()
        self.testbed.init_datastore_v3_stub(use_sqlite=True, datastore_file=':memory:')
        self.testbed.init_memcache_stub()
        self.testbed.init_urlfetch_stub()

        # in order for named queues to be able to run in unit tests we need
        # to update the test bed to know where to search for our queues.yaml
        # file.
        yaml_dir = os.path.abspath(os.path.join(settings.BASE_DIR, os.pardir))
        self.testbed.init_taskqueue_stub(root_path=yaml_dir)

    def tearDown(self):
        self.testbed.deactivate()
        self._restore_user()
        super(AppEngineTestCase, self).tearDown()

    def login(self, email, user_id=None, is_admin=False):
        """Set the current Google authenticated user by email address.

        Use is_admin=True to set them as an App Engine admin.
        """
        user_id = user_id or email.split('@', 1)[0]
        os.environ['USER_EMAIL'] = email
        os.environ['USER_ID'] = user_id
        os.environ['USER_IS_ADMIN'] = '1' if is_admin else '0'

    def logout(self):
        for key in self._user_keys:
            del os.environ[key]

    def _save_user(self):
        self._userenv = {k: os.environ.get(k, sentinel) for k in self._user_keys}

    def _restore_user(self):
        for key, value in self._userenv.items():
            if value is not sentinel:
                os.environ[key] = value
