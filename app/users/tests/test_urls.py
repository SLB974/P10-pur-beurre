""" testing user urls """

from django.contrib.auth.views import LoginView, LogoutView
from django.test import SimpleTestCase
from django.urls import resolve, reverse
from users import views


class TestUserUrls(SimpleTestCase):
    """testing users urls"""

    def test_account_url_resolves(self):
        url = reverse('account')
        self.assertEqual(resolve(url).func, views.account)

    def test_sign_up_url(self):
        url = reverse('signup')
        self.assertEqual(resolve(url).func, views.signup)
        
       
    def test_logout_url(self):
        url = reverse('logout')
        self.assertEqual(resolve(url).func.view_class, LogoutView)
