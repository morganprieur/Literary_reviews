
from reviews.models import Ticket, Review, UserFollows 
from django.db.models import Q 



def followed_users(user): 
    f_users = UserFollows.objects.filter(user=user) 
    return f_users 


def get_users_viewable_reviews(user, f_users): 
    for f in f_users: 
        reviews = Review.objects.filter( 
            Q(user=user) | Q(user=f.followed_user) | \
            Q(ticket__user=user) | Q(ticket__user=f.followed_user)) 
        # print(reviews) 
    return reviews 

def get_users_viewable_tickets(user, f_users, reviews): 
    for f in f_users: 
        tickets = Ticket.objects.filter( 
            Q(user=user) | Q(user=f.followed_user)) 

    # print(tickets) 
    # list(tickets) 
    # print(type(tickets)) 
    # for r in reviews: 
    #     for t in tickets: 
    #         if r.ticket == t: 
    #             print(r.ticket.id) 
    #             tickets.pop(tickets.index(t)) 
    #             # List.objects.get(pk).delete()
    # print(tickets) 

    return tickets 


