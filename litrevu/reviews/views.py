
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.models import User 
from django.contrib.auth.decorators import login_required 
from django.shortcuts import redirect, render 
from django.views.generic import View 
# from django.views import View as V 

from django.conf import settings 
from reviews.models import Review, Ticket, UserFollows 
from . import forms 


# ============ login ============================== # 

class SignupPageView(View): 
    template_name = 'rev/signup.html' 
    form_class = forms.SignupForm 

    def get(self, request): 
        form = self.form_class() 
        print(form.as_p) 
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


# TODO: set the content of this page : 
@login_required 
def home(request): 
    header = 'Accueil' 
    # test = 'Hello home' 

    followed = UserFollows.objects.filter( 
        user__username=request.user.username) 

    tickets = Ticket.objects.all() 
    """ 
        # ots = Work_order.objects.all() 
        # ots_count = ots.count 
        # for ot in ots: 
        #     # filter(Q(firstname='Emil') | Q(firstname='Tobias'))
        #     # documents = Document.objects.filter(work_order__id=ot.id, Q(type='ORDRE DE TRAVAUX') | Q( 
        #           type='COMPTE-RENDU D\'INTERVENTION')) 
        #     documents = Document.objects.filter( 
        #         work_order__id=ot.id, type='ORDRE DE TRAVAUX' 
        #         ) | Document.objects.filter( 
        #         work_order__id=ot.id, type='COMPTE-RENDU D\'INTERVENTION' 
        #     ) 
        #     docs_count = documents.count 
        # ---- 
        # x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        # if x_forwarded_for:
        #     ip = x_forwarded_for.split(',')[0]
        # # ip = '90.51.91.219' 
        # else:
        #     ip = request.META.get('REMOTE_ADDR') 
        # ---- 
    """ 
    return render( 
        request, 'rev/home.html', context={ 
            'header': header, 
            'followed': followed, 
            'tickets': tickets, 
        } 
    ) 
    # ---- 
    # "https://api-adresse.data.gouv.fr/search/?q==7+bd+lamarck+bourges&limit=1" 
    # ---- 
    # return HttpResponse("Welcome! You are visiting from: {}".format(ip)) 
    # ---- 

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
        print(request.POST) 
        print(request.FILES) 
        if form.is_valid(): 
            print(dir(forms.TicketForm)) 
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
def create_review(request): 
    form = forms.ReviewForm() 
    if request.method == 'POST': 
        form = forms.ReviewForm(request.POST) 
        print(request.POST) 
        if form.is_valid(): 
            # print(dir(forms.ReviewForm)) 
            review = form.save(commit=False) 
            # review.ticket = none 
            review.user = request.user 
            review.save() 
            return redirect('home') 
    else: 
        header = 'Créer une revue' 
        form = forms.ReviewForm() 
        return render(request, 'rev/create_review.html', context={ 
            'header': header, 
            'form': form}) 


# # ======== tuto ModelForm ======== # 
# blog/views.py
# from django.shortcuts import redirect, render
# from . import forms

# @login_required
# def photo_upload(request):
#     form = forms.PhotoForm()
#     if request.method == 'POST':
#         form = forms.PhotoForm( 
#             request.POST, request.FILES)
#         if form.is_valid():
#             photo = form.save(commit=False)
#             # set the uploader to the user before saving the model
#             photo.uploader = request.user
#             # now we can save
#             photo.save()
#             return redirect('home')
#     return render(request, 'blog/photo_upload.html', context={'form': form})
# # ======== /tuto ======== # 

# TODO: corriger pour l'utiliser à la place de ModelForm 
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


# reviews/views.py 
def logout_user(request):
    logout(request)
    return redirect('home')
    # return redirect('login')


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

