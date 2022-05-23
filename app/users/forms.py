from allauth.account.forms import LoginForm
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class RegisterForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields =('email', 'username', 'password1', 'password2')
        
class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        username = forms.CharField(label='Email / Username')

class UserForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username','email']
