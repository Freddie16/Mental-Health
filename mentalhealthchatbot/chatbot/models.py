# chatbot/models.py
from django.db import models
from django.contrib.auth.models import User

class Questionnaire(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stress_level = models.CharField(max_length=50, choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')])
    sleep_hours = models.IntegerField()
    mood = models.CharField(max_length=50, choices=[('Happy', 'Happy'), ('Anxious', 'Anxious'), ('Depressed', 'Depressed')])
    exercise_frequency = models.CharField(
        max_length=50,
        choices=[('Never', 'Never'), ('Rarely', 'Rarely'), ('Sometimes', 'Sometimes'), ('Often', 'Often')],
        default='Sometimes'  # Add default value
    )
    social_support = models.CharField(
        max_length=50,
        choices=[('Low', 'Low'), ('Moderate', 'Moderate'), ('High', 'High')],
        default='Moderate'  # Add default value
    )
    diet_quality = models.CharField(
        max_length=50,
        choices=[('Poor', 'Poor'), ('Average', 'Average'), ('Good', 'Good')],
        default='Average'  # Add default value
    )
    completed = models.BooleanField(default=False)
class ChatSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class ChatMessage(models.Model):
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE)
    content = models.TextField()
    is_user = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

    