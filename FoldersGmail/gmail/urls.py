# your_app_name/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_emails, name='get_email'),
    path('folders/', views.folders_work, name='folders_work'),
    path('add_folder/', views.add_folder, name='add_folder'),
    path('open/<int:foldres_id>/', views.open_folder, name='open_folder'),
    path('del/<int:folders_id>/', views.delete_folder, name='del_folder')
]