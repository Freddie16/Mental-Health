# Generated by Django 5.1.6 on 2025-02-15 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0016_remove_profile_chat_sessions_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionnaire',
            name='stress_level',
            field=models.CharField(choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')], max_length=6),
        ),
    ]
