from django.shortcuts import render, redirect
from django.http import JsonResponse
import google.generativeai as genai
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import QuestionnaireForm
from formtools.wizard.views import SessionWizardView
from .forms import Step1Form, Step2Form, Step3Form, Step4Form, Step5Form, Step6Form
from .models import Questionnaire
from django.utils.decorators import method_decorator
import time
import speech_recognition as sr  # Added missing import

# Configure Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)

# Initialize the Gemini model
model = genai.GenerativeModel('gemini-pro')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in the user immediately

            # Redirect to questionnaire after signup
            return redirect(settings.SIGNUP_REDIRECT_URL)  # Use the new setting
    
    else:
        form = UserCreationForm()

    return render(request, 'chatbot/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Direct login users to home
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('home')  # Changed from 'chat' to 'home'
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    
    return render(request, 'chatbot/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('home')

def home(request):
    """Always show home page first"""
    return render(request, 'chatbot/home.html')

@login_required
def start_chat(request):
    """Redirect to chat interface after authentication"""
    return redirect('chat')

def chat(request):
    if request.method == 'POST':
        user_input = request.POST.get('user_input', '')
        try:
            # Generate a response using Gemini
            response = model.generate_content(user_input)
            ai_response = response.candidates[0].content.parts[0].text if response.candidates else "No response from AI"
            return JsonResponse({'ai_response': ai_response})
        except Exception as e:
            return JsonResponse({'error': f"Gemini Error: {str(e)}"}, status=500)
    return render(request, 'chatbot/chat.html')

def voice_input(request):
    """Voice input view that handles speech-to-text conversion"""
    if request.method == 'POST':
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            audio = recognizer.listen(source)
            try:
                text = recognizer.recognize_google(audio)
                return JsonResponse({'text': text})
            except sr.UnknownValueError:
                return JsonResponse({'error': 'Could not understand audio'})
    return render(request, 'chatbot/voice_input.html')

FORMS = [
    ("stress_level", Step1Form),
    ("sleep_hours", Step2Form),
    ("mood", Step3Form),
    ("exercise_frequency", Step4Form),
    ("social_support", Step5Form),
    ("diet_quality", Step6Form),
]

TEMPLATES = {
    "stress_level": "chatbot/questionnaire_step1.html",
    "sleep_hours": "chatbot/questionnaire_step2.html",
    "mood": "chatbot/questionnaire_step3.html",
    "exercise_frequency": "chatbot/questionnaire_step4.html",
    "social_support": "chatbot/questionnaire_step5.html",
    "diet_quality": "chatbot/questionnaire_step6.html",
}

@method_decorator(login_required, name='dispatch')
class QuestionnaireWizard(SessionWizardView):
    form_list = FORMS

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def done(self, form_list, **kwargs):
        user = self.request.user

        # Prevent duplicate questionnaire entries
        if Questionnaire.objects.filter(user=user).exists():
            return redirect('/chat/')  # Redirect to chat if already filled

        # Save questionnaire data
        questionnaire = Questionnaire.objects.create(
            user=user,
            stress_level=form_list[0].cleaned_data.get("stress_level"),
            sleep_hours=form_list[1].cleaned_data.get("sleep_hours"),
            mood=form_list[2].cleaned_data.get("mood"),
            exercise_frequency=form_list[3].cleaned_data.get("exercise_frequency"),
            social_support=form_list[4].cleaned_data.get("social_support"),
            diet_quality=form_list[5].cleaned_data.get("diet_quality"),
        )
        
        return redirect('/chat/')  # After questionnaire, redirect to chat

# Add a view to handle the loading screen and redirect
def loading(request):
    # Simulate a delay (e.g., processing data)
    time.sleep(3)  # Adjust the delay as needed
    return redirect('chat')
