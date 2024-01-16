
# reviews/forms.py
from django import forms 
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm 
from django.forms import ModelForm 

# blog/forms.py
from . import models


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name')  # , 'role' 


class UserForm(forms.Form): 
        username = forms.CharField(label="pseudo", max_length=150) 

# class UserForm(ModelForm): 
#     class Meta: 
#         model = get_user_model() 
#         fields = ['username'] 

# class NameForm(forms.Form):
#     your_name = forms.CharField(label="Your name", max_length=100)


# class AuthorForm(forms.Form):
#     name = forms.CharField(max_length=100)
#     title = forms.CharField(
#         max_length=3,
#         widget=forms.Select(choices=TITLE_CHOICES),
#     )
#     birth_date = forms.DateField(required=False)

# class AuthorForm(ModelForm):
#     class Meta:
#         model = Author
#         fields = ["name", "title", "birth_date"]


# ex form sans utiliser la classe LoginView : 
# class LoginForm(forms.Form):
#     username = forms.CharField( 
#         max_length=63, 
#         label='Nom d’utilisateur' 
#     ) 
#     password = forms.CharField( 
#         max_length=63, 
#         widget=forms.PasswordInput, 
#         label='Mot de passe' 
#     ) 

