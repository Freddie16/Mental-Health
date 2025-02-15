from django.apps import apps
from rest_framework import serializers

try:
    from chatbot.models import ChatSession
except ImportError:
    ChatSession = None  # Avoid breaking the import

class ChatSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatSession
        fields = '__all__'

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.Meta.model = apps.get_model('chatbot', 'ChatSession')  # Load model dynamically
