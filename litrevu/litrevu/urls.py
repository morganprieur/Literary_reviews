"""
URL configuration for litrevu project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
""" 
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView 
from django.urls import path 
from reviews import views 

# afficher images (https://zestedesavoir.com/tutoriels/598/developpez-votre-site-web-avec-le-framework-django/263_premiers-pas/1525_la-gestion-des-fichiers/) 
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls), 

    path('home/', views.home, name='home'), 
    path('activity/', views.activity, name='activity'), 

    path('create_ticket/', views.create_ticket, name='create-ticket'), 
    # path('create_review/', views.create_review, name='create-review'), 
    path('create_review/<ticket_id>/', views.create_review, name='create-review'), 
    # path('create_new_review/', views.create_new_review, name='create-new-review'), 

    path('edit_ticket/<ticket_id>/', views.edit_ticket, name='edit-ticket'), 

    # abonnements 
    path('abonnements/', views.abonnements, name='abonnements'), 
    # path("about/", GreetingView.as_view(greeting="G'day")),
    path('create_abo.html/<user_id>/', views.create_abo, name='create-abo'), 
    path('delete_abo/<abonnements_id>/', views.delete_abo, name='delete-abo'), 
    # path('delete_abo/', views.delete_abo, name='delete-abo'), 

    # authentication 
    path('login/', LoginView.as_view( 
        template_name='rev/login.html', 
        redirect_authenticated_user=False), 
        # redirect_authenticated_user=True),  # redirects to accounts/user//?next=home/ 
        name='login'), 
    path('logout/', views.logout_user, name='logout'), 
    path('signup/', views.SignupPageView.as_view(), name='signup'), 


    # path('login', LoginView.as_view( 
    #     template_name='uthdemo/login.html', 
    #     redirect_authenticated_user=True), 
    #     name='login'), 

    #     # path('', LoginView.as_view( 
    #     #         template_name='uthdemo/login.html', 
    #     #         redirect_authenticated_user=True), 
    #     #     name='login'), 
    #     # path('', uthdemo.views.LoginPageView.as_view(), name='login'),
    #     # path('', uthdemo.views.login_page, name='login'), 
    #     
    #     
    #     # path('signup/', uthdemo.views.signup_page, name='signup'), 

] 

# fotoblog/urls.py 
# TODO: only in DEBUG mode, change ASAP 
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 


# # ======== Exemple demo ======== # 

# # fotoblog 
# from django.conf import settings 
# from django.conf.urls.static import static 

# # uthdemo 
# from uthdemo import views 
# from rest_framework import routers 

# api : 
# router = routers.DefaultRouter() 
# router.register(r'users', views.UserViewSet) 

# app_name = 'uthdemo' 

# api : 
# router.register(r'documents', views.DocumentViewSet) 
# router.register(r'work_orders', views.Work_orderViewSet) 
# router.register(r'ebp', views.EbpViewSet) 

# urlpatterns = [ 
#   # api : 
#     path('uthdemo/', include('uthdemo.urls')), 
#     path('', include(router.urls)), 

#     path('work_order_detail/<work_order_id>/', uthdemo.views.work_order_detail, name='work_order_detail'), 
#     # http://localhost:9000/work_orders/?d8f47724-4eea-4924-8ffe-38e61f4a6d74/ 
#     path('ebp_detail/<ebp_id>/', uthdemo.views.ebp_detail, name='ebp_detail'), 
#     path('pt_detail/<pt_id>/', uthdemo.views.pt_detail, name='pt_detail'), 

#     # fotoblog tuto 
#     # path('blog/<int:blog_id>', blog.views.view_blog, name='view_blog'), 



