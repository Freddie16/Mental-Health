# mentalhealthchatbot/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('chatbot.urls')),
    path('accounts/', include('allauth.urls')),  # Ensure this line is present

]