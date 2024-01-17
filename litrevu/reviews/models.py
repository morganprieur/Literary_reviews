from django.db import models

# User - django.contrib.auth.models.User 
from django.contrib.auth.models import User 
from django.conf import settings 
from django.core.validators import MaxValueValidator, MinValueValidator


# class CustomUser(AbstractUser): 
#     email = models.EmailField( 
#         # _("email address"), 
#         unique=True 
#     ) 

#     USERNAME_FIELD = "email" 
#     REQUIRED_FIELDS = [] 


class Ticket(models.Model): 
    title = models.CharField( 
        max_length=128, 
    ) 
    description = models.TextField( 
        max_length=2048, 
    ) 
    user = models.ForeignKey( 
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
    ) 
    image = models.ImageField( 
        null=True, 
        blank=True, 
    ) 
    time_created = models.DateTimeField( 
        auto_now_add=True, 
    ) 


class Review(models.Model): 
    # file deepcode ignore django~null~true~nontext~field: <please specify a reason of ignoring this>
    ticket = models.ForeignKey( 
        Ticket, 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True, 
    ) 
    rating = models.PositiveSmallIntegerField( 
        # max_length=1024, 
        validators=[ 
            MinValueValidator(0), 
            MaxValueValidator(5) 
        ] 
    ) 
    user = models.ForeignKey( 
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
    ) 
    headline = models.CharField( 
        max_length=128, 
    ) 
    body = models.TextField( 
        max_length=8192, 
        blank=True, 
    ) 
    time_created = models.DateTimeField( 
        auto_now_add=True, 
    ) 


class UserFollows(models.Model): 
    user = models.ForeignKey( 
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='following', 
    ) 
    followed_user = models.ForeignKey( 
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='followed_by', 
    ) 

    class Meta: 
        unique_together = ('user', 'followed_user', ) 
        verbose_name_plural = 'User Follows'

