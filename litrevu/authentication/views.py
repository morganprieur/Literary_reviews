from django.shortcuts import render

# import des fonctions authenticate, login et logout 
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required 


# ============ login ============================== # 

# # authentication/views.py
# from django.contrib.auth import authenticate, login, logout
# from django.shortcuts import redirect, render

# from . import forms 


# # blog/views.py 
# def logout_user(request):
#     logout(request)
#     return redirect('login')

# # def signup_page(request):
# #     form = forms.SignupForm()
# #     if request.method == 'POST':
# #         form = forms.SignupForm(request.POST)
# #         if form.is_valid():
# #             user = form.save()
# #             # auto-login user
# #             login(request, user)
# #             return redirect(settings.LOGIN_REDIRECT_URL)
# #     return render(request, 'uthdemo/signup.html', context={'form': form}) 


# class SignupPageView(View): 
#     template_name = 'uthdemo/signup.html' 
#     form_class = forms.SignupForm 

#     def get(self, request): 
#         form = self.form_class() 
#         # message = '' 
#         return render(request, self.template_name, context={'form': form}) 

#     def post(self, request): 
#         form = self.form_class(request.POST) 
#         if form.is_valid(): 
#             user = form.save()
#             # auto-login user
#             login(request, user)
#             return redirect(settings.LOGIN_REDIRECT_URL) 


# # @with_ip_geolocation 
@login_required 
def home(request): 
    # print(f'dir(request) : {dir(request)}') 

    test = 'Hello home' 

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
        request, 'auth/home.html', context={ 
            'test': test, 
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


# @login_required 
# def work_order_detail(request, work_order_id): 
#     print('request : ', request) 
#     # template = loader.get_template('signup.html')  # pour classe 
#     ot = get_object_or_404(Work_order, id=work_order_id)  # Work_order.objects.get(uuid=request) 
#     documents = Document.objects.filter(work_order__id=ot.id) 
#     docs_count = documents.count 
#     return render( 
#         request, 'uthdemo/work_order_detail.html', context={ 
#             'ot': ot, 
#             'documents': documents, 
#             'docs_count': docs_count  
#         } 
#     ) 
#     # return render( 
#     #     request, 'uthdemo/work_order.html', context={ 
#     #         'ot': ot, 
#     #         'documents': documents 
#     #     } 
#     # ) 


# @login_required 
# def ebp_detail(request, ebp_id): 
#     # print(f"ebp id : {Ebp.id}") 
#     ebp = get_object_or_404(Ebp, id=ebp_id) 
#     ots = Work_order.objects.filter(ebp__id=ebp_id) 
#     # documents = Document.objects.filter(work_order__id=ot.id) 
#     # documents = Document.objects.filter(work_order__ebp__id=ebp.id) 
#     docs = Document.objects.filter(work_order__ebp__id=ebp.id) 
#     # print(f"documents : {documents}") 
#     documents = [] 
#     for doc in docs: 
#         # filter(Q(firstname='Emil') | Q(firstname='Tobias'))
#         # if 'ORDRE DE TRAVAUX' not in doc.type | 'COMPTE-RENDU' not in doc.type: 
#         if 'DOCUMENTATION TECHNIQUE' in doc.type: 
#             document = doc 
#             documents.append(document) 

#     return render( 
#         request, 'uthdemo/ebp_detail.html', context={ 
#             'ebp': ebp, 
#             'ots': ots, 
#             'documents': documents 
#         } 
#     ) 


# @login_required 
# def pt_detail(request, pt_id): 
#     pt = get_object_or_404(Tech_point, id=pt_id) 
#     ebps = Ebp.objects.filter(tech_point__id=pt_id) 
#     ots = Work_order.objects.filter(tech_point__id=pt_id) 
#     return render( 
#         request, 
#         'uthdemo/pt_detail.html', 
#         context={ 
#             'pt': pt, 
#             'ebps': ebps, 
#             'ots': ots, 
#         } 
#     ) 

# # # blog/views.py
# # # from django.shortcuts import get_object_or_404
# # @login_required
# # def view_blog(request, blog_id):
# #     blog = get_object_or_404(models.Blog, id=blog_id)
# #     return render(request, 'blog/view_blog.html', {'blog': blog})


# # La classe LoginPageView est remplacée par django.contrib.auth.views.LoginView (urls.py) 
# # class LoginPageView(View):
# #     template_name = 'uthdemo/login.html'
# #     form_class = forms.LoginForm

# #     def get(self, request):
# #         form = self.form_class()
# #         message = ''
# #         return render(request, self.template_name, context={'form': form, 'message': message})

# #     def post(self, request):
# #         form = self.form_class(request.POST)
# #         if form.is_valid():
# #             user = authenticate(
# #                 username=form.cleaned_data['username'],
# #                 password=form.cleaned_data['password'],
# #             )
# #             if user is not None:
# #                 login(request, user)
# #                 return redirect('home')
# #         message = 'Identifiants invalides.'
# #         return render(request, self.template_name, context={'form': form, 'message': message})

