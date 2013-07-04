import random
from string import letters
from time import sleep

from django import test
from django.conf import settings
from django.contrib.auth.models import User

import test_utils
import elasticutils.contrib.django.estestcase as estestcase

from mozillians.users.cron import index_all_profiles
from mozillians.users.models import MOZILLIANS, PUBLIC, UserProfile


class TestCase(test_utils.TestCase):
    """Tests for common package."""

    def setUp(self):
        # TODO: can this be more elegant?
        self._AUTHENTICATION_BACKENDS = settings.AUTHENTICATION_BACKENDS
        settings.AUTHENTICATION_BACKENDS = [
            'mozillians.common.backends.TestBackend']
        settings.ES_INDEXES = {'default': 'mozillians-test',
                               'public': 'mozillians-public-test'}
        settings.ES_DISABLED = True
        settings.ES_TIMEOUT = 60


        # Create a Mozillian
        self.mozillian = User.objects.create(
                email='u000001@mozillians.org', username='7f3a67u000001')
        profile = self.mozillian.get_profile()
        profile.is_vouched = True
        profile.full_name='Amandeep McIlrath'
        profile.save()

        # Create another Mozillian
        self.mozillian2 = User.objects.create(
                email='u000002@mozillians.org', username='7f3a67u000002')
        profile = self.mozillian2.get_profile()
        profile.is_vouched = True
        profile.full_name='Amando Brown'
        profile.privacy_full_name = PUBLIC
        profile.save()

        # Create a non-vouched account
        self.pending = User.objects.create(
                email='pending@mozillians.org', username='pending')
        pending_profile = self.pending.get_profile()
        pending_profile.full_name='Amanda Younger'
        pending_profile.privacy_full_name = PUBLIC
        pending_profile.save()

        # Create an incomplete account
        self.incomplete = (
            User.objects.create(email='incomplete@mozillians.org',
                                username='incomplete'))

        self.client.get('/')
        self.mozillian_client = test.Client()
        self.mozillian_client.login(email=self.mozillian.email)
        self.mozillian2_client = test.Client()
        self.mozillian2_client.login(email=self.mozillian2.email)
        self.pending_client = test.Client()
        self.pending_client.login(email=self.pending.email)
        self.incomplete_client = test.Client()
        self.incomplete_client.login(email=self.incomplete.email)
        self.anonymous_client = test.Client()
        self.data_privacy_fields = {}
        for field in UserProfile._privacy_fields:
            self.data_privacy_fields['privacy_%s' % field] = MOZILLIANS

    def tearDown(self):
        super(TestCase, self).tearDownClass()
        if getattr(self, '_AUTHENTICATION_BACKENDS', None):
            settings.AUTHENTICATION_BACKENDS = self._AUTHENTICATION_BACKENDS
        User.objects.all().delete()


class ESTestCase(TestCase, estestcase.ESTestCase):

    @classmethod
    def setUpClass(cls):
        """Runs the :class:`TestCase` setup to add some data.

        Also re-creates indexes respecting data mappings, flushes and
        refreshes the data so it's searchable via computer.

        """
        estestcase.ESTestCase.setUpClass()
        TestCase.setUpClass()

        # Add on demand more models here.
        index_all_profiles()

        # Allow time for ES to index stuff
        sleep(1)

    @classmethod
    def tearDownClass(cls):
        TestCase.tearDownClass()
        estestcase.ESTestCase.tearDownClass()


def user(**kwargs):
    """Return a user with all necessary defaults filled in.

    Default password is 'testpass' unless you say otherwise in a
    kwarg.

    """
    save = kwargs.pop('save', True)
    is_vouched = kwargs.pop('is_vouched', None)
    vouched_by = kwargs.pop('vouched_by', None)
    defaults = {}
    defaults['username'] = kwargs.get('username',
                                      ''.join(random.choice(letters)
                                              for x in xrange(15)))
    defaults['email'] = kwargs.get(
        'email', ''.join(
            random.choice(letters) for x in xrange(10)) + '@example.com')
    u = User(**defaults)
    u.set_password(kwargs.get('password', 'testpass'))
    if save:
        u.save()
        profile = u.get_profile()
        if is_vouched is not None:
            profile.is_vouched = is_vouched
        if vouched_by is not None:
            profile.vouched_by = vouched_by
        profile.full_name = kwargs.get('full_name', '')
        profile.save()
    return u
