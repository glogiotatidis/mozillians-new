from django.contrib.auth.models import User

from nose.tools import ok_

from mozillians.common.tests import TestCase
from mozillians.users.tests import UserFactory
from mozillians.users.tasks import remove_incomplete_accounts


class IncompleteAccountsTests(TestCase):
    """Incomplete accounts removal tests."""

    def test_remove_incomplete_accounts(self):
        """Test remove incomplete accounts."""
        user = UserFactory.create(userprofile={'full_name': ''})
        remove_incomplete_accounts(days=0)
        ok_(not User.objects.filter(id=user.id).exists())


class ElasticSearchIndexTests(TestCase):
    def test_index_objects(self):
        pass

    def test_index_objects_public(self):
        pass

    def test_unindex_objects(self):
        pass

    def test_unindex_objects_public(self):
        pass


class BasketTests(TestCase):
    pass
