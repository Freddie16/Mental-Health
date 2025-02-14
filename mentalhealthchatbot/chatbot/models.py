# chatbot/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.utils import timezone


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
    topic = models.CharField(max_length=100, default='general')
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)
    messages = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s chat on {self.start_time}"

    class Meta:
        ordering = ['-created_at']

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add your profile fields here
    questionnaire_completed = models.BooleanField(default=False)
    chat_sessions = models.IntegerField(default=0)
    progress_score = models.IntegerField(default=0)
    
    def update_progress(self):
        """
        Calculate and update the user's progress based on their activities
        """
        # Calculate base progress from questionnaire
        base_progress = 20 if self.questionnaire_completed else 0
        
        # Add progress from chat sessions (max 80 points from chats)
        chat_progress = min(self.chat_sessions * 10, 80)
        
        # Update total progress
        self.progress_score = base_progress + chat_progress
        self.save()
    
    def __str__(self):
        return f"{self.user.username}'s Profile"