# coding: utf-8
""" Module for :
                    Fetching openfoodfacts data
                    cleaning data
                    save data in database
                    """

# import json

import requests

from .models import Category, Favorite, Product
from .utils import CATEGORIES, CUSTOM_FIELDS, CUSTOM_NUTRIMENTS, criterias


class ApiConsulter:
    """Manage API's requests, data cleaning and saving."""

    def __init__(self):
        self.doubled_name=set()
        self.doubled_ean=set()

    @classmethod
    def get_results(cls, category):
        """API's GET consultation.

        parameter : category = searched category

        return : string
        """
        
        url = "https://fr.openfoodfacts.org/cgi/search.pl?"

        criterias['tag_1'] = category

        response = requests.get(url, params=criterias)
        response = response.json()
        
        # filename="cat_" + category + ".json"
        # with open(filename, "w") as f:
        #     json.dump(response, f, indent=4)

        return response
    
    @classmethod
    def db_clean(cls):
        """ clean existing records in database """
        Category.objects.all().delete()
        Product.objects.all().delete()
        Favorite.objects.all().delete()

    @staticmethod    
    def check_fields(record):
        """
        Check that all the fields in custom_fields are in the record
        
        :param record: the record to check
        :return: a boolean value.
        """
        
        
        for field in CUSTOM_FIELDS:
            if field not in record:
                return False
                        
            if record[field].strip()=="" or record[field].strip()=="0":
                return False
        
        return True
    
    @staticmethod
    def check_nutriments(record):
        """
        The function checks if the product has all the required nutriments
        
        :param record: the product record to check
        :return: A boolean value.
        """
        
        for nutriment in CUSTOM_NUTRIMENTS:
            if nutriment not in record['nutriments']:
                return False
            
            if record['nutriments'][nutriment] == '':
                return False
            
        return True
    
    @staticmethod
    def save_category(category):
        """ Creating a new record in Category table.
        :param category: the category to add
        :return: integer value.
        """
    
        data = Category.objects.create(category=category)
        data.save()
        return Category.objects.last()

    
    def validate_product(self, record):
        """ 
        Checking if the product has all the required nutriments and fields.
        Checking if product_name_fr and/or _id fields are not added yet.
        :param: record to check
        :return: a Boolean value. 
        """
       
        if (self.check_fields(record) is True
            and self.check_nutriments(record) is True
            and record['product_name_fr'].lower().strip() not in self.doubled_name
            and record['_id'] not in self.doubled_ean
            and record['product_name_fr'].strip() != ""):
            return True
        return False
    
    @staticmethod
    def create_record(record, last):
        """
        Creating the product object.
        :param:
            record: record to create,
            last: Category foreign key.
        :return: Product object.
        """
        return Product(product=record['product_name_fr'],
                                brand=record['brands'],
                                category_id = last,
                                score=record['nutrition_grade_fr'],
                                pic_url=record['image_front_url'],
                                url=record['url'],
                                energy=record['nutriments']['energy-kcal'],
                                carbo=record['nutriments']['carbohydrates'],
                                fat=record['nutriments']['fat'],
                                proteins=record['nutriments']['proteins'],
                                sodium=record['nutriments']['sodium'],
                                fiber=record['nutriments']['fiber'])
        
    
    def bulk_fabrik(self, container, last):
        records = []
        for record in container:
            if self.validate_product(record):
                data = self.create_record(record, last)
                
                records.append(data)
                self.doubled_name.add(record['product_name_fr'].lower().strip())
                self.doubled_ean.add(record['_id'])
        return records        
    
    def db_save(self):
        """ Empties db and insert records. """
       
        self.db_clean()
        
        for category in CATEGORIES:
            last = self.save_category(category)
            
            response = self.get_results(category)
            
            bulk = self.bulk_fabrik(response['products'], last)
            
            try:
                Product.objects.bulk_create(bulk)
                
            except ValueError:
                pass
