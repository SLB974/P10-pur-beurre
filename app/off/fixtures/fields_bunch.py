correct_fields_noodle ={"_id":"1", 
                        "brands":"Suzi Wan", 
                        "product_name_fr":"Nouilles au poulet", 
                        "nutrition_grade_fr":"c", 
                        "image_front_url":"www.something.com"}

wrong_fields_noodle = {"_id":"1", 
                      "brands":"Suzi Wan", 
                      "product_name_fr":"Nouilles au poulet", 
                      "image_front_url":"www.something.com"}

empty_fields_noodle ={"_id":"1", 
                        "brands":"     ", 
                        "product_name_fr":"Nouilles au poulet", 
                        "nutrition_grade_fr":"c", 
                        "image_front_url":"www.something.com"}

correct_nutriments_noodle= {"_id":"1", 
                        "brands":"Suzi Wan", 
                        "product_name_fr":"Nouilles au poulet", 
                        "nutrition_grade_fr":"c", 
                        "image_front_url":"www.something.com",
                        "nutriments": {
                            'energy-kcal': "150",
                            'carbohydrates': "10",
                            'fat':"10",
                            'proteins':"10",
                            'sodium':"2",
                            'fiber':"3"}}
    
wrong_nutriments_noodle = {"_id":"1", 
                        "brands":"Suzi Wan", 
                        "product_name_fr":"Nouilles au poulet", 
                        "nutrition_grade_fr":"c", 
                        "image_front_url":"www.something.com",
                        "nutriments": {
                            'energy-kcal': "150",
                            'carbohydrates': "10",
                            'fiber':"3",
                            'fat':'50'}}

empty_nutriments_noodle= {"_id":"1", 
                        "brands":"Suzi Wan", 
                        "product_name_fr":"Nouilles au poulet", 
                        "nutrition_grade_fr":"c", 
                        "image_front_url":"www.something.com",
                        "nutriments": {
                            'energy-kcal': "25",
                            'carbohydrates': "15",
                            'fat':"",
                            'proteins':"10",
                            'sodium':"2",
                            'fiber':"3"}}

