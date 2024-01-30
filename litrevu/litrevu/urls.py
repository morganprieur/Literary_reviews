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
    path('abonnements/', views.abonnements, name='abonnements'), 

    path('create_abo.html/<user_id>/', views.create_abo, name='create-abo'), 
    path('create_new_review/', views.create_new_review, name='create-new-review'), 
    path('create_review/<ticket_id>/', views.create_review, name='create-review'), 
    path('create_ticket/', views.create_ticket, name='create-ticket'), 

    path('block_user/<block_user_id>/<user_id>', views.block_user, name='block-user'), 
    # block-user' with keyword arguments '{'blocked_user_id': 19, 'user_id': 7}' not found. 1 pattern(s) tried: ['block_user/block_user_id/user_id\\Z 
    path('impossible_abo/', views.create_abo, name='create-abo'), 

    path('delete_abo/<abonnements_id>/', views.delete_abo, name='delete-abo'), 
    path('delete_review/<review_id>/', views.delete_review, name='delete-review'), 
    path('delete_ticket/<ticket_id>/', views.delete_ticket, name='delete-ticket'), 

    path('edit_review/<review_id>/', views.edit_review, name='edit-review'), 
    path('edit_ticket/<ticket_id>/', views.edit_ticket, name='edit-ticket'), 

    # authentication 
    path('login/', LoginView.as_view( 
        template_name='rev/login.html', 
        redirect_authenticated_user=False), 
        name='login'), 
    path('logout/', views.logout_user, name='logout'), 
    path('signup/', views.SignupPageView.as_view(), name='signup'), 

] 

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 

