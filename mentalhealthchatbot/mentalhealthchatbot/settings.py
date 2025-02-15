"""
Django settings for mentalhealthchatbot project.

Generated by 'django-admin startproject' using Django 5.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-5fm$*ss8(udrnd%5##fqg=uejb(uyjlg+cvl$a(p74p#e&r-0l'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['mindchat.onrender.com', '127.0.0.1', 'localhost']

CORS_ALLOWED_ORIGINS = [
    "https://mindchat.onrender.com",
    "http://localhost:3000",  # Add this if testing locally
]


CORS_ALLOW_CREDENTIALS = True
# settings.py

# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # SMTP server for Gmail
EMAIL_PORT = 587  # Port for Gmail's SMTP server
EMAIL_USE_TLS = True  # Use TLS encryption
EMAIL_HOST_USER = 'freddiemurigi@gmail.com'  # Your Gmail address
EMAIL_HOST_PASSWORD = 'btdp ftwk gwcd xorn'  # Your Gmail app password (not your regular password)
EMAIL_FILE_PATH = '/tmp/app-messages'  # Path to save emails


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'chatbot',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
    'crispy_forms',
    'corsheaders',
    'formtools',
    'rest_framework',  


]
SITE_ID = 1

ACCOUNT_LOGIN_METHODS = ['email']  # Replace ACCOUNT_AUTHENTICATION_METHOD
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
SOCIALACCOUNT_QUERY_EMAIL = True

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',  # Add this line
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Correct
    'corsheaders.middleware.CorsMiddleware',


]

ROOT_URLCONF = 'mentalhealthchatbot.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "chatbot/templates"],  # Add this
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mentalhealthchatbot.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

GEMINI_API_KEY ='AIzaSyDQFZ9jnSvQqzJ_WsZX4-XwcZxUI-y4iwg'  # Replace with your actual API key
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# settings.py
LOGIN_URL = '/accounts/login/'  # Point to your login URL
# Change this line in settings.py
LOGIN_REDIRECT_URL = 'home'  # Login goes to home
LOGOUT_REDIRECT_URL = '/'  # Logout goes to home
ACCOUNT_SIGNUP_REDIRECT_URL = '/questionnaire/'  # Ensure this path is correct
  # Signup should go to the questionnaire


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
    },
    'facebook': {
        'METHOD': 'oauth2',
        'SCOPE': ['email', 'public_profile'],
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'FIELDS': ['id', 'email', 'name'],
    },

    
}

import nltk
nltk.download('vader_lexicon')
