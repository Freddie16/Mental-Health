from django.contrib import admin
from chatbot.models import Profile, Questionnaire, ChatSession

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'questionnaire_completed', 'chat_sessions', 'progress_score']
    search_fields = ['user__username']

@admin.register(Questionnaire)
class QuestionnaireAdmin(admin.ModelAdmin):
    list_display = ['user', 'stress_level', 'mood', 'completed']
    list_filter = ['stress_level', 'mood', 'completed']
    search_fields = ['user__username']

@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username']