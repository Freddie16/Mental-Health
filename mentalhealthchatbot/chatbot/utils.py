from gtts import gTTS
import os
import speech_recognition as sr


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