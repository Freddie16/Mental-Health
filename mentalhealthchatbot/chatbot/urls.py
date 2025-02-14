from django.urls import path
from . import views
from .views import home, start_chat, chat, signup, login_view, logout_view, QuestionnaireWizard, loading
from .forms import Step1Form, Step2Form, Step3Form, Step4Form, Step5Form, Step6Form
from .views import profile_view





FORMS = [
    ("stress_level", Step1Form),
    ("sleep_hours", Step2Form),
    ("mood", Step3Form),
    ("exercise_frequency", Step4Form),
    ("social_support", Step5Form),
    ("diet_quality", Step6Form),
]


urlpatterns = [
    path('', home, name='home'),
    path('start-chat/', start_chat, name='start-chat'),
    path('chat/', chat, name='chat'),
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('questionnaire/', QuestionnaireWizard.as_view(), name='questionnaire'),
    path('loading/', loading, name='loading'),  # Add this line
    path('profile/', profile_view, name='profile'),



]