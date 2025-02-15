from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile, UserProfile  
from django.contrib.auth import get_user_model

User = get_user_model()  
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        UserProfile.objects.create(user=instance)  # Create UserProfile too
