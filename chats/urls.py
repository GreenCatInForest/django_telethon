from django.contrib import admin
from django.urls import include, path
from django.shortcuts import render
from . import views

urlpatterns = [
    path('telegram/login/', views.telegram_login_view, name='telegram_login_view'),
    path('telegram/verify/', views.telegram_verify_view, name='telegram_verify_view'),
    path('telegram/chats/', views.telegram_chats_view, name='telegram_chats_view'),
]