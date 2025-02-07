# chatbot/views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
import google.generativeai as genai
from django.conf import settings
from django.contrib.auth.decorators import login_required


# Configure Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)

# Initialize the Gemini model
model = genai.GenerativeModel('gemini-pro')

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