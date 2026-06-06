from pathlib import Path
from decouple import config, Csv

# =========================

# BASE DIRECTORY

# =========================

BASE_DIR = Path(__file__).resolve().parent.parent

# =========================

# SECURITY SETTINGS

# =========================

SECRET_KEY = config("SECRET_KEY")

DEBUG = True  # Development mode

ALLOWED_HOSTS = config(
"ALLOWED_HOSTS",
default="127.0.0.1,localhost",
cast=Csv()
)

# =========================

# INSTALLED APPS

# =========================

INSTALLED_APPS = [
'django.contrib.admin',
'django.contrib.auth',
'django.contrib.contenttypes',
'django.contrib.sessions',
'django.contrib.messages',
'django.contrib.staticfiles',

"widget_tweaks",
"RecipeApp",

]

# =========================

# MIDDLEWARE

# =========================

MIDDLEWARE = [
'django.middleware.security.SecurityMiddleware',
'django.contrib.sessions.middleware.SessionMiddleware',
'django.middleware.common.CommonMiddleware',
'django.middleware.csrf.CsrfViewMiddleware',
'django.contrib.auth.middleware.AuthenticationMiddleware',
'django.contrib.messages.middleware.MessageMiddleware',
'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# =========================

# ROOT URL CONFIG

# =========================

ROOT_URLCONF = 'RecipeProject.urls'

# =========================

# TEMPLATES CONFIG

# =========================

TEMPLATES = [
{
'BACKEND': 'django.template.backends.django.DjangoTemplates',
'DIRS': [BASE_DIR / "templates"],
'APP_DIRS': True,
'OPTIONS': {
'context_processors': [
'django.template.context_processors.request',
'django.contrib.auth.context_processors.auth',
'django.contrib.messages.context_processors.messages',
],
},
},
]

# =========================

# WSGI APPLICATION

# =========================

WSGI_APPLICATION = 'RecipeProject.wsgi.application'

# =========================

# DATABASE

# =========================

DATABASES = {
'default': {
'ENGINE': 'django.db.backends.sqlite3',
'NAME': BASE_DIR / 'db.sqlite3',
}
}

# =========================

# PASSWORD VALIDATION

# =========================

AUTH_PASSWORD_VALIDATORS = [
{'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
{'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
{'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
{'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# =========================

# LANGUAGE & TIMEZONE

# =========================

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# =========================

# STATIC FILES

# =========================

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# =========================

# MEDIA FILES (IMAGES)

# =========================

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"

# =========================

# DEFAULT PRIMARY KEY

# =========================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# =========================

# EMAIL CONFIG

# =========================

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = config("EMAIL_HOST", default="smtp.gmail.com")
EMAIL_PORT = config("EMAIL_PORT", default=587, cast=int)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=True, cast=bool)
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")

# =========================

# AUTH SETTINGS

# =========================

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = '/accounts/login/'
