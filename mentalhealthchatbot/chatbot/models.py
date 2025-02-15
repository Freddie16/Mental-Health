from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from .sentiment import sia  # Import sia from sentiment.py

# Initialize Sentiment Analyzer

class ChatSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.CharField(max_length=100, default='general')
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)
    messages = models.TextField()
    sentiment_score = models.FloatField(default=0.0)  # Add this field
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s chat on {self.start_time}"

    class Meta:
        ordering = ['-created_at']

# Profile model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    progress_score = models.FloatField(default=0.0)

    def update_progress(self):
        """ Update progress without causing infinite recursion """
        Profile.objects.filter(pk=self.pk).update(progress_score=self.progress_score)

    def save(self, *args, **kwargs):
        """ Save method that avoids infinite recursion """
        if not kwargs.get('update_fields'):  # Avoid recursion by skipping update call
            super().save(*args, **kwargs)  # Save first to get a valid instance
            self.update_progress()  # Now update progress directly in DB
        else:
            super().save(*args, **kwargs)

    # Adding computed properties for admin display
    def questionnaire_completed(self):
        """ Returns whether the associated questionnaire is completed """
        questionnaire = getattr(self, 'questionnaire', None)
        return questionnaire.completed if questionnaire else False
    questionnaire_completed.boolean = True  # This will display a checkbox in the admin

    def chat_sessions(self):
        """ Returns the number of chat sessions related to this profile """
        return ChatSession.objects.filter(user=self.user).count()

    def __str__(self):
        return f"Profile of {self.user.username}"
STRESS_LEVEL_CHOICES = [
    ('Low', 'Low'),
    ('Moderate', 'Moderate'),
    ('High', 'High'),
]
# Questionnaire model
class Questionnaire(models.Model):
    EXERCISE_FREQUENCY_CHOICES = [
        ('Never', 'Never'),
        ('Rarely', 'Rarely'),
        ('Occasionally', 'Occasionally'),
        ('Regularly', 'Regularly'),
        ('Daily', 'Daily'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stress_level = models.CharField(max_length=8, choices=STRESS_LEVEL_CHOICES)  # Change max_length to 8
    sleep_hours = models.IntegerField()
    mood = models.CharField(max_length=50)
    exercise_frequency = models.CharField(max_length=20, choices=EXERCISE_FREQUENCY_CHOICES)
    social_support = models.CharField(max_length=100)
    diet_quality = models.CharField(max_length=100)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.mood}"


# UserProfile model for tracking mental health progress
class UserProfile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    mental_health_progress = models.FloatField(default=0.0)

# ChatMessage model for storing individual messages
class ChatMessage(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    message = models.TextField()
    sentiment_score = models.FloatField(default=0.0)
    timestamp = models.DateTimeField(auto_now_add=True)
