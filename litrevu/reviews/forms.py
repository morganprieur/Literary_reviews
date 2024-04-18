
# reviews/forms.py 
from django import forms 
from django.contrib.auth import get_user_model 
from django.contrib.auth.forms import UserCreationForm 
from django.forms import ModelForm 

from . import models


class SignupForm(UserCreationForm): 
    """ Class that displays only the useful fields to register a user. 
    """ 
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ( 
            'username', 
            'email', 
            'first_name', 
            'last_name' 
        ) 


class UserForm(forms.Form): 
    """ General class to search a user on his/her username. 
    """ 
    username = forms.CharField(label="pseudo ", max_length=150) 


class TicketForm(ModelForm): 
    """ Class that displays the fields to register one ticket. 
    """ 
    class Meta: 
        model = models.Ticket 
        fields = [ 
            'title', 
            'description', 
            'image' 
        ] 


class NewReviewForm(ModelForm): 
    """ Class that displays the fields to register a new review and ticket at the same time. 
        The body of the review is displayed at a textarea. 
    """ 
    class Meta: 
        model = models.Review 
        fields = [ 
            'ticket', 
            'rating', 
            'headline', 
            'body' 
        ] 
        labels = { 
            'rating': 'Rating (de 0 à 5)', 
        } 
        widgets = { 
            'body': forms.Textarea(attrs={'rows': 4, 'cols': 15}), 
        } 


class ReviewForm(ModelForm): 
    """ Class that displays the fields to register a new review, answering to a ticket. 
    The body of the review is displayed at a textarea, and the ticket input is hidden. 
    """ 
    class Meta: 
        model = models.Review 
        fields = [ 
            'ticket', 
            'rating', 
            'headline', 
            'body' 
        ] 
        labels = { 
            'rating': 'Rating (de 0 à 5)', 
        } 
        widgets = { 
            'body': forms.Textarea(attrs={'rows': 4, 'cols': 15}), 
            'ticket': forms.HiddenInput(), 
        } 

