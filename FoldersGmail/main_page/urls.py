# your_app_name/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('info/', views.info, name='info')
]