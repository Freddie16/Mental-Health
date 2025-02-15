from django.contrib import admin
from chatbot.models import Profile, Questionnaire, ChatSession

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'questionnaire_completed', 'chat_sessions')  # Ensure these exist in Profile

@admin.register(Questionnaire)
class QuestionnaireAdmin(admin.ModelAdmin):
    list_display = ['user', 'stress_level', 'mood', 'completed']
    list_filter = ['stress_level', 'mood', 'completed']
    search_fields = ['user__username']

@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'start_time', 'topic']
    list_filter = ['start_time', 'topic']
    search_fields = ['user__username', 'topic', 'messages']
    readonly_fields = ['start_time', 'end_time']
