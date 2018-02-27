"""
Django settings for dev project.

Generated by 'django-admin startproject' using Django 1.11.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*gjsv)j9b2swuy@bmlf&a99pj5iretjat%ogrz9v(!@+e2#lm1'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SENDGRID_EMAIL_HOST = "smtp.sendgrid.net"
# SENDGRID_EMAIL_PORT = "587"
# SENDGRID_EMAIL_USERNAME = "app86156095@heroku.com"
# SENDGRID_EMAIL_PASSWORD = "FReakyboygeniuse123"


EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'shakaraexpress@gmail.com'
EMAIL_MAIN = 'shakaraexpress@gmail.com'
EMAIL_HOST_PASSWORD = 'gtbank007'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# EMAIL_BACKEND = 'sgbackend.SenderGridBackend',
# SENDGRID_API_KEY = 

DEFAULT_FROM_EMAIL = "Team SHAKARA EXPRESS <info@shakaraexpress.com>"

# ADMINS = [('Team SHAKARA EXPRESS', EMAIL_HOST_USER)]
# MANAGERS = ADMINS

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'imagekit',

    # custom app
    'core',
    'tags',
    'dashboard',
    'analytics',
    'bookings',
    'newsletter',
    'orders',
    'products',
    'services',
    'shops',
    'billing',

    # third-party-app-modules
    'storages',
    'crispy_forms',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'django_comments_xtd',
    'django_comments',
    'star_ratings',
    'pagedown',
    'markdown_deux',
    'django_filters',
    'carton',
    # 'shopping',

    # socialmedia auth
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.instagram',
    'allauth.socialaccount.providers.twitter',
]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'dev.urls'

CRISPY_TEMPLATE_PACK = 'bootstrap3'

RECENT_BOOKING_NUMBER = 10

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

CART_PRODUCT_MODEL = 'products.models.Product'

COMMENTS_APP = 'django_comments_xtd'
COMMENTS_XTD_MAX_THREAD_LEVEL = 2
COMMENTS_XTD_CONFIRM_EMAIL = True
#  To help obfuscating comments before they are sent for confirmation.
COMMENTS_XTD_SALT = (b"Timendi causa est nescire. "
                     b"Aequam memento rebus in arduis servare mentem.")
# Source mail address used for notifications.
COMMENTS_XTD_FROM_EMAIL = "shakaraexpress@gmail.com"
# Contact mail address to show in messages.
COMMENTS_XTD_CONTACT_EMAIL = "shakaraexpress@gmail.com"
COMMENTS_XTD_MARKUP_FALLBACK_FILTER = 'markdown'

ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = True
# ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 7
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 300
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_MIN_LENGTH = 3
# ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = True
ACCOUNT_SESSION_REMEMBER = "Remember me?"
ACCOUNT_LOGOUT_REDIRECT_URL = "/"
LOGIN_REDIRECT_URL = "/"
ACCOUNT_USERNAME_BLACKLIST = ['admin', 'settings', 'news', 'about', 'help',
                           'signin', 'signup', 'signout', 'terms', 'privacy',
                           'cookie', 'new', 'login', 'logout', 'administrator',
                           'join', 'account', 'username', 'root', 'blog',
                           'user', 'users', 'billing', 'subscribe', 'reviews',
                           'review', 'blog', 'blogs', 'edit', 'mail', 'email',
                           'home', 'job', 'jobs', 'contribute', 'newsletter',
                           'shop', 'profile', 'register', 'auth',
                           'authentication', 'campaign', 'config', 'delete',
                           'remove', 'forum', 'forums', 'download',
                           'downloads', 'contact', 'blogs', 'feed', 'feeds',
                           'faq', 'intranet', 'log', 'registration', 'search',
                           'explore', 'rss', 'support', 'status', 'static',
                           'media', 'setting', 'css', 'js', 'follow',
                           'activity', 'questions', 'articles', 'network', 'mathemartins',
                           'bae','boo','fuck','pussy','dick','shit','sheet','pussyNigga','pussynigga',
                           'prick','virgina','camelToe','bitch', 'trackamechanic',
                           ]

WSGI_APPLICATION = 'dev.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'shakaraexpress.sqlite3'),
    }
}

# import dj_database_url
# db_from_env = dj_database_url.config()
# DATABASES['default'].update(db_from_env)

# CORS_REPLACE_HTTPS_REFERER       = True
# HOST_SCHEME                      = "https://"
# SECURE_PROXY_SSL_HEADER          = ('HTTP_X_FORWARDED_PROTO', 'https')
# SECURE_SSL_REDIRECT              = True
# SESSION_COOKIE_SECURE            = True
# CSRF_COOKIE_SECURE               = True
# SECURE_HSTS_INCLUDE_SUBDOMAINS   = True
# SECURE_HSTS_SECONDS              = 1000000
# SECURE_FRAME_DENY                = True

# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SECURE_SSL_REDIRECT = True


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DATE_INPUT_FORMATS = [
                        '%Y-%m-%d %H:%M:%S',
                        '%Y-%m-%d %H:%M',
                        '%Y-%m-%d', 
                        '%m/%d/%Y %H:%M:%S', 
                        '%m/%d/%Y %H:%M', 
                        '%m/%d/%Y', 
                        '%m/%d/%y %H:%M:%S', 
                        '%m/%d/%y %H:%M', 
                        '%m/%d/%y'
                    ] 


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
from dev.aws.conf import *

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

#TEAM MANAGERS
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

#TEAM DOESN'T
STATIC_ROOT = os.path.join(BASE_DIR, "static_cdn", "staticfiles")

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

# MEDIA_ROOT = os.path.join(BASE_DIR, "static_cdn", "media")

#Braintree Payments Details
BRAINTREE_PUBLIC = "qn3p5n7njksw47r3"
BRAINTREE_PRIVATE = "d14ac944794c0df1c81991ecf49221ff"
BRAINTREE_MERCHANT_ID = "n84nynknvzz3j3sz"
BRAINTREE_ENVIRONEMNT = "Sandbox"