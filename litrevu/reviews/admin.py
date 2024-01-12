from django.contrib import admin

from reviews.models import ( 
    Ticket, 
    Review, 
    UserFollows, 
) 
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin  
from django.contrib.auth.models import User 

class TicketAdmin(admin.ModelAdmin): 
    list_display = ( 
        'title', 
        'description', 
        'user', 
        'image', 
        'time_created',  
    ) 
admin.site.register(Ticket, TicketAdmin) 

class ReviewAdmin(admin.ModelAdmin): 
    list_display = ( 
        'ticket', 
        'user', 
        'headline', 
        'body', 
        'time_created',  
    ) 
admin.site.register(Review, ReviewAdmin) 

class UserFollowsAdmin(admin.ModelAdmin): 
    list_display = ( 
        'user', 
        'followed_user',  
    ) 
admin.site.register(UserFollows, UserFollowsAdmin) 

