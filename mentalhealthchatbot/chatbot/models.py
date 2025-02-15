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


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    questionnaire_completed = models.BooleanField(default=False)
    chat_sessions = models.IntegerField(default=0)
    progress_score = models.IntegerField(default=50)  # Start at neutral 50%

    def update_progress(self):
        print(f"Updating progress for {self.user.username}...")  # Debugging

        # Get the last 5 chat sessions
        chats = ChatSession.objects.filter(user=self.user).order_by('-created_at')[:5]

        sentiment_scores = []
        for chat in chats:
            score = sia.polarity_scores(chat.messages)['compound']  # Get sentiment score (-1 to 1)
            sentiment_scores.append(score)

        if sentiment_scores:
            avg_score = sum(sentiment_scores) / len(sentiment_scores)
            self.progress_score = int((avg_score + 1) * 50)  # Convert to 0-100 scale
        else:
            self.progress_score = 50  # Default to neutral if no chats

        print(f"New progress score for {self.user.username}: {self.progress_score}")  # Debugging
        self.save(update_fields=['progress_score'])  # Ensure only progress is updated

    def save(self, *args, **kwargs):
        self.update_progress()
        super().save(*args, **kwargs)


class Questionnaire(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stress_level = models.IntegerField()
    sleep_hours = models.IntegerField()
    mood = models.CharField(max_length=50)
    exercise_frequency = models.IntegerField()
    social_support = models.CharField(max_length=100)
    diet_quality = models.CharField(max_length=100)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.mood}"


class UserProfile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    mental_health_progress = models.FloatField(default=0.0)


class ChatMessage(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    message = models.TextField()
    sentiment_score = models.FloatField(default=0.0)
    timestamp = models.DateTimeField(auto_now_add=True)
