"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
# from home.views import *
from Rent.views import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns 

urlpatterns = [
    path('', index, name="index"),
    path('resource/',resource, name="resource"),
    path('delete-resource/<id>',delete_resource,name="delete_resource"),
    path('update-resource/<id>',update_resource,name="update_resource"),
    path('login/', login_page, name='login_page'),
    path('register/',register, name='register'),
    path('logout/', logout_page, name='logout_page'),
    path('get_resource/', get_resource, name='get_resource'),

        
    path('admin/', admin.site.urls),
    path("payment/", include("Rent.urls")),

    path('add_resource/',add_resource, name='add_resource'),
    path('payment/<int:resource_id>/', payment_view, name='payment'),
]

if settings.DEBUG: 
         urlpatterns += static(settings.MEDIA_URL,
                               document_root=settings.MEDIA_ROOT)
         
urlpatterns += staticfiles_urlpatterns()
