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
from django.urls import path 
import authentication.views 

from django.contrib.auth.views import LoginView, LogoutView 
# from uthdemo.views import SignupPageView 

# afficher images (https://zestedesavoir.com/tutoriels/598/developpez-votre-site-web-avec-le-framework-django/263_premiers-pas/1525_la-gestion-des-fichiers/) 
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls), 

    path('home/', authentication.views.home, name='home'), 

    path('login/', LoginView.as_view( 
        template_name='auth/login.html', 
        redirect_authenticated_user=True), 
        name='login'), 


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
    #     path('logout/', uthdemo.views.logout_user, name='logout'), 
    #     path('signup', SignupPageView.as_view(), name='signup'), 
    #     # path('signup/', uthdemo.views.signup_page, name='signup'), 

] 


# # ======== Exemple demo ======== # 

# # fotoblog 
# from django.conf import settings 
# from django.conf.urls.static import static 

# # uthdemo 
# from uthdemo import views 
# from rest_framework import routers 

# router = routers.DefaultRouter() 
# router.register(r'users', views.UserViewSet) 

# app_name = 'uthdemo' 

# router.register(r'documents', views.DocumentViewSet) 
# router.register(r'work_orders', views.Work_orderViewSet) 
# router.register(r'ebp', views.EbpViewSet) 

# urlpatterns = [ 

#     path('uthdemo/', include('uthdemo.urls')), 
#     path('', include(router.urls)), 


#     path('work_order_detail/<work_order_id>/', uthdemo.views.work_order_detail, name='work_order_detail'), 
#     # http://localhost:9000/work_orders/?d8f47724-4eea-4924-8ffe-38e61f4a6d74/ 
#     path('ebp_detail/<ebp_id>/', uthdemo.views.ebp_detail, name='ebp_detail'), 
#     path('pt_detail/<pt_id>/', uthdemo.views.pt_detail, name='pt_detail'), 

#     # fotoblog tuto 
#     # path('blog/<int:blog_id>', blog.views.view_blog, name='view_blog'), 

#     # api-auth/login/ 
#     path('api-auth/', include('rest_framework.urls', namespace='rest_framework')), 

# ] 

# fotoblog/urls.py 
# TODO: only in DEBUG mode, change ASAP 
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
# # ======== /Exemple connect-demo ======== # 

