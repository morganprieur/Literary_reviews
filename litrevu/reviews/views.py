
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
    """ Displays the signup page or registers a new User instance. 
        Args: 
            self (the view class). 
            request (django.core.handlers.wsgi.WSGIRequest): 
                The infos passed while calling and loading the page. 
        Returns:
            HttpResponse: "render" and "redirect" are shortcuts for HttpResponse. 
    """ 
    template_name = 'rev/signup.html' 
    form_class = forms.SignupForm 

    def get(self, request): 
        " Displays the form to sign-up. " 
        form = self.form_class() 
        return render( 
            request, 
            self.template_name, 
            context={'form': form}) 

    def post(self, request): 
        " Sends the filled form. " 
        form = self.form_class(request.POST) 
        if form.is_valid(): 
            " Registers the new User instance. " 
            user = form.save()
            # auto-login user: 
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL) 
        else: 
            " Displays the form again with the errors. " 
            message = 'Veuillez suivre les instructions' 
            return render(request, self.template_name, context={ 
                'form': form, 
            }) 


def logout_user(request): 
    """ Logs out the logged-in user.  
        Args: 
            request (django.core.handlers.wsgi.WSGIRequest): 
                The infos passed while calling and loading the page. 
                'user': the logged-in User instance to log-out. 
        Returns:
            HttpResponse: "render" and "redirect" are shortcuts for HttpResponse. 
    """ 
    logout(request)
    return redirect('home') 


@login_required 
def home(request): 
    """ Displays the flux page. 
        Args: 
            request (django.core.handlers.wsgi.WSGIRequest): 
                The infos passed while calling and loading the page. 
                'user': the logged-in User instance. 
        Returns:
            HttpResponse: "render" and "redirect" are shortcuts for HttpResponse. 
    """ 
    header = 'Accueil' 

    user = request.user 
    f_users = helpers.followed_users(user) 

    """ The users' reviews and the reviews from his/her subscriptions' 
        with the belonging tickets. 
    """ 
    reviews = helpers.get_users_viewable_reviews(user) 
    reviews = reviews.annotate( 
        content_type=Value("REVIEW", CharField())) 

    """ The users' tickets and the tickets from his/her subscriptions' 
        with the belonging reviews, excluding the tickets already stored with a review. 
    """ 
    tickets = helpers.get_users_viewable_tickets(user, reviews) 
    tickets = tickets.annotate(content_type=Value("TICKET", CharField())) 

    " combine and sort the two types of posts. " 
    posts = sorted( 
        chain(reviews, tickets), 
        key=lambda post: post.time_created, 
        reverse=True 
    ) 

    " Pagination with 4 posts per page. " 
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
def activity(request): 
    """ Displays the user's activity page, included if related 
        to the activity of another user. 
        Args: 
            request (django.core.handlers.wsgi.WSGIRequest): 
                The infos passed while calling and loading the page. 
                'user': the logged-in User instance. 
        Returns:
            HttpResponse: "render" and "redirect" are shortcuts for HttpResponse. 
    """ 
    header = 'Vos posts' 
    user = request.user 
    followed = helpers.followed_users(user) 

    " The users' reviews with the belonging tickets. " 
    reviews_qs = Review.objects.select_related("ticket").filter( 
        Q(user__in=UserFollows.objects.filter(user=user)\
            .values("followed_user")) | Q(user=user) 
    ) 
    reviews_qs = reviews_qs.annotate( 
        content_type=Value('REVIEW', CharField())) 
    tickets = Ticket.objects.filter( 
        user=user 
    ).exclude(id__in=reviews_qs.values("ticket_id")) 
    reviews = [] 
    for review in reviews_qs: 
        if (not(review.ticket.user == review.user)) | (review.user==user): 
            reviews.append(review) 
    """ The users' tickets with the belonging reviews, 
        excluding the tickets already stored with a review. 
    """ 
    tickets = tickets.annotate( 
        content_type=Value('TICKET', CharField())) 

    " combine and sort the two types of posts. " 
    posts = sorted( 
        chain(reviews, tickets), 
        key=lambda post: post.time_created, 
        reverse=True 
    ) 

    " Pagination with 4 posts per page. " 
    paginator = Paginator(posts, 4) 
    page = request.GET.get("page") 
    page_obj = paginator.get_page(page) 

    return render(request, 'rev/activity.html', context={ 
        'header': header, 
        'user': user, 
        'posts': posts, 
        'page_obj': page_obj, 
        'followed': followed, 
    }) 


@login_required 
def abonnements(request): 
    """ Displays the user's subscriptions page. 
        Args: 
            request (django.core.handlers.wsgi.WSGIRequest): 
                The infos passed while calling and loading the page. 
                'user': the logged-in User instance. 
                'GET': the data sent with the search form. 
        Returns:
            HttpResponse: "render" and "redirect" are shortcuts for HttpResponse. 
    """ 
    header = 'Abonnements' 
    user = request.user 

    " Search form to find other User instances. " 
    users = [] 
    form = forms.UserForm(request.GET) 
    if form.is_valid(): 
        username = form.cleaned_data['username'] 
        users = User.objects.filter(username__icontains=username) 

    " Subscriptions and followers to display. " 
    followed = UserFollows.objects.filter( 
        user__username=request.user.username) 
    followers = UserFollows.objects.filter( 
        followed_user__username=request.user.username) 

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
    """ Follow a user: 
            - Check if the user has not been blocked by tue the user who he wants to follow ; 
            - Check if the user doesn't already follow this user ; 
            If not, registers a subscription of the logged-in user to the one with 
                ID=user_id. 
        Args:
            request (django.core.handlers.wsgi.WSGIRequest): 
                The infos passed while calling and loading the page. 
            user_id (int): The logged-in user. 
        Returns:
            HttpResponse: "render" and "redirect" are shortcuts for HttpResponse. 
    """ 
    user_follow = User.objects.get(id=user_id) 
    message = '' 
    """ Check if the user has been blocked by the User instance 
        with ID == user_id. 
    """ 
    blocked_users = BlockedUsers.objects.filter( 
        user=user_follow, 
        blocked_user=request.user) 
    """ Check if the followed user has been already followed 
        by this user. 
    """ 
    follow_binomials = UserFollows.objects.filter( 
        user=request.user, 
        followed_user=user_follow) 
    if follow_binomials: 
        message = 'Vous êtes déjà abonné à cet utilisateur.' 
        return render(request, 'rev/create_abo.html', context={'message': message}) 
    elif blocked_users: 
        message = f'''Impossible de vous abonner à cet utilisateur 
            {user_follow.username}.''' 
        return render(request, 'rev/create_abo.html', context={'message': message}) 
    elif request.method == 'POST': 
        " If the subscription can be set " 
        abo = UserFollows.objects.create( 
            followed_user=user_follow, user=request.user) 
        abo.save() 
        return redirect('abonnements',) 
    else: 
        header = 'S\'abonner' 
        return render(request, 'rev/create_abo.html', context={'header': header, 
            'user': user_follow}) 


@login_required 
def create_ticket(request): 
    """ Displays the empty TicketForm or sends the filled form. 
        If the form has been sent and is valide: 
            - Creates a new Ticket instance ; 
            - Redirects to the flux page. 
        If the form has been sent and is not valide, a popup 
            generated by Django forms alerts for the error.. 
        If the form has not been sent, the empty form is displayed. 
        Args: 
            request (django.core.handlers.wsgi.WSGIRequest): 
                The infos passed while calling and loading the page. 
                'user': the logged-in User instance. 
                'POST': the data sent with the TicketForm. 
                'FILES': the files sent with the TicketForm. 
        Returns: 
            HttpResponse: "render" and "redirect" are shortcuts for HttpResponse. 
    """ 
    form = forms.TicketForm() 
    if request.method == 'POST': 
        form = forms.TicketForm( 
            request.POST, request.FILES) 
        if form.is_valid(): 
            """ Registers the new Ticket instance with the logged-in 
                user as the ticket's user. 
            """ 
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
    """ Displays the empty ReviewForm and TicketForm or sends the filled forms in the 
        same action. 
        The ticketForm is treated by the create_ticket fuction. 
        If the ReviewForm has been sent and is valide: 
            - Creates a new Review instance with the last registered 
                Ticket instance as a ticket ; 
            - Redirects to the flux page. 
        If the ReviewForm has been sent and is not valide, a popup 
            generated by Django forms alerts for the error. 
        If the forms have not been sent, the empty forms are displayed. 
        Args: 
            request (django.core.handlers.wsgi.WSGIRequest): 
                The infos passed while calling and loading the page. 
                'user': the logged-in User instance. 
                'POST': the data sent with the both forms. 
                'FILES': the files sent with the TicketForm. 
        Returns: 
            HttpResponse: "render" and "redirect" are shortcuts for HttpResponse. 
    """ 
    ticket_form = forms.TicketForm() 
    review_form = forms.NewReviewForm() 
    header = "Ecrire une revue et un ticket" 
    if request.method == 'POST': 
        review_form = forms.NewReviewForm(request.POST) 
        " Call to the create_ticket function to treat the TicketForm. " 
        create_ticket(request) 
        last_ticket = Ticket.objects.filter().last() 
        """ Register the new Review instance 
            with the last registered Ticket instance as a ticket. 
        """ 
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
    """ Displays the empty ReviewForm or sends the filled one. 
        If the form has been sent and is valide: 
            - Creates a new Review instance ; 
            - Redirects to the flux page. 
        If the form has been sent and is not valide, a popup 
            generated by Django forms alerts for the error. 
        If the form has not been sent, the empty form is displayed. 
        Args: 
            request (django.core.handlers.wsgi.WSGIRequest): 
                The infos passed while calling and loading the page. 
                'user': the logged-in User instance. 
                'POST': the data sent with the ReviewForm. 
        Returns: 
            HttpResponse: "render" and "redirect" are shortcuts for HttpResponse. 
    """ 
    ticket = Ticket.objects.get(pk=ticket_id) 
    form_review = forms.ReviewForm() 
    if request.method == 'POST': 
        form_review = forms.ReviewForm(request.POST) 
        if form_review.is_valid(): 
            " Register the new Review instance with the got Ticket instance as a ticket. " 
            review = form_review.save(commit=False) 
            review.user = request.user 
            review.save() 
            " Redirects to the user's flux page. " 
            return redirect('home') 
    else: 
        " If the form has not been sent, displays the empty form. " 
        header = "Créer une revue" 
        form = forms.ReviewForm(initial={'ticket': ticket}) 
        return render(request, 'rev/create_review.html', context={ 
            'header': header, 
            'ticket': ticket, 
            'form': form, 
        }) 


@login_required
def block_user(request, block_user_id, user_id): 
    """ Block a user: 
            - Delete the subscription of the blocked_user  to the logged-in user ; 
            - register the blocked binomial into the blockedUsers table ; 
            - Prevent the blocked_user to follow again the logged-in user 
                (into create_abo view). 
        Args:
            request (django.core.handlers.wsgi.WSGIRequest): 
                The infos passed while calling and loading the page. 
            block_user_id (int): The user-to-block's ID. 
            user_id (int): The connected user. 
        Returns:
            _type_: _description_
    """ 
    subscription = UserFollows.objects.get( 
        user__pk=block_user_id, 
        followed_user__pk=user_id) 

    user = User.objects.get(pk=user_id) 
    blocked_user = User.objects.get(pk=block_user_id) 

    if request.method == 'POST': 
        subscription.delete() 

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
def edit_ticket(request, ticket_id): 
    """ Displays the empty TicketForm or sends the filled one 
        and treats the data. 
        If the form has been sent and is valide: 
            - Edits the Ticket instance ; 
            - Redirects to the user's activity page. 
        If the form has been sent and is not valide, a popup 
            generated by Django forms alerts for the error. 
        If the form has not been sent, the empty form is displayed. 
        Args: 
            request (django.core.handlers.wsgi.WSGIRequest): 
                The infos passed while calling and loading the page. 
                'user': the logged-in User instance. 
                'ticket_id': The ID the ticket to edit. 
                'POST': the data sent with the TicketForm. 
        Returns: 
            HttpResponse: "render" and "redirect" are shortcuts for HttpResponse. 
    """ 
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
    """ Displays the empty ReviewForm or sends the filled one 
        and treats the data. 
        If the form has been sent and is valide: 
            - Edit the Review instance ; 
            - Redirects to the user's activity page. 
        If the form has been sent and is not valide, a popup 
            generated by Django forms alerts for the error. 
        If the form has not been sent, the empty form is displayed. 
        Args: 
            request (django.core.handlers.wsgi.WSGIRequest): 
                The infos passed while calling and loading the page. 
                'user': the logged-in User instance. 
                'review_id': The ID the review to edit. 
                'POST': the data sent with the ReviewForm. 
        Returns: 
            HttpResponse: "render" and "redirect" are shortcuts for HttpResponse. 
    """ 
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
def delete_abo(request, abonnements_id): 
    """ Displays the data sent with the link from the "abonnements" 
        page for confirmation, and two buttons for delete the 
        subscription or return to the user's subscriptions page. 
        If the form has been sent: 
            - Deletes the UserFollows instance with the abonnements_id 
                as a followed_user.id ; 
            - Redirects to the user's subscriptions page. 
        If the form has not been sent, the data to confirm and the two 
            buttons are displayed. 
        Args: 
            request (django.core.handlers.wsgi.WSGIRequest): 
                The infos passed while calling and loading the page. 
                'user': the logged-in User instance. 
                'review_id': The ID the UserFollows instance to delete. 
                'POST': the data sent with the ReviewForm. 
        Returns: 
            HttpResponse: "render" and "redirect" are shortcuts for HttpResponse. 
    """ 
    abo = UserFollows.objects.get(id=abonnements_id) 

    if request.method == 'POST': 
        abo.delete() 
        return redirect('abonnements', ) 
    return render(request, 'rev/delete_abo.html', {'abo': abo}) 


@login_required
def delete_review(request, review_id): 
    """ Displays the data sent with the link from the activity 
        page for confirmation, and two buttons for delete the 
        review or return to the user's activity page. 
        If the form has been sent: 
            - Deletes the Review instance with the review_id as an id ; 
            - Redirects to the user's activity page. 
        If the form has not been sent, the data to confirm and the two 
            buttons are displayed. 
        Args: 
            request (django.core.handlers.wsgi.WSGIRequest): 
                The infos passed while calling and loading the page. 
                'user': the logged-in User instance. 
                'review_id': The ID the review to delete. 
                'POST': the data sent with the ReviewForm. 
        Returns: 
            HttpResponse: "render" and "redirect" are shortcuts for HttpResponse. 
    """ 
    post = Review.objects.get(id=review_id) 

    if request.method == 'POST': 
        post.delete() 
        return redirect('activity', ) 
    return render(request, 'rev/delete_review.html', context={ 
        'post': post 
    }) 


@login_required
def delete_ticket(request, ticket_id): 
    """ Displays the data sent with the link from the activity 
        page for confirmation, and two buttons for delete the 
        ticket or return to the user's activity page. 
        If the form has been sent: 
            - Deletes the Review instance with the ticket_id as an id ; 
            - Redirects to the user's activity page. 
        If the form has not been sent, the data to confirm and the two 
            buttons are displayed. 
        Args: 
            request (django.core.handlers.wsgi.WSGIRequest): 
                The infos passed while calling and loading the page. 
                'user': the logged-in User instance. 
                'ticket_id': The ID the review to delete. 
                'POST': the data sent with the TicketForm. 
        Returns: 
            HttpResponse: "render" and "redirect" are shortcuts for HttpResponse. 
    """ 
    f_users = helpers.followed_users(request.user) 

    ticket = Ticket.objects.get(id=ticket_id) 
    post = Review.objects.get(ticket=ticket) 

    if request.method == 'POST': 
        ticket.delete() 
        post.delete() 
        return redirect('activity', ) 
    return render(request, 'rev/delete_ticket.html', context={ 
        'post': post, 
        'followed': f_users, 
    }) 



