# your_app_name/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_emails, name='get_email'),
]