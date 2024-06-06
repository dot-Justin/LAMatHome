  
from django.contrib import admin
from django.urls import path, include
from . import views 
from .views import JournalEntryListView, ContactListView, settings_view

app_name = 'main'

urlpatterns = [
    path('', views.base, name='base'),
    path('journal/', JournalEntryListView.as_view(), name='journal-list'),
    path('contacts/', ContactListView.as_view(), name='contact-list'),
    path('settings/', settings_view, name='settings'),
]
