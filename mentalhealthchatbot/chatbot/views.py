# chatbot/views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
import google.generativeai as genai
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages



# Configure Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)

# Initialize the Gemini model
model = genai.GenerativeModel('gemini-pro')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Redirect to home page after successful signup
    else:
        form = UserCreationForm()
    return render(request, 'chatbot/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('home')
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
            ai_response = response.text
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