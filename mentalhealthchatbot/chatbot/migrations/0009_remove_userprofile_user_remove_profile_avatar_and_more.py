# Generated by Django 5.1.6 on 2025-02-14 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0008_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='user',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='avatar',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='bio',
        ),
        migrations.AddField(
            model_name='profile',
            name='chat_sessions',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='profile',
            name='progress_score',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='profile',
            name='questionnaire_completed',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='MentalHealthProgress',
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
