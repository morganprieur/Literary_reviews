from django.db import models

from django.contrib.auth.models import User 
from django.conf import settings 
from django.core.validators import MaxValueValidator, MinValueValidator


class BlockedUsers(models.Model): 
    """ Intermediary table for storage of the user / blocked_user binomials. 
        Args:
            models (Models instance): Parent-class extended. 
    """ 
    user = models.ForeignKey( 
        User, 
        on_delete=models.CASCADE, 
        related_name='blocker' 
    ) 
    blocked_user = models.ForeignKey( 
        User, 
        on_delete=models.CASCADE, 
        related_name='blocked_user' 
    ) 

    class Meta: 
        unique_together = ('user', 'blocked_user', ) 
        verbose_name_plural = 'Blocked users' 


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
    ) 
    rating = models.PositiveSmallIntegerField( 
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

