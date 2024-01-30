from django.contrib import admin 
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin 

from reviews.models import ( 
    Ticket, 
    Review, 
    BlockedUsers, 
    UserFollows, 
) 
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin  
from django.contrib.auth.models import User 

class UserAdmin(BaseUserAdmin): 
    list_display = ( 
        'id', 'username', 'email', 'first_name', 'last_name', 'is_staff' 
    ) 
admin.site.unregister(User) 
admin.site.register(User, UserAdmin) 

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


class BlockedUsersAdmin(admin.ModelAdmin): 
    list_display = ( 
        'user', 
        'blocked_user',  
    ) 
admin.site.register(BlockedUsers, BlockedUsersAdmin) 

