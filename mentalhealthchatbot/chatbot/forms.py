# chatbot/forms.py
from django import forms
from .models import Questionnaire

class QuestionnaireForm(forms.ModelForm):
    class Meta:
        model = Questionnaire
        fields = ['stress_level', 'sleep_hours', 'mood', 'exercise_frequency', 'social_support', 'diet_quality']
class Step1Form(forms.Form):
    stress_level = forms.ChoiceField(
        choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')],
        widget=forms.RadioSelect,
        label="How would you describe your current stress level?"
    )

class Step2Form(forms.Form):
    sleep_hours = forms.IntegerField(
        widget=forms.NumberInput(attrs={'min': 0, 'max': 24}),
        label="How many hours of sleep do you get on average per night?"
    )

class Step3Form(forms.Form):
    mood = forms.ChoiceField(
        choices=[('Happy', 'Happy'), ('Anxious', 'Anxious'), ('Depressed', 'Depressed')],
        widget=forms.RadioSelect,
        label="How would you describe your current mood?"
    )

class Step4Form(forms.Form):
    exercise_frequency = forms.ChoiceField(
        choices=[('Never', 'Never'), ('Rarely', 'Rarely'), ('Sometimes', 'Sometimes'), ('Often', 'Often')],
        widget=forms.RadioSelect,
        label="How often do you exercise?"
    )

class Step5Form(forms.Form):
    social_support = forms.ChoiceField(
        choices=[('Low', 'Low'), ('Moderate', 'Moderate'), ('High', 'High')],
        widget=forms.RadioSelect,
        label="How would you rate your social support system?"
    )

class Step6Form(forms.Form):
    diet_quality = forms.ChoiceField(
        choices=[('Poor', 'Poor'), ('Average', 'Average'), ('Good', 'Good')],
        widget=forms.RadioSelect,
        label="How would you rate the quality of your diet?"
    )