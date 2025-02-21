from django.shortcuts import render, redirect
from django.http import JsonResponse
import google.generativeai as genai
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from formtools.wizard.views import SessionWizardView
from django.utils.decorators import method_decorator
import speech_recognition as sr
import json
from django.views.decorators.csrf import csrf_exempt

from .forms import (
    QuestionnaireForm,
    Step1Form, Step2Form, Step3Form, Step4Form, Step5Form, Step6Form
)
from .models import Questionnaire, Profile, ChatSession, UserProfile
from .utils import analyze_message
from .sentiment import sia


# Configure Gemini API
genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')


# -------------- Authentication Views -------------- #
def signup(request):
    """Handles user signup."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in immediately after signup
            return redirect(settings.SIGNUP_REDIRECT_URL)  # Redirect to questionnaire
    else:
        form = UserCreationForm()
    return render(request, 'chatbot/signup.html', {'form': form})


def login_view(request):
    """Handles user login."""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('home')  # Redirect to home after login
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'chatbot/login.html', {'form': form})


def logout_view(request):
    """Handles user logout."""
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('home')


# -------------- Home and Chat Views -------------- #
def home(request):
    """Displays the home page."""
    return render(request, 'chatbot/home.html')


@login_required
def start_chat(request):
    """Redirects to the chat interface."""
    return redirect('chat')


@login_required
def chat(request, session_id=None):
    """Handles the chat interface and AI responses."""
    session = None  # Initialize session as None
    if session_id:
        # Retrieve specific session if session_id is provided
        session = ChatSession.objects.filter(id=session_id, user=request.user).first()
    else:
        # Get the latest chat session for the user
        session = ChatSession.objects.filter(user=request.user).order_by('-start_time').first()

    if request.method == 'POST':
        user_input = request.POST.get('user_input', '')
        try:
            detected_topic = detect_topic(user_input)  # Detect topic from user input
            sentiment_score = sia.polarity_scores(user_input)['compound']  # Analyze sentiment

            prompt = f"""As a mental health assistant, respond to this {detected_topic}-related message:
            User: {user_input}
            Helpful Response:"""

            response = model.generate_content(prompt) # Generate AI response
            ai_response = response.candidates[0].content.parts[0].text if response.candidates else "Sorry, I can't generate a response right now."


            if session:
                # Append messages to existing session
                session.messages += f"\nUser: {user_input}\nAI: {ai_response}"
                session.sentiment_score = sentiment_score
                session.save()
            else:
                # Create new chat session
                session = ChatSession.objects.create(
                    user=request.user,
                    topic=detected_topic,
                    messages=f"User: {user_input}\nAI: {ai_response}",
                    sentiment_score=sentiment_score
                )

            return JsonResponse({
                'ai_response': ai_response,
                'detected_topic': detected_topic,
                'session_id': session.id
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    context = {'session': session}  # Pass session to template
    return render(request, 'chatbot/chat.html', context)


def detect_topic(text):
    """Detects the topic of the user message."""
    keywords = {
        'anxiety': ['anxious', 'worry', 'panic', 'nervous'],
        'depression': ['sad', 'hopeless', 'empty', 'worthless'],
        'alcoholism': ['drink', 'alcohol', 'sober', 'relapse'],
        'stress': ['stress', 'overwhelm', 'pressure', 'burnout']
    }
    text_lower = text.lower()
    for topic, terms in keywords.items():
        if any(term in text_lower for term in terms):
            return topic
    return 'general'


# -------------- Voice Input View -------------- #
def voice_input(request):
    """Handles voice input and speech-to-text conversion."""
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


# -------------- Questionnaire Views (Wizard) -------------- #
FORMS = [  # Questionnaire form steps
    ("stress_level", Step1Form),
    ("sleep_hours", Step2Form),
    ("mood", Step3Form),
    ("exercise_frequency", Step4Form),
    ("social_support", Step5Form),
    ("diet_quality", Step6Form),
]

TEMPLATES = {  # Templates for each questionnaire step
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
    template_name = 'chatbot/questionnaire_wizard.html'  # General template for wizard

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]] # Dynamically set template for each step

    def done(self, form_list, **kwargs):
        """Processes completed questionnaire data."""
        user = self.request.user
        Questionnaire.objects.create( # Save questionnaire data to database
            user=user,
            stress_level=form_list[0].cleaned_data.get("stress_level"),
            sleep_hours=form_list[1].cleaned_data.get("sleep_hours"),
            mood=form_list[2].cleaned_data.get("mood"),
            exercise_frequency=form_list[3].cleaned_data.get("exercise_frequency"),
            social_support=form_list[4].cleaned_data.get("social_support"),
            diet_quality=form_list[5].cleaned_data.get("diet_quality"),
            completed=True,  # Mark questionnaire as completed
        )
        return redirect('/loading/') # Redirect to loading page


# -------------- Loading View -------------- #
def loading(request):
    """Renders the loading page."""
    return render(request, 'chatbot/loading.html')


# -------------- Profile View -------------- #
def profile_view(request):
    """Displays the user profile and progress with keyword-level progress."""
    user = request.user
    keywords_topics = { # Keywords mapped to topics for progress tracking
        'anxiety': ['anxious', 'worry', 'panic', 'nervous'],
        'depression': ['sad', 'hopeless', 'empty', 'worthless'],
        'stress': ['stress', 'overwhelm', 'pressure', 'burnout'],
        'alcoholism': ['drink', 'alcohol', 'sober', 'relapse']
    }

    chat_sessions = ChatSession.objects.filter(user=user) # Get all chat sessions for user
    latest_session = chat_sessions.order_by('-start_time').first() # Get latest session

    progress_data = { # Initialize progress data structure
        'total_sessions': chat_sessions.count(),
        'topics': {},
        'overall_sentiment': 0
    }

    total_sentiment = 0
    topic_sentiments = {} # To store total sentiment per topic for overall topic progress

    for topic, keywords in keywords_topics.items():
        topic_data = {'keywords': {}, 'total_sentiment': 0, 'keyword_count': 0}
        for keyword in keywords:
            keyword_sessions = chat_sessions.filter(messages__icontains=keyword) # Sessions containing keyword
            keyword_count = keyword_sessions.count()
            if keyword_count > 0:
                avg_sentiment = sum(s.sentiment_score for s in keyword_sessions) / keyword_count
                topic_data['keywords'][keyword] = {
                    'count': keyword_count,
                    'progress': int((avg_sentiment + 1) * 50) # Sentiment to 0-100 scale
                }
                topic_data['total_sentiment'] += avg_sentiment * keyword_count # Accumulate sentiment
                topic_data['keyword_count'] += keyword_count # Count of keywords with sessions

        if topic_data['keyword_count'] > 0: # Calculate topic progress if keywords found
            topic_avg_sentiment = topic_data['total_sentiment'] / topic_data['keyword_count']
            progress_data['topics'][topic] = {
                'keywords': topic_data['keywords'],
                'progress': int((topic_avg_sentiment + 1) * 50), # Topic progress is avg of keyword sentiments
                'count': topic_data['keyword_count'] # Total sessions for the topic (keywords combined)
            }
            total_sentiment += topic_avg_sentiment # Accumulate for overall sentiment

    if progress_data['topics']: # Calculate overall sentiment if topic data exists
        progress_data['overall_sentiment'] = int((total_sentiment / len(progress_data['topics']) + 1) * 50)

    context = {
        'progress_data': progress_data,
        'questionnaire_completed': Questionnaire.objects.filter(user=user).exists(),
        'latest_session': latest_session,  # Pass latest session to template
    }
    return render(request, 'chatbot/profile.html', context)


def calculate_progress(queryset):
    """Calculates progress based on average sentiment score."""
    if not queryset.exists():
        return 0
    avg_sentiment = sum(s.sentiment_score for s in queryset) / queryset.count()
    return int((avg_sentiment + 1) * 50)  # Sentiment to 0-100 scale


# -------------- Chat Message Processing (AJAX Endpoint) -------------- #
@csrf_exempt
@login_required
def chat_message(request):
    """Endpoint to process chat messages and update progress."""
    if request.method == "POST":
        data = json.loads(request.body)
        user = request.user
        message_text = data.get("message")

        if not message_text:
            return JsonResponse({"error": "Message is required"}, status=400)

        progress_increase = analyze_message(user, message_text) # Analyze message and update progress
        user_profile = UserProfile.objects.get(user=user) # Fetch updated user profile

        return JsonResponse({
            "message": "Message processed successfully",
            "progress_increase": progress_increase,
            "new_progress": user_profile.mental_health_progress
        })

    return JsonResponse({"error": "Invalid request"}, status=400)