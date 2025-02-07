# chatbot/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('start-chat/', views.start_chat, name='start-chat'),
    path('chat/', views.chat, name='chat'),
]