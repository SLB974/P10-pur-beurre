""" testing nutella urls """

from django.test import SimpleTestCase
from django.urls import resolve, reverse
from nutella import views


class TestNutellaUrls(SimpleTestCase):
    "testing nutella urls return proper template"
    
    def test_index_url_resolves(self):
        url = reverse('index')
        self.assertEqual(resolve(url).func, views.index)

    def test_product_url_resolves(self):
        url = reverse('product', args=[0])
        self.assertEqual(resolve(url).func, views.product)

    def test_product_search_url_resolves(self):
        url = reverse('product_search')
        self.assertEqual(resolve(url).func, views.search_product)

    def test_product_remplacement_url_resolves(self):
        url = reverse('product_replacement', args=[0])
        self.assertEqual(resolve(url).func, views.search_replacement)

    def test_save_favorite_url_resolves(self):
        url = reverse('save_favorite', kwargs={'pk_replaced':0, 'pk_replacing':0})
        self.assertEqual(resolve(url).func, views.save_favorite)

    def test_delete_favorite_url_resolves(self):
        url = reverse('delete_favorite', args=[0])
        self.assertEqual(resolve(url).func, views.delete_favorite)

    def test_product_user_url_resolves(self):
        url = reverse('product_user', args=[0])
        self.assertEqual(resolve(url).func, views.product_user)

    def test_legal_notice_url_is_resolved(self):
        url = reverse('legal_notice')
        self.assertEqual(resolve(url).func, views.legal_notice)
