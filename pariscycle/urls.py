"""
URL configuration for pariscycle project.

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
from django.urls import include, path
from . import views

urlpatterns = [
    path('parisCycle/', views.index, name='base'),
    path('parisCycle/home', include("home.urls"), name='home'),
    path('parisCycle/data', views.parisdata, name='parisdata'),
    path('parisCycle/maps', views.maps, name='maps'),
    path('admin', admin.site.urls, name='adminLogin'),
    path('parisCycle/article', include("actu.urls"), name='article')
]