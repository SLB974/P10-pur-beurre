from unittest.mock import patch

from django.test import Client, TestCase
from django.urls import reverse


class TestOffView(TestCase):
    
    def setUp(self):
        self.client = Client()
            
    def new_db_save(self):
        return


    def test_database_view_response(self):

        with patch('off.views.ApiConsulter.db_save', new_callable= self.new_db_save()):
            response = self.client.get(reverse('database'))
            self.assertEqual(response.status_code, 200)
        

    def test_database_view_returns_proper_template(self):
        with patch('off.views.ApiConsulter.db_save', new_callable= self.new_db_save()):
            response = self.client.get(reverse('database'))
            self.assertTemplateUsed(response, 'off/database.html')
