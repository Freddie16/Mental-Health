from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('start-chat/', views.start_chat, name='start-chat'),
    path('chat/', views.chat, name='chat'),
    path('signup/', views.signup, name='signup'),  # Add this line for signup
    path('login/', views.login_view, name='login'),  # Add this line for login
    path('logout/', views.logout_view, name='logout'), 
]