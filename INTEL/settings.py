from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')



# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-!nx!$(#4=9hba@j73sd*otb8nzh(g!_g5fxgn*#q_rnjpbwkk_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

AUTHENTICATION_BACKENDS = ['axes.backends.AxesStandaloneBackend', 'django.contrib.auth.backends.ModelBackend']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'axes',
    'rest_framework',
    'allauth_2fa',
    'django_otp',
    'django_otp.plugins.otp_totp',
    'corsheaders',
    'rest_framework.authtoken',
    'app',
    'Marketinsights',
    'ResearchAssistant'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'axes.middleware.AxesMiddleware',
    'corsheaders.middleware.CorsMiddleware'
]


AXES_LOCK_OUT_AT_FAILURE = False
# AXES_USE_USER_AGENT = True
AXES_COOLOFF_TIME = 1
AXES_LOGIN_FAILURE_LIMIT = 50

CORS_ALLOW_ALL_ORIGINS = True  # You can change this to True for all origins (not recommended for production)
CORS_ALLOW_CREDENTIALS = True  # If you need to send cookies or authentication headers
CORS_ALLOWED_ORIGINS = ["http://123.201.192.65:8181"]  # Replace with the actual domain of your frontend application

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

SESSION_ENGINE = 'django.contrib.sessions.backends.db'
# SESSION_COOKIE_SECURE = True  # Set to True for HTTPS environments
SESSION_COOKIE_AGE = 600 # 10 min
SESSION_COOKIE_NAME = 'session_id'
ROOT_URLCONF = 'INTEL.urls'

OTP_TOTP_ISSUER = "app"
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'INTEL.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'intel2',  # Or path to database file if using sqlite3.
        'USER': 'postgres',  # Not used with sqlite3.
        'PASSWORD': 'root',  # Not used with sqlite3.
        'HOST': 'localhost',  # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '5432',  # Set to empty string for default. Not used with sqlite3.
    }
}

# {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
#         'NAME': 'intellisense',  # Or path to database file if using sqlite3.
#         'USER': 'root',  # Not used with sqlite3.
#         'PASSWORD': 'Amol14@ms',  # Not used with sqlite3.
#         'HOST': 'localhost',  # Set to empty string for localhost. Not used with sqlite3.
#         'PORT': '3306',  # Set to empty string for default. Not used with sqlite3.
#     }
# }

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication'
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
        'rest_framework.permissions.AllowAny',
    ]
}

AUTH_USER_MODEL = 'app.CustomUser'


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
# User(will get acknowledgement mail) and Intellisense backend team (will get email notification)
# from EMAIL_HOST_USER. To be set by Intellisense.
EMAIL_HOST_USER = 'vempataputejeswari07@gmail.com'
EMAIL_HOST_PASSWORD = 'nuvd jgah bqra wqce'
