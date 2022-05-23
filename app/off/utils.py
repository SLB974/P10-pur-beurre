#coding: utf-8

CUSTOM_FIELDS = ['_id', 'product_name_fr','brands', 'nutrition_grade_fr', 'image_front_url']
CUSTOM_NUTRIMENTS =['energy-kcal', 'carbohydrates', 'fat', 'proteins', 'sodium', 'fiber']
CATEGORIES = ["Poissons", "Conserves","Pizzas", "Fromages", "Produits à tartiner"]

criterias = {
    'search_simple': 1,
    'action': 'process',
    'tagtype_0': 'countries',
    'tag_contains_0': 'contains',
    'tag_0': 'france',
    'tagtype_1': 'categories',
    'tag_contains_1': 'contains',
    'tag_1': None,
    'tagtype_2': 'brands',
    'tag_contains_2': 'does_not_contain',
    'tag_2': (None,''),
    'tagtype_3': 'nutrition_grade_fr',
    'tag_contains_3': 'does not contain',
    'tag_3': (None, ''),
    'tagtype_4': 'product_name_fr',
    'tag_contains_4': 'does_not_contain',
    'tag_4': (None,''),
    'tagtype_5': 'categories_lc',
    'tag_contains_5': 'contains',
    'tag_5': 'fr',
    'tagtype_6': 'labels_lc',
    'tag_contains_6': 'contains',
    'tag_6': 'fr',
    'page_size': 1000,
    'json': 1
}
