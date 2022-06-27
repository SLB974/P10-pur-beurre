"""Nutella views tests"""

from django.contrib.auth import get_user_model
from django.test import Client, TestCase, TransactionTestCase
from django.urls import reverse
from nutella.views import nutriscore
from off.models import Favorite, Product


class TestNutellaStandardViews(TestCase):
    """nutella views tests with no login required"""
    
    fixtures = [
        'fixture_category.json',
        'fixture_product.json',
        'fixture_favorite.json',
        'fixture_user.json'
    ]
    
    def setUp(self):
        self.client = Client()
    
    def test_index_view_redirects_to_nutella(self):
        response = self.client.get('/')
        self.assertRedirects(response, '/nutella/', status_code=301, target_status_code=200)

    def test_index_view_renders_proper_template(self):
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'nutella/index.html')

    def test_product_view_response(self):
        response = self.client.get(reverse('product', args=[1]))
        self.assertEqual(response.status_code,200)
        
    def test_product_view_renders_proper_template(self):
        response = self.client.get(reverse('product', args=[1]))
        self.assertTemplateUsed(response, 'nutella/product.html')

    def test_product_search_response(self):
        response=self.client.get(reverse("product_search"), {"home_search":"pizza"})
        self.assertEqual(response.status_code,200)

    def test_product_search_renders_proper_template(self):
        response = self.client.get(reverse('product_search'), {
            "home_search": "pizza", "page":1})
        self.assertTemplateUsed(response, 'nutella/product_search.html')
        
    def test_product_search_page_over_should_return_last_page(self):
        response= self.client.get(reverse('product_search'),
                                  {"home_search":"pizza", "page":999})
        paginator = response.context['product_list'].paginator
        actual = response.context['product_list'].number
        expected = paginator.get_page(paginator.num_pages).number
        self.assertEquals(expected, actual)
        

    def test_search_replacement_view_response(self):
        response = self.client.get(reverse('product_replacement', args=[1]))
        self.assertEqual(response.status_code, 200)

    def test_search_replacement_view_renders_proper_template(self):
        response = self.client.get(reverse('product_replacement', args=[1]))
        self.assertTemplateUsed(response, 'nutella/product_replacement.html')
        
    def test_product_replacement_page_over_should_return_last_page(self):
        response= self.client.get(reverse('product_replacement', args=[1]),
                                  {"page":999})
        paginator = response.context['product_list'].paginator
        actual = response.context['product_list'].number
        expected = paginator.get_page(paginator.num_pages).number
        self.assertEquals(expected, actual)

    def test_legal_notice_view_response(self):
        response = self.client.get(reverse('legal_notice'))
        self.assertEqual(response.status_code,200)
        
    def test_legal_notice_view_renders_proper_template(self):
        response = self.client.get(reverse('legal_notice'))
        self.assertTemplateUsed(response, 'nutella/legal_notice.html')
        
    def test_nutriscore_should_return_proper_value(self):
        self.assertTrue('Nutri-score-A' in nutriscore('a'))
        self.assertTrue('Nutri-score-B' in nutriscore('b'))
        self.assertTrue('Nutri-score-C' in nutriscore('c'))
        self.assertTrue('Nutri-score-D' in nutriscore('d'))
        self.assertTrue('Nutri-score-E' in nutriscore('e'))
        
class TestSaveFavoriteView(TestCase):
    """nutella Save Favorite View with login required tests"""

    fixtures = [
        'fixture_category.json',
        'fixture_product.json',
        'fixture_user.json'
    ]
    
    @staticmethod
    def user_creation():
        username="papa"
        password="nimportequoi70"
        User = get_user_model()
        user = User.objects.create_user(username, password=password)
      
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.kwargs = {'pk_replaced':1, 'pk_replacing':2}
        cls.url = 'save_favorite'
    
    
    
    def setUp(self):
        self.user_creation()
        self.client.login(username='papa', password='nimportequoi70')
        
    
    def test_response_with_no_user_logged(self):
        self.client.logout()
        response = self.client.get(reverse(self.url, kwargs=self.kwargs))
        self.assertTrue(response.status_code, 200)
    
    def test_redirects_properly_with_no_user_logged(self):
        self.client.logout()
        response = self.client.post(reverse(self.url, kwargs=self.kwargs))
        expected = "/accounts/login/?next=/nutella/save_favorite/1/2/"
        self.assertEqual(response.url, expected)

    def test_response_with_user_logged(self):
        url = reverse(self.url, kwargs=self.kwargs)
        response = self.client.get(url, HTTP_REFERER = 'index')
        expected ="/nutella/"
        self.assertRedirects(response, expected, status_code=302, target_status_code=200)
        
    def test_add_favorite_with_user_logged(self):
        url = reverse(self.url, kwargs=self.kwargs)
        self.client.get(url, HTTP_REFERER = 'index')
        self.assertEqual(Favorite.objects.count(),1)

class TestDeleteFavoriteView(TestCase):
    """nutella delete favorite view with login required"""
    
    fixtures = [
        'fixture_category.json',
        'fixture_product.json',
        'fixture_favorite.json',
        'fixture_user.json'
    ]
    
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.user_model=get_user_model()
        cls.user = cls.user_model.objects.create_user(username='john', password='lennon', email="whatever@lennon.com")
        cls.url = 'delete_favorite'
    
    def setUp(self):
        logged_in = self.client.login(username = 'john', password='lennon')
        
    def test_response_with_no_user_logged(self):
        self.client.logout()
        response = self.client.post(reverse(self.url, args=[1]))
        self.assertTrue(response.status_code, 200)
                   
    def test_redirects_properly_with_no_user_logged(self):
        self.client.logout()
        response = self.client.post(reverse(self.url, args=[1]))
        expected = "/accounts/login/?next=/nutella/delete_favorite/1/"
        self.assertEqual(response.url, expected)
    
    def test_response_with_user_logged(self):
        url = reverse(self.url, args=[1])
        response = self.client.get(url, HTTP_REFERER = 'index')
        expected ="/nutella/"
        self.assertRedirects(response, expected, status_code=302, target_status_code=200)
    
    def test_delete_favorite_with_user_logged(self):
        url = reverse(self.url, args=[1])
        self.client.get(url, HTTP_REFERER='index')
        self.assertEqual(Favorite.objects.count(), 0)

class TestProductUserView(TestCase):
    """nutella user product view with login required"""
    
    fixtures = [
    'fixture_category.json',
    'fixture_product.json',
    ]
    
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.user_model = get_user_model()
        cls.user = cls.user_model.objects.create_user(username='john', password='lennon', email="jonh@lennon.com")
        cls.url = 'product_user'
    
    def setUp(self):
        logged_in=self.client.login(username = 'john', password='lennon')

    def test_response_with_no_user_logged(self):
        self.client.logout()
        response = self.client.post(reverse(self.url, args=[1]))
        self.assertTrue(response.status_code, 200)
                   
    def test_redirects_properly_with_no_user_logged(self):
        self.client.logout()
        response = self.client.post(reverse(self.url, args=[1]))
        expected = "/accounts/login/?next=/nutella/product_user/1/"
        self.assertEqual(response.url, expected)
    
    def test_response_with_user_logged(self):
        url = reverse(self.url, args=[1])
        response = self.client.get(url)
        self.assertTrue(response.status_code, 200)
    
    def test_view_renders_proper_template(self):
        url = reverse(self.url, args=[1])
        response=self.client.get(url)
        self.assertTemplateUsed(response, 'nutella/product_user.html')
        