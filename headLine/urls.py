"""newsApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'headline'

urlpatterns = [
    path('register/', views.register, name='register'), 
    path('login/', views.login_user, name='login'),
    path('addar/', views.addArticle, name='addar'),
    path('catar/', views.addCategory, name='catar'),
    path('', views.home, name='home'), 
    path('logout/', views.logout_user, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('article/<int:id>', views.article, name='article'),
    path('api/', include('headLine.api.api_urls'))
]
