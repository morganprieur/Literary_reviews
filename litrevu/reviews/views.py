
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
    # print(f'dir(request) : {dir(request)}') 
    # print(f'request : {request}') 

    header = 'home' 
    # test = 'Hello home' 

    followed = UserFollows.objects.filter( 
        user__username=request.user.username) 

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
    return render( 
        request, 'rev/home.html', context={ 
            'header': header, 
            # 'test': test, 
            'followed': followed, 
            # 'ots': ots, 
            # 'ots_count': ots_count, 
            # 'documents': documents, 
            # 'docs_count': docs_count, 
            # 'ip': ip, 
            # 'location': location 
        } 
    ) 
    # ---- 
    # "https://api-adresse.data.gouv.fr/search/?q==7+bd+lamarck+bourges&limit=1" 
    # ---- 
    # return HttpResponse("Welcome! You are visiting from: {}".format(ip)) 
    # ---- 


# marche pas : 
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
    # print(user_id) 
    # print(request.user.id) 
    user = User.objects.get(id=user_id) 
    # print(user) 

    if request.method == 'POST': 
        abo = UserFollows.objects.create(followed_user=user, user=request.user) 
        print('abo.followed_user : ', abo.followed_user, 'abo.user : ', abo.user) 
        header = 'Abonnements' 
        abo.save() 
        # return redirect('band_list') 
        return redirect('abonnements',)  # context={ 
        #     'header': header, 
        # }) 
    else: 
        header = 'S\'abonner' 
        return render(request, 'rev/create_abo.html', context={ 
            'header': header, 
            'user': user}) 



    # def post(self, request): 
    #     form = self.form_class(request.POST) 
    #     if form.is_valid(): 
    #         user = form.save()
    #         # auto-login user: 
    #         login(request, user)
    #         return redirect(settings.LOGIN_REDIRECT_URL) 



@login_required
def delete_abo(request, abonnements_id): 
    abo = UserFollows.objects.get(id=abonnements_id) 
    # print('abo.id : ', abo.id, 'abo.followed_user : ', abo.followed_user) 

    if request.method == 'POST': 
        # abo = UserFollows.objects.get(id=abonnements_id) 
        header = 'Abonnements' 
        abo.delete() 
        # return redirect('band_list') 
        return redirect('abonnements', ) 
    return render(request, 'rev/delete_abo.html', {'abo': abo}) 
        # 'header': header, 


# # ======== tuto ======== # 
# from .forms import NameForm
# def get_name(request):
#     # if this is a POST request we need to process the form data
#     if request.method == "POST":
#         # create a form instance and populate it with data from the request:
#         form = NameForm(request.POST)
#         # check whether it's valid:
#         if form.is_valid():
#             # process the data in form.cleaned_data as required
#             # ...
#             # redirect to a new URL:
#             return HttpResponseRedirect("/thanks/")

#     # if a GET (or any other method) we'll create a blank form
#     else:
#         form = NameForm()

#     return render(request, "name.html", {"form": form})
# # ======== /tuto ======== # 


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

