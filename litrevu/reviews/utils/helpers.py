
from reviews.models import Ticket, Review, UserFollows 
from django.db.models import Q 


def followed_users(user): 
    f_users = UserFollows.objects.filter(user=user) 
    return f_users 


def get_users_viewable_reviews(user): 
    reviews = Review.objects.select_related("ticket").filter(
        Q(user__in=UserFollows.objects.filter(user=user)\
            .values("followed_user")) | Q(user=user)
    ) 
    return reviews 

def get_users_viewable_tickets(user, reviews): 
    tickets = Ticket.objects.filter(
        Q(user__in=UserFollows.objects.filter(user=user)\
        .values("followed_user")) | Q(user=user)
    ).exclude(id__in=reviews.values("ticket_id")) 
    return tickets 
