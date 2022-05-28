""" testing the openfoodfact fetcher class"""

import json
from unittest.mock import patch

from django.test import TestCase
from off.fetcher import ApiConsulter
from off.fixtures.fields_bunch import (correct_fields_noodle,
                                       correct_nutriments_noodle,
                                       empty_fields_noodle,
                                       empty_nutriments_noodle,
                                       wrong_fields_noodle,
                                       wrong_nutriments_noodle)
from off.models import Category, Favorite, Product


class ApiConsulterTestCase(TestCase):
    """Test class for ApiConsulter"""
    
    fixtures = ['fixture_category.json',
            'fixture_product.json',
            ]
    
    consulter = ApiConsulter()
    
    @staticmethod
    def fromages_api_response():
        with open('off/fixtures/fromages_api_response.json', 'r', encoding='utf-8') as file:
            return json.load(file)
        
    @staticmethod
    def fromages_record():
        with open('off/fixtures/fromages_product.json', 'r', encoding='utf-8') as file:
            return json.load(file)
        
    def test_category_should_have_one_record(self):
        self.assertEqual(Category.objects.count(),1)
        
    def test_product_should_have_ten_records(self):
        self.assertEqual(Product.objects.count(),10)
    
    def test_db_clean_empties_database(self):
        self.consulter.db_clean()
        self.assertEqual(Category.objects.count(),0)
        self.assertEqual(Product.objects.count(),0)
        self.assertEqual(Favorite.objects.count(),0)
  
    def test_check_fields_returns_false_with_wrong_data(self):
        self.assertFalse(self.consulter.check_fields(wrong_fields_noodle))
    
    def test_check_fields_returns_false_with_empty_data(self):
        self.assertFalse(self.consulter.check_fields(empty_fields_noodle))
    
    def test_check_fields_returns_true_with_correct_data(self):
        self.assertTrue(self.consulter.check_fields(correct_fields_noodle))
    
    def test_check_nutriments_returns_false_with_wrong_data(self):
        self.assertFalse(self.consulter.check_nutriments(wrong_nutriments_noodle))
        
    def test_check_nutriments_returns_false_with_empty_data(self):
        self.assertFalse(self.consulter.check_nutriments(empty_nutriments_noodle))
    
    def test_check_nutriments_returns_true_with_correct_data(self):
        self.assertTrue(self.consulter.check_nutriments(correct_nutriments_noodle))

    def test_save_category_should_add_fromage_category(self):
        category = self.consulter.save_category('Fromages')
        if category is not None:
            self.assertEqual(category.category,'Fromages')
        
    def test_create_record_should_return_Product_object(self):
        record = self.fromages_record()
        last = Category.objects.last()
        record = self.consulter.create_record(record, last)
        self.assertEqual(type(record), Product)        
    
    @patch('off.fetcher.ApiConsulter.check_fields')
    def test_validate_product_should_call_check_fields(self, mock_check_fields):
        mock_check_fields.return_value=True
        self.consulter.validate_product(self.fromages_record())
        mock_check_fields.assert_called_once()
        
    @patch('off.fetcher.ApiConsulter.check_nutriments')
    def test_validate_product_should_call_check_nutriments(self, mock_check_nutriments):
        mock_check_nutriments.return_value=True
        self.consulter.validate_product(self.fromages_record())
        mock_check_nutriments.assert_called_once()

    @patch('off.fetcher.requests.get')
    def test_get_results_should_call_requests_get_method(self, mock_requests_get):
        mock_requests_get.return_value.status_code = 200
        self.consulter.get_results('Fromages')
        mock_requests_get.assert_called_once()

    @patch('off.fetcher.CATEGORIES',['Fromages'])
    @patch('off.fetcher.ApiConsulter.db_clean')
    @patch('off.fetcher.ApiConsulter.get_results')
    def test_db_save_should_call_db_clean(self, mock_get_results, mock_db_clean):
        mock_get_results.return_value = self.fromages_api_response()
        consulter = ApiConsulter()
        consulter.db_save()
        mock_db_clean.assert_called_once()

    @patch('off.fetcher.CATEGORIES',['Fromages'])
    @patch('off.fetcher.ApiConsulter.save_category')
    @patch('off.fetcher.ApiConsulter.get_results')
    def test_db_save_should_call_save_category_with_Fromages(self, mock_get_results, mock_save_category):
        mock_get_results.return_value = self.fromages_api_response()
        consulter = ApiConsulter()
        try:
            consulter.db_save()
        except ValueError:
            pass
        mock_save_category.assert_called_with('Fromages')

    @patch('off.fetcher.CATEGORIES', ['Fromages'])
    @patch('off.fetcher.ApiConsulter.get_results')
    def test_db_save_should_call_get_results(self, mock_get_results):
        mock_get_results.return_value = self.fromages_api_response()
        consulter = ApiConsulter()
        consulter.db_save()
        mock_get_results.assert_called()

    @patch('off.fetcher.CATEGORIES', 'Fromages')
    @patch('off.fetcher.ApiConsulter.bulk_fabrik')
    @patch('off.fetcher.ApiConsulter.get_results')
    def test_db_save_should_call_bulk_fabrik(self, mock_get_results, mock_bulk_fabrik):
        mock_get_results.return_value = self.fromages_api_response()
        consulter = ApiConsulter()
        consulter.db_save()
        mock_bulk_fabrik.assert_called()

    @patch('off.fetcher.ApiConsulter.validate_product')
    def test_bulk_fabrik_should_call_validate_product(self, mock_validate_product):
        container = self.fromages_api_response()['products']
        last = Category.objects.get(pk=1)
        self.consulter.bulk_fabrik(container, last)
        mock_validate_product.assert_called()
    
    @patch('off.fetcher.ApiConsulter.create_record')
    def test_bulk_fabrik_should_call_create_record(self, mock_create_record):
        container = self.fromages_api_response()['products']
        last = Category.objects.get(pk=1)
        self.consulter.bulk_fabrik(container, last)
        mock_create_record.assert_called()        
    
    @patch('off.fetcher.CATEGORIES', ['Fromages'])
    @patch('off.fetcher.ApiConsulter.get_results')
    def test_db_save_should_create_5_records_in_Product_model(self,mock_get_results):
        mock_get_results.return_value = self.fromages_api_response()
        consulter = ApiConsulter()
        consulter.db_save()
        self.assertEqual(Product.objects.count(), 5)
        
    @patch('off.fetcher.CATEGORIES', ['Fromages'])
    @patch('off.fetcher.ApiConsulter.get_results')
    @patch('off.fetcher.Product.objects.bulk_create')
    def test_db_save_should_pass_if_value_error(self, mock_bulk_create, mock_get_results):
        mock_bulk_create.side_effect = ValueError
        mock_get_results.return_value= self.fromages_api_response()
        consulter = ApiConsulter()
        consulter.db_save()
        self.assertRaises(ValueError)
