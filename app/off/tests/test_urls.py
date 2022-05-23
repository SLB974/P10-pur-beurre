""" testing off urls """

from django.test import SimpleTestCase
from django.urls import resolve, reverse
from off.views import database


class TestOffUrls(SimpleTestCase):
    """testing off only url"""

    def test_database_url_resolves(self):
        url = reverse('database')
        self.assertEqual(resolve(url).func, database)
