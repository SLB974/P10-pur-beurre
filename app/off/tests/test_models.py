""" testing off models """

from django.contrib.auth import get_user_model
from django.test import TestCase
from off.models import Category, Favorite, Product


class CategoryModelTest(TestCase):
    """testing off model Category"""

    fixtures = ['fixture_category.json',
        'fixture_product.json',
        ]
        

    def test_object_name_should_be_category_field(self):
        category = Category.objects.last()
        expected = category.category
        self.assertEqual(str(category), expected)
        
class ProductModelTest(TestCase):
    """testing off model Product"""

    fixtures = ['fixture_category.json',
            'fixture_product.json',
            ]
        
    def test_object_name_should_be_product_field(self):
        
        product = Product.objects.last()
        expected = product.product
        self.assertEqual(str(product), expected)

class FavoriteModelTest(TestCase):
    """testing off model Favorite"""
    
    fixtures = ['fixture_category.json',
            'fixture_product.json',
            'fixture_user.json'
            ]
    
    def test_object_name_should_be_correct(self):
        user = get_user_model().objects.get(pk=1)
        product = Product.objects.get(pk=1)
        replace = Product.objects.get(pk=2)
        
        favorite = Favorite.objects.create(
            user_id = user,
            product_id = product,
            replacement_id = replace
        )
        
        favorite = Favorite.objects.last()
        
        expected = (str(user) + "/" 
                    + str(product) + " vs "
                    + str(replace))
        
        self.assertEqual(str(favorite), expected)
        