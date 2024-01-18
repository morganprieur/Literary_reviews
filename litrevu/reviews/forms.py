
# reviews/forms.py
from django import forms 
from django.contrib.auth import get_user_model 
# from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm 
from django.forms import ModelForm 

# blog/forms.py
from . import models


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name')  # , 'role' 


class UserForm(forms.Form): 
    username = forms.CharField(label="pseudo ", max_length=150) 

# class UserForm(ModelForm): 
#     class Meta: 
#         model = get_user_model() 
#         fields = ['username'] 


# class TicketForm(forms.Form): 
#     title = forms.CharField(label="Titre ") 
#     description = forms.CharField(label="Description ") 
#     # user = forms.CharField(label="Utilisateur ") 
#     image = forms.FileField(label="Télécharger un fichier ") 


class TicketForm(ModelForm): 
    class Meta: 
        model = models.Ticket 
        fields = ('title', 
            'description', 
            # 'user', 
            'image' 
        ) 

# class AuthorForm(forms.Form):
#     name = forms.CharField(max_length=100)
#     title = forms.CharField(
#         max_length=3,
#         widget=forms.Select(choices=TITLE_CHOICES),
#     )
#     birth_date = forms.DateField(required=False)

# class ReviewForm(forms.Form): 
#             ticket = forms.ForeignKey() 
#             rating = forms.PositiveSmallIntegerField(MinValueValidator(0), MaxValueValidator(5)) 
#             # 'user', 
#             headline =  forms.CharField(max_length=128)
#             body = forms.TextField() 
#         ) 

class ReviewForm(ModelForm): 
    class Meta: 
        model = models.Review 
        fields = [ 
            'ticket', 
            'rating', 
            # 'user',  # auto: request.user 
            'headline', 
            'body' 
        ] 
        widgets = { 
            'body': forms.Textarea(attrs={'rows': 4, 'cols': 15}), 
        } 


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

