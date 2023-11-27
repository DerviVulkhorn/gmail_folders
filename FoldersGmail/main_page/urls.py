# your_app_name/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('about/', views.about, name='about'),
    path('info/', views.info, name='info'),
    path('main/', views.main, name='main')
]