from django.test import Client, TestCase
from django.urls import reverse
from users.forms import RegisterForm


class TestUserViews(TestCase):
    """testing users views"""
    
    fixtures = ['fixture_user.json']
    
    def setUp(self):
        self.client = Client()
        self.url = 'signup'
        self.username = 'testuser'
        self.email = 'testuser@test.com'
        self.password='thisisAveryCompletePassword@321556'
        
    def test_account_view_response(self):
        response = self.client.get(reverse('account'))
        self.assertEqual(response.status_code, 200)
        
    def test_account_renders_proper_template(self):
        response = self.client.get(reverse('account'))
        self.assertTemplateUsed(response, 'users/account.html')

    def test_signup_view_GET_response(self):
        response = self.client.get(reverse(self.url))
        self.assertEqual(response.status_code, 200)
        
   
    def test_signup_view_POST_user_exists(self):
        response = self.client.post(reverse(self.url), data={
            'username':'slb',
            'email': "papa@gmail.com",
            "password1":"",
            "password2":""
        })
        self.assertEqual(response.context["advice"], "Choisissez un autre nom d'utilisateur.")

    def test_signup_view_POST_email_exists(self):
        response = self.client.post(reverse(self.url), data={
            'username':'whatever',
            'email': "slb974run@gmail.com",
            "password1":"",
            "password2":""
        })
        self.assertEqual(response.context["advice"], "Choisissez une autre adresse e-mail.")

    def test_signup_view_POST_passwords_error(self):
        response = self.client.post(reverse(self.url), data={
            'username':'whatever',
            'email': "whatever@test.com",
            "password1":self.password,
            "password2":self.password + "@"
        })
        self.assertEqual(response.context["message"], "Les mots de passe ne correspondent pas.")
