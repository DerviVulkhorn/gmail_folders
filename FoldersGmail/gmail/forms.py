from django import forms
from .models import *

class AddFormFolder(forms.Form):
    title = forms.CharField(max_length=255, label='Title folder')
    words = forms.CharField(max_length=300, label='Words for folder')
    discriprion = forms.CharField(max_length=300, label='Discription folder')