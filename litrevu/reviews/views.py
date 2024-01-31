
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.models import User 
from django.contrib.auth.decorators import login_required 
from django.core.paginator import Paginator 
from django.db.models import CharField, Value 
from itertools import chain 
from django.shortcuts import redirect, render 
from django.views.generic import View 
# litrevu/reviews 
from django.conf import settings 
from reviews.models import Review, Ticket, BlockedUsers, UserFollows 
from reviews.utils import helpers 
# litrevu/reviews utils 
from . import forms 
from django.db.models import Q 

# ============ login ============================== # 

class SignupPageView(View): 
    template_name = 'rev/signup.html' 
    form_class = forms.SignupForm 

    def get(self, request): 
        form = self.form_class() 
        return render( 
            request, 
            self.template_name, 
            context={'form': form}) 

    def post(self, request): 
        form = self.form_class(request.POST) 
        if form.is_valid(): 
            user = form.save()
            # auto-login user: 
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL) 
        else: 
            message = 'Veuillez suivre les instructions' 
            return render(request, self.template_name, context={ 
                'form': form, 
            }) 


def logout_user(request):
    logout(request)
    return redirect('home') 


@login_required 
def home(request): 
    header = 'Accueil' 

    user = request.user 
    f_users = helpers.followed_users(user) 

    reviews = helpers.get_users_viewable_reviews(user) 
    reviews = reviews.annotate( 
        content_type=Value("REVIEW", CharField())) 

    tickets = helpers.get_users_viewable_tickets(user, reviews) 
    tickets = tickets.annotate(content_type=Value("TICKET", CharField())) 

    # combine and sort the two types of posts 
    posts = sorted( 
        chain(reviews, tickets), 
        key=lambda post: post.time_created, 
        reverse=True 
    ) 

    paginator = Paginator(posts, 4) 
    page = request.GET.get("page") 
    page_obj = paginator.get_page(page) 

    return render( 
        request, 'rev/home.html', context={ 
            'header': header, 
            'user': user, 
            'followed': f_users, 
            'posts': posts, 
            "page_obj": page_obj, 
        } 
    ) 


@login_required 
def edit_ticket(request, ticket_id): 
    ticket = Ticket.objects.get(pk=ticket_id) 
    form = forms.TicketForm(instance=ticket) 
    if request.method == 'POST': 
        form = forms.TicketForm( 
            request.POST, request.FILES, instance=ticket) 
        if form.is_valid(): 
            edited_ticket = form.save() 
            return redirect('activity') 
    else: 
        header = 'Modifier un ticket' 
        return render(request, 'rev/edit_ticket.html', context={ 
            'header': header, 
            'form': form, 
        }) 


@login_required 
def edit_review(request, review_id): 
    review = Review.objects.get(pk=review_id) 
    ticket_id = review.ticket.id 
    ticket = Ticket.objects.get(pk=ticket_id) 
    form = forms.ReviewForm(instance=review) 

    if request.method == 'POST': 
        form = forms.ReviewForm(request.POST, instance=review) 
        if form.is_valid(): 
            edited_review = form.save() 
            return redirect('activity') 
    else: 
        header = 'Modifier une revue' 
        return render(request, 'rev/edit_review.html', context={ 
            'header': header, 
            'review': review, 
            'ticket': ticket, 
            'form': form, 
        }) 


@login_required 
def abonnements(request): 
    header = 'Abonnements' 
    user = request.user 
    users = [] 
    form = forms.UserForm(request.GET) 

    followed = UserFollows.objects.filter( 
        user__username=request.user.username) 
    followers = UserFollows.objects.filter( 
        followed_user__username=request.user.username) 
    for fr in followers: 
        print(fr.followed_user.id, fr.followed_user.username) 
        print(fr.user.id, fr.user.username) 

    if form.is_valid(): 
        username = form.cleaned_data['username'] 
        users = User.objects.filter(username__icontains=username) 

    return render(request, 'rev/abonnements.html', context={ 
            'header': header, 
            'followed': followed, 
            'followers': followers, 
            'user': user, 
            'users': users, 
            'form': form, 
        } 
    ) 


@login_required 
def create_abo(request, user_id): 

    user = User.objects.get(id=user_id) 
    blocked_users = BlockedUsers.objects.all() 

    print('blocked_users[0].id', blocked_users[0].blocked_user.id) 

    if request.method == 'POST': 
        # file deepcode ignore IdentityCheckOnNewObj: local project , file deepcode ignore new~object~identity: <please specify a reason of ignoring this>
        if blocked_users and (blocked_users[0].blocked_user==user): 
            print('yes') 
            print(blocked_users) 
            return redirect('impossible-abo', user_id) 
        else: 
            print('no') 
            abo = UserFollows.objects.create( 
                followed_user=user, user=request.user) 
            abo.save() 
            return redirect('abonnements',) 
    else: 
        header = 'S\'abonner' 
        return render(request, 'rev/create_abo.html', context={ 
            'header': header, 
            'user': user}) 


@login_required
def reject_abo(request, user_id): 
    user = User.objects.get(pk=user_id) 
    header = 'Opération impossible' 
    return render(request, 'rev/impossible_abo.html', context={ 
        'header': header, 
        'user': user, 
    }) 



@login_required
def block_user(request, block_user_id, user_id): 

    follow = UserFollows.objects.get( 
        user__pk=block_user_id, 
        followed_user__pk=user_id) 
    # print(follow)
    # print(follow.user, follow.followed_user) 

    user = User.objects.get(pk=user_id) 
    blocked_user = User.objects.get(pk=block_user_id) 

    # print('blocked_user id : ', blocked_user.id) 
    # print('blocked_user username : ', blocked_user.username) 

    if request.method == 'POST': 
        follow.delete() 
        
        block = BlockedUsers.objects.create( 
            user=user, blocked_user=blocked_user) 
        block.save() 

        return redirect('abonnements', ) 
    else: 
        header = 'Confirmation de blocage d\'un utilisateur' 
        return render(request, 'rev/block_user.html', context={ 
            'header': header, 
            'blocked_user': blocked_user, 
        }) 


@login_required
def delete_abo(request, abonnements_id): 
    abo = UserFollows.objects.get(id=abonnements_id) 

    if request.method == 'POST': 
        abo.delete() 
        return redirect('abonnements', ) 
    return render(request, 'rev/delete_abo.html', {'abo': abo}) 


@login_required
def delete_review(request, review_id): 
    post = Review.objects.get(id=review_id) 

    if request.method == 'POST': 
        post.delete() 
        return redirect('activity', ) 
    return render(request, 'rev/delete_review.html', context={ 
        'post': post 
    }) 


@login_required
def delete_ticket(request, ticket_id): 
    post = Ticket.objects.get(id=ticket_id) 

    if request.method == 'POST': 
        post.delete() 
        return redirect('activity', ) 
    return render(request, 'rev/delete_ticket.html', context={ 
        'post': post 
    }) 


@login_required 
def create_ticket(request): 
    form = forms.TicketForm() 
    if request.method == 'POST': 
        form = forms.TicketForm( 
            request.POST, request.FILES) 
        if form.is_valid(): 
            ticket = form.save(commit=False) 
            ticket.user = request.user 
            ticket.save() 
            return redirect('home') 
    else: 
        header = 'Créer un ticket' 
        form = forms.TicketForm() 
        return render(request, 'rev/create_ticket.html', context={ 
            'header': header, 
            'form': form}) 


@login_required 
def create_new_review(request): 
    ticket_form = forms.TicketForm() 
    review_form = forms.NewReviewForm() 
    header = "Ecrire une revue et un ticket" 
    if request.method == 'POST': 
        review_form = forms.NewReviewForm(request.POST) 
        create_ticket(request) 
        last_ticket = Ticket.objects.filter().last() 
        if review_form.is_valid(): 
            new_review = review_form.save(commit=False) 
            new_review.ticket = last_ticket 
            new_review.user = request.user 
            new_review.save() 
            return redirect('home') 
    return render(request, 'rev/create_new_review.html', context={ 
        'header': header, 
        'ticket_form': ticket_form, 
        'review_form': review_form, 
        }) 


@login_required 
def create_review(request, ticket_id): 
    ticket = Ticket.objects.get(pk=ticket_id) 
    form_review = forms.ReviewForm() 
    if request.method == 'POST': 
        form_review = forms.ReviewForm(request.POST) 
        if form_review.is_valid(): 
            review = form_review.save(commit=False) 
            review.user = request.user 
            print(review) 
            review.save() 
            return redirect('home') 
    else: 
        header = "Créer une revue" 
        form = forms.ReviewForm(initial={'ticket': ticket}) 
        return render(request, 'rev/create_review.html', context={ 
            'header': header, 
            'ticket': ticket, 
            'form': form, 
        }) 





@login_required 
def activity(request): 
    header = 'Vos posts' 

    user = request.user 
    f_users = helpers.followed_users(user) 

    reviews = helpers.get_users_viewable_reviews(user) 
    reviews = reviews.annotate( 
        content_type=Value('REVIEW', CharField())) 

    tickets = helpers.get_users_viewable_tickets(user, reviews) 
    tickets = tickets.annotate( 
        content_type=Value('TICKET', CharField())) 
    tickets = list(tickets) 

    posts = sorted( 
        chain(reviews, tickets), 
        key=lambda post: post.time_created, 
        reverse=True 
    ) 

    paginator = Paginator(posts, 4) 
    page = request.GET.get("page") 
    page_obj = paginator.get_page(page) 

    return render(request, 'rev/activity.html', context={ 
        'header': header, 
        'user': user, 
        'posts': posts, 
        "page_obj": page_obj, 
    }) 

