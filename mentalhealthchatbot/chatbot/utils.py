from gtts import gTTS
import os
import speech_recognition as sr
from textblob import TextBlob
from pymongo import MongoClient
from django.db.models import F
from .models import UserProfile, ChatMessage
from .sentiment import sia  # Import sia from sentiment.py


# Initialize Sentiment Analyzer
client = MongoClient("mongodb://localhost:27017/")
db = client["mental_health_chatbot"]
messages_collection = db["chat_messages"]
def text_to_speech(text, filename="response.mp3"):
    tts = gTTS(text=text, lang='en')
    tts.save(filename)
    return filename

def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Sorry, I could not understand the audio."
        except sr.RequestError:
            return "Sorry, there was an issue with the speech recognition service."
        
POSITIVE_KEYWORDS = {"feeling good", "improving", "hopeful", "confident", "better", "stronger"}

def analyze_message(user, message_text):
    # Sentiment Analysis using TextBlob
    sentiment = TextBlob(message_text).sentiment.polarity  # -1 (negative) to +1 (positive)

    # Keyword Tracking
    keyword_score = sum(1 for word in POSITIVE_KEYWORDS if word in message_text.lower())

    # Overall Progress Calculation
    progress_increment = (sentiment * 10) + (keyword_score * 5)  # Weighted formula

    # Store message in MongoDB
    messages_collection.insert_one({"user": str(user.id), "message": message_text, "sentiment": sentiment})

    # Update User Progress
    UserProfile.objects.filter(user=user).update(
        mental_health_progress=F("mental_health_progress") + progress_increment
    )

    # Save message with sentiment score in Django DB
    ChatMessage.objects.create(user=user, message=message_text, sentiment_score=sentiment)

    return progress_increment
def analyze_message(user, message_text):
    # Example function that uses sia
    sentiment_score = sia.polarity_scores(message_text)['compound']
    # Perform your logic here
    return sentiment_score