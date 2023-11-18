from pathlib import Path
import os
import sys
import dj_database_url
from django.core.management.utils import get_random_secret_key


SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", get_random_secret_key())
BASE_DIR = Path(__file__).resolve().parent.parent
DEBUG = os.getenv("DEBUG", "False") == "True"
ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")
ALLOWED_HOSTS=['*']
#DEVELOPMENT_MODE = os.getenv("DEVELOPMENT_MODE", "False") == "True"

# Application definition

INSTALLED_APPS = [
    'whitenoise.runserver_nostatic',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "cmsHTMX",
    "django_htmx",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'headlessDjango.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            '/home/user/websites/headlessDjango/cms/templates/',
            '/home/user/websites/headlessDjango/cmsHTMX/templates/'
            ],
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

WSGI_APPLICATION = 'headlessDjango.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# 'ENGINE': 'django.db.backends.postgresql_psycopg2',

DGTOKEN='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'
AI_SECRET_KEY='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'
DB_NAME='headlessdjango'
DB_USER='headless'
DB_PASSWORD='beans_hot_drive_dysfunctional_mouse'
DB_HOST='127.0.0.1'
DB_PORT='5432'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        #'NAME': os.getenv('DB_NAME'),
        #'USER': os.getenv('DB_USER'),
        #'PASSWORD': os.getenv('DB_PASSWORD'),
        #'HOST': os.getenv('DB_HOST'),
        #'PORT': os.getenv('DB_PORT'),

        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': DB_PORT,

    }
}

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

STATIC_ROOT = BASE_DIR / "staticfiles"
STATIC_URL = '/static/'
#STATICFILES_DIRS = [
#    "/home/user/websites/headlessDjango/cmsHTMX/static",
#]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

IMG_BODY = {
    "width": 800,
    "quality": 82
}

IMG_HEADER = {
    "width": 800,
    "quality": 84
}

IMG_THUMBNAIL = {
    "width": 200,
    "quality": 60
}

LOGIN_URL = "/admin/login/?next=/cmshtmx/"

#DGTOKEN = os.getenv('DGTOKEN')
BLOG_REPO = 'blog.alistairrobinson.me'
CONTENT_FOLDER = 'content'
IMG_BUCKET = 'https://ik.imagekit.io/alistairrobinson/blog'
#AI_SECRET_KEY = os.getenv('AI_SECRET_KEY')