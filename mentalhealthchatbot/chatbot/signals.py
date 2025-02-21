# chatbot/signals.py
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import UserProfile, Profile # added Profile import

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance, questionnaire_completed=False)  # Set questionnaire_completed to False
        Profile.objects.create(user=instance) # Create Profile too, removed progress_score

post_save.connect(create_user_profile, sender=User)