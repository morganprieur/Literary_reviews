
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.models import User 
from django.contrib.auth.decorators import login_required 
from django.db.models import CharField, Value 
from itertools import chain 
from django.shortcuts import redirect, render 
from django.views.generic import View 
# from django.views import View as V 

from django.conf import settings 
from reviews.models import Review, Ticket, UserFollows 
from reviews.utils import helpers 
# litrevu\reviews\utils
from . import forms 
from django.db.models import Q 

# ============ login ============================== # 

class SignupPageView(View): 
    template_name = 'rev/signup.html' 
    form_class = forms.SignupForm 

    def get(self, request): 
        form = self.form_class() 
        # print(form.as_p) 
        # message = '' 
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


def logout_user(request):
    logout(request)
    return redirect('home') 


# TODO: set the content of this page : 
@login_required 
def home(request): 
    header = 'Accueil' 

    user = request.user 
    f_users = helpers.followed_users(user) 

    """ ex list of m2m relations 
        # users_groups = request.user.groups.values_list('name', flat = True) 
        # groups_as_list = list(users_groups) 
        # print(str(request.user) + ' permissions : ' + str(groups_as_list)) 
        # return groups_as_list 
    """ 
    reviews = helpers.get_users_viewable_reviews(user, f_users) 
    reviews = reviews.annotate( 
        content_type=Value('REVIEW', CharField())) 
    # returns queryset of reviews
    tickets = helpers.get_users_viewable_tickets(user, f_users, reviews)
    # returns queryset of tickets
    tickets = tickets.annotate( 
        content_type=Value('TICKET', CharField())) 
    tickets = list(tickets) 
    # print(tickets) 
    for review in reviews: 
        for ticket in tickets: 
            # print(review) 
            # print(ticket) 
            if review.ticket_id == ticket.id: 
                tickets.pop(tickets.index(ticket)) 
    # print(tickets) 
    # combine and sort the two types of posts 
    posts = sorted( 
        chain(reviews, tickets), 
        key=lambda post: post.time_created, 
        reverse=True 
    ) 
    # form = forms.Send_ticket_idForm() 

    return render( 
        request, 'rev/home.html', context={ 
            'header': header, 
            'user': user, 
            'followed': f_users, 
            'posts': posts, 
            # 'post': post, 
            # 'form': form, 
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
            return redirect('home') 
    else: 
        header = 'Modifier un ticket' 
        return render(request, 'rev/edit_ticket.html', context={ 
            'header': header, 
            'form': form, 
        }) 

# @login_required
# # @permission_required('blog.change_blog')
# def edit_ticket_blog(request, blog_id):
#     blog = get_object_or_404(models.Blog, id=blog_id)
#     edit_form = forms.BlogForm(instance=blog)
#     delete_form = forms.DeleteBlogForm()
#     if request.method == 'POST':
#         if 'edit_blog' in request.POST:
#             edit_form = forms.BlogForm(request.POST, instance=blog)
#             if edit_form.is_valid():
#                 edit_form.save()
#                 return redirect('home')
#         if 'delete_blog' in request.POST:
#             delete_form = forms.DeleteBlogForm(request.POST)
#             if delete_form.is_valid():
#                 blog.delete()
#                 return redirect('home')
#     context = {
#         'edit_form': edit_form,
#         'delete_form': delete_form,
#     }
#     return render(request, 'blog/edit_blog.html', context=context)


    # return render(request, 'rev/home.html') 
    # return render(request, 'home.html', context={'posts': posts}) 

    # for f in followed: 
    #     tickets = list(Ticket.objects.filter(Q(user=user) | Q(user__id=f.followed_user_id)).order_by('-time_created')) 
    #     reviews = list(Review.objects.filter(Q(user=user) | Q(user__username=user.username)).order_by('-time_created')) 
    # # file deepcode ignore listFromList: <please specify a reason of ignoring this>
    # list(reviews) 
    # for review in reviews: 
    #     for ticket in tickets: 
    #         # print(review) 
    #         # print(ticket) 
    #         if review.ticket_id == ticket.id: 
    #             tickets.pop(tickets.index(ticket)) 
    # # print(tickets) 
    """ ex CDC énoncé 
        def feed(request):
            reviews = get_users_viewable_reviews(request.user)
            # returns queryset of reviews
            reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))
            tickets = get_users_viewable_tickets(request.user)
            # returns queryset of tickets
            tickets = tickets.annotate(content_type=Value('TICKET', CharField()))
            # combine and sort the two types of posts
            posts = sorted(
                ’ chain(reviews, tickets),
                key=lambda post: post.time_created,
                reverse=True
            ) 
            return render(request, 'feed.html', context={'posts': posts}) 
    """ 


    """ ex demo_uthd documents 
        # for ot in ots: 
        #     # filter(Q(firstname='Emil') | Q(firstname='Tobias'))
        #     # documents = Document.objects.filter(work_order__id=ot.id, Q(type='ORDRE DE TRAVAUX') | Q( 
        #           type='COMPTE-RENDU D\'INTERVENTION')) 
        #     documents = Document.objects.filter( 
        #         work_order__id=ot.id, type='ORDRE DE TRAVAUX' 
        #         ) | Document.objects.filter( 
        #         work_order__id=ot.id, type='COMPTE-RENDU D\'INTERVENTION' 
        #     ) 
    """ 

# @login_required 
# def review_snippet(request): 

    

""" marche pas : 
    # TypeError: View.__init__() takes 1 positional argument but 2 were given 
    # try with class LoginView(V): 
    # class LoginPageView(V):
    #     template_name = 'authentication/login.html'
    #     form_class = forms.LoginForm

    #     def get(self, request):
    #         form = self.form_class()
    #         message = ''
    #         return render(request, self.template_name, context={'form': form, 'message': message})
            
    #     def post(self, request):
    #         form = self.form_class(request.POST)
    #         if form.is_valid():
    #             user = authenticate(
    #                 username=form.cleaned_data['username'],
    #                 password=form.cleaned_data['password'],
    #             )
    #             if user is not None:
    #                 login(request, user)
    #                 return redirect('home')
    #         message = 'Identifiants invalides.'
    #         return render(request, self.template_name, context={'form': form, 'message': message})
""" 


@login_required 
def abonnements(request): 
    header = 'Abonnements' 
    users = [] 
    form = forms.UserForm(request.GET) 

    followed = UserFollows.objects.filter( 
        user__username=request.user.username) 
    followers = UserFollows.objects.filter( 
        followed_user__username=request.user.username) 

    if form.is_valid(): 
        username = form.cleaned_data['username'] 
        users = User.objects.filter(username__icontains=username) 

    return render(request, 'rev/abonnements.html', context={ 
            'header': header, 
            'followed': followed, 
            'followers': followers, 
            'users': users, 
            'form': form, 
        } 
    ) 


@login_required 
def create_abo(request, user_id): 
    user = User.objects.get(id=user_id) 

    if request.method == 'POST': 
        abo = UserFollows.objects.create(followed_user=user, user=request.user) 
        # print('abo.followed_user : ', abo.followed_user, 'abo.user : ', abo.user) 
        header = 'Abonnements' 
        abo.save() 
        return redirect('abonnements',) 
    else: 
        header = 'S\'abonner' 
        return render(request, 'rev/create_abo.html', context={ 
            'header': header, 
            'user': user}) 


@login_required
def delete_abo(request, abonnements_id): 
    abo = UserFollows.objects.get(id=abonnements_id) 

    if request.method == 'POST': 
        header = 'Abonnements' 
        abo.delete() 
        return redirect('abonnements', ) 
    return render(request, 'rev/delete_abo.html', {'abo': abo}) 

# # ======== tuto forms.Form // marche pas ======== # 
# if request.method == "POST":
#     form = PostcodeForm(request.POST)
#     if form.is_valid():
#         cd = form.cleaned_data
#         pc = Postcode(
#             start_postcode = cd['start_postcode'], <-- unexpected attribut 'title' (['title]) 
#             end_postcode = cd['end_postcode'],
#             result_measurement_unit = cd['distance_unit']
#         )
#         pc.save()
# # ======== /tuto ======== # 

@login_required 
def create_ticket(request): 
    form = forms.TicketForm() 
    if request.method == 'POST': 
        form = forms.TicketForm( 
            request.POST, request.FILES) 
        # print(request.POST) 
        # print(request.FILES) 
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


#TODO à tester (changé nom du form NewReviewForm) 
# TODO: tester si on désigne un ticket déjà existant 
@login_required 
def create_new_review(request): 
    ticket_form = forms.TicketForm() 
    review_form = forms.NewReviewForm() 
    header = "Ecrire une revue et un ticket" 
    if request.method == 'POST': 
        review_form = forms.NewReviewForm(request.POST) 
        create_ticket(request) 
        last_ticket = Ticket.objects.filter().last() 
        # print(last_ticket.title) 
        if review_form.is_valid(): 
            new_review = NewReviewForm.save(commit=False) 
            new_review.ticket = last_ticket 
            new_review.user = request.user 
            new_review.save() 
            return redirect('home') 
    return render(request, 'rev/create_new_review.html', context={ 
        'header': header, 
        'ticket_form': ticket_form, 
        'review_form': review_form, 
        }) 


#TODO à tester (form -> link) 
@login_required 
def create_review(request, ticket_id): 
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
        # TODO ajouter l'affichage du ticket avant le form 
        header = 'Vous êtes en train de poster en réposne à' 
        ticket = Ticket.objects.get(pk=ticket_id) 
        # print(ticket.pk) 
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

    reviews = Review.objects.filter(user=user) 
    # reviews = helpers.get_users_viewable_reviews(user, f_users) 
    # returns queryset of reviews
    reviews = reviews.annotate( 
        content_type=Value('REVIEW', CharField())) 

    tickets = Ticket.objects.filter(user=user) 
    # tickets = helpers.get_users_viewable_tickets(user, f_users, reviews)
    # returns queryset of tickets
    tickets = tickets.annotate( 
        content_type=Value('TICKET', CharField())) 
    tickets = list(tickets) 

    for review in reviews: 
        for ticket in tickets: 
            if review.ticket_id == ticket.id: 
                tickets.pop(tickets.index(ticket)) 
    print(tickets) 

    # combine and sort the two types of posts 
    posts = sorted( 
        chain(reviews, tickets), 
        key=lambda post: post.time_created, 
        reverse=True 
    ) 

    return render(request, 'rev/activity.html', context={ 
        'header': header, 
        'user': user, 
        'posts': posts, 
    }) 








# ======== forms.Form ======== # 
# @login_required 
# def create_ticket(request): 
#     form = forms.TicketForm() 
#     if request.method == 'POST': 
#         form = forms.TicketForm( 
#             request.POST, request.FILES) 
#         print(request.POST) 
#         print(request.FILES) 
#         if form.is_valid(): 
#             # print(dir(form)) 
#             # ticket = forms.TicketForm( 
#             #     title = cd['title'], 
#             #     description = cd['description'], 
#             #     image = cd['image'] 
#             # ) 
#             # title = form.cleaned_data['title'] 
#             # description = form.cleaned_data['description'] 
#             # image = form.cleaned_data['image'] 
#             # ticket = Ticket.objects.create(form) 
#             print(dir(forms.TicketForm)) 
#             cd = form.cleaned_data 
#             ticket = forms.TicketForm( 
#                 title = cd['title'], 
#                 description = cd['description'], 
#                 image = cd['image'] 
#             ) 
#             ticket.user = request.user 
#             # print(ticket) 
#             ticket.save() 
#             # ticket = Ticket.objects.create(**form.cleaned_data) 
#             return redirect('home') 
#     else: 
#         # if request.method == 'GET': 
#         header = 'Créer un ticket' 
#         form = forms.TicketForm() 
#         return render(request, 'rev/create_ticket.html', context={ 
#             'header': header, 
#             'form': form}) 
# ======== forms.Form ======== # 



# # listings/views.py
# def band_delete(request, id):
#     band = Band.objects.get(id=id)  # nécessaire pour GET et pour POST

#     if request.method == 'POST':
#         # supprimer le groupe de la base de données
#         band.delete()
#         # rediriger vers la liste des groupes
#         return redirect('band_list')
#     # pas besoin de « else » ici. Si c'est une demande GET, continuez simplement
#     return render(request,
#                     'listings/band_delete.html',
#                     {'band': band})





# La classe LoginPageView est remplacée par django.contrib.auth.views.LoginView (urls.py) 
# class LoginPageView(View):
#     template_name = 'uthdemo/login.html'
#     form_class = forms.LoginForm

#     def get(self, request):
#         form = self.form_class()
#         message = ''
#         return render(request, self.template_name, context={'form': form, 'message': message})

#     def post(self, request):
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             user = authenticate(
#                 username=form.cleaned_data['username'],
#                 password=form.cleaned_data['password'],
#             )
#             if user is not None:
#                 login(request, user)
#                 return redirect('home')
#         message = 'Identifiants invalides.'
#         return render(request, self.template_name, context={'form': form, 'message': message})

""" réponse chatGPT 
    # views.py
    from django.shortcuts import render
    from .models import Ticket
    from .forms import TicketForm

    def my_view(request):
        # Supposons que vous récupérez une liste de tickets depuis la base de données
        tickets = Ticket.objects.all()

        if request.method == 'POST':
            # Traitement du formulaire si soumis
            pass
        else:
            # Créer une liste de formulaires préremplis avec les données de chaque ticket
            forms = [TicketForm(initial={'title': ticket.title}) for ticket in tickets]

        return render(request, 'template.html', {'forms': forms})

    {# template.html #}
    {% for form in forms %}
        <p>{{ form.instance.title }} (ID: {{ form.instance.id }})</p>
        <form action="../create_review/" method="POST">
            {% csrf_token %}
            {{ form.as_p }}
            <button type="submit">Créer une revue</button>
        </form>
    {% endfor %}
""" 





